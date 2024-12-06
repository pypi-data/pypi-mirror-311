import numpy as np
import pandas as pd
import networkx as nx
from copy import deepcopy

import random
from itertools import permutations


class SyntheticStructure:
    def __init__(self, num_nodes, **kwargs):
        self.num_nodes = num_nodes
        self.node_names = [f'X{i+1}' for i in range(self.num_nodes)]
        self.random_seed = kwargs.get(
            'random_seed', None)  # TODO: Add random seed
        self.G = nx.DiGraph()
        self.G.add_nodes_from(self.node_names)
        self.generate_spanning_tree()
        self.add_random_edges()

    def generate_spanning_tree(self):
        """Generate a random spanning tree to ensure all nodes are connected."""
        nodes = random.sample(self.node_names, len(self.node_names))
        for i in range(1, len(nodes)):
            possible_parents = nodes[:i]
            parent = random.choice(possible_parents)
            self.G.add_edge(parent, nodes[i])

    def add_random_edges(self):
        for (node1, node2) in permutations(self.node_names, 2):
            if not nx.has_path(self.G, node2, node1):  # Check for cycle
                if random.random() < 0.2:  # Randomly decide to add an edge
                    self.G.add_edge(node1, node2)

    def get_edges(self):
        return list(self.G.edges())

    def get_nodes(self):
        return list(self.G.nodes())

    def visualize(self):
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Matplotlib is not installed. Visualization is not possible.")
            return

        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos, with_labels=True, node_color='lightblue',
                font_weight='bold', node_size=700, font_size=18)
        plt.show()

    def possible_ATEs(self):
        """Identify pairs of nodes where an ATE might be estimable."""
        possible_ATE_pairs = []
        for node1, node2 in permutations(self.node_names, 2):
            if nx.has_path(self.G, node1, node2):
                possible_ATE_pairs.append((node1, node2))
        return possible_ATE_pairs


class SyntheticData:
    def __init__(self, node_specs, edge_specs, **kwargs):
        self.nodes = node_specs.keys()
        self.edges = [(x["nodes"][0], x["nodes"][1]) for x in edge_specs]
        self.edge_weights = [x["effect"] for x in edge_specs]
        self.node_specs = node_specs
        self.original_mean = {}
        self.original_std = {}
        self.dependency_map = self._generate_dependency_map()
        self.ordered_nodes = self._topological_sort()
        self.generate_data()

    def _generate_dependency_map(self):
        dependency_map = {}
        for edge in self.edges:
            parent, child = edge
            if child not in dependency_map:
                dependency_map[child] = []
            dependency_map[child].append(parent)
        return dependency_map

    def _topological_sort(self):
        G = nx.DiGraph()
        G.add_edges_from(self.edges)
        return list(nx.topological_sort(G))

    def generate_data(self, num_samples=100):
        self.coefs = {}
        self.data = {}
        self.noise = {}

        for node in self.ordered_nodes:
            if node not in self.dependency_map:  # Root node
                self.data[node] = np.random.normal(0, 1, num_samples)
            else:
                parents = self.dependency_map[node]
                parent_data = [self.data[parent] for parent in parents]
                self.coefs[node] = np.array([self.edge_weights[self.edges.index(
                    (parent, node))] for parent in parents], dtype=np.float64)

                # Compute data for node without noise so
                # we can calculate the noise std from R2
                self.data[node] = self.coefs[node] @ np.stack(
                    parent_data, axis=0)
                # Compute noise for node
                noise_std = np.sqrt(
                    self.data[node].var() * (1 - self.node_specs[node]["r2"]))
                self.noise[node] = np.random.normal(
                    0, noise_std, num_samples)
                # Add noise to the data
                self.data[node] += self.noise[node]

            # Record the mean, std that the coefficients and intercepts are based on (inputs are already standardised to 0, 1)
            self.original_mean[node] = self.data[node].mean()
            self.original_std[node] = self.data[node].std()

            self.data[node] = (
                self.data[node] - self.original_mean[node]) / self.original_std[node]
            if node in self.dependency_map:
                self.coefs[node] = self.coefs[node] / self.original_std[node]

        # Convert data to desired scales
        for node in self.ordered_nodes:
            self.data[node] = self.data[node] * self.node_specs[node]['std'] + \
                self.node_specs[node]['mean']

        self.data = pd.DataFrame(self.data)

        # Do clipping based on node_specs if min/max are provided
        for node in self.nodes:
            lower_bound = self.node_specs[node].get('min', None)
            upper_bound = self.node_specs[node].get('max', None)
            self.data[node] = np.clip(
                self.data[node], lower_bound, upper_bound)
        return self.data

    def forward(self, values):
        # Deep copy is used to not affect the original self.data when modifying forward_data
        forward_data = deepcopy(self.data)

        # Update forward_data with the new values
        for node, value in values.items():
            forward_data[node] = value

        # Use node scales to standardise the data according to the original data (not the modified forward_data)
        for node in self.ordered_nodes:
            forward_data[node] = (
                forward_data[node] - self.node_specs[node]['mean']) / self.node_specs[node]['std']

        # Propagate changes through the causal structure
        for node in self.ordered_nodes:
            if node in values:
                continue  # Skip this node because its value is already set by the intervention
            if node not in self.dependency_map:
                continue  # If the node has no parents, there is nothing to propagate

            parents = self.dependency_map[node]
            parent_data = [forward_data[parent] for parent in parents]
            forward_data[node] = self.coefs[node] @ np.stack(
                parent_data, axis=0) + self.noise[node]

        for node in self.ordered_nodes:
            forward_data[node] = forward_data[node] * \
                self.node_specs[node]['std'] + self.node_specs[node]['mean']

        forward_data = pd.DataFrame(forward_data)

        for node in self.nodes:
            lower_bound = self.node_specs[node].get('min', None)
            upper_bound = self.node_specs[node].get('max', None)
            forward_data[node] = np.clip(
                forward_data[node], lower_bound, upper_bound)

        return forward_data
