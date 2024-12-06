from copy import deepcopy
import networkx as nx
import pandas as pd
import numpy as np
from typing import Any, List, Tuple, Dict

from kairosml.mechanisms import BaseMechanism, MechanismFactory
from kairosml.distributions import BaseDistribution, DistributionFactory
from kairosml.model_query import ModelQuery
from kairosml.model_diagnostics import ModelDiagnostics
import tempfile
import json
import os
import tarfile
import requests
import warnings
from openai import OpenAI


class Model:
    def __init__(self, nodes: List[str], edges: List[Tuple[str, str]], node_types: Dict[str, str] = {}, **kwargs: Any) -> None:
        # Model structure
        self.edges = edges
        self.nodes = nodes
        self._validate_structure()

        # Set any undefined node types to continuous
        self.node_types = self._validate_node_types(node_types)
        self.mechanisms = self._generate_mechanisms(node_types)
        self.distributions = self._generate_distributions(node_types)

        # Data
        self.data = None
        self.node_to_index = None
        self.node_bounds = None
        self._generate_dependency_map()

        # Register submodules
        self.query = ModelQuery(self)
        self.diagnostics = ModelDiagnostics(self)

    def _validate_structure(self) -> None:
        """
        Validate the structure of the model.

        Returns:
            None

        Raises:
            ValueError: if the model structure is invalid
        """
        # Check that the edges are valid
        for edge in self.edges:
            if edge[0] not in self.nodes or edge[1] not in self.nodes:
                raise ValueError(
                    f"Invalid edge in model structure: {edge[0]} -> {edge[1]}.")

        # Check that the model is acyclic
        G = nx.DiGraph(self.edges)
        if not nx.is_directed_acyclic_graph(G):
            raise ValueError("Model structure must be acyclic.")

    def _validate_node_types(self, node_types: Dict[str, str]) -> Dict[str, str]:
        """
        Ensures `node_types` are defined correctly and sets defaults.

        Args:
            node_types (Dict[str, str]): Node types

        Returns:
            Dict[str, str]: Processed node types
        """
        for node in self.nodes:
            if node not in node_types:
                node_types[node] = "continuous"
            elif node_types[node] not in ["continuous", "binary"]:
                raise ValueError(
                    "Node types must be either 'continuous' or 'binary'.")
        return node_types

    def _generate_mechanisms(self, node_types: Dict[str, str]) -> Dict[str, BaseMechanism]:
        """
        Generate the causal mechanisms for each node in the model.

        Args:
            node_types: dict, containing the type of each node in the model

        Returns:
            mechanisms: dict, containing the causal mechanism for each node
        """
        mechanisms = {}
        for node, node_type in node_types.items():
            mechanisms[node] = MechanismFactory.create_mechanism(node_type)
        return mechanisms

    def _generate_distributions(self, node_types: Dict[str, str]) -> Dict[str, Any]:
        """
        Generate the distributions for each node in the model.

        Args:
            node_types: dict, containing the type of each node in the model

        Returns:
            distributions: dict, containing the distribution for each node
        """
        distributions = {}
        for node, node_type in node_types.items():
            distributions[node] = DistributionFactory.create_distribution(
                node_type)
        return distributions

    def _generate_dependency_map(self) -> None:
        """
        Generate the dependency map for the model. This is used to determine the order of evaluation for the model.

        Returns:
            None

        """
        G = nx.DiGraph(self.edges)

        # Do a topological sort
        topo_sorted_nodes = list(nx.topological_sort(G))

        # Create a dictionary that stores the parent nodes for each node
        parents = {}
        for node in topo_sorted_nodes:
            parents[node] = list(G.predecessors(node))

        # Determine the order of evaluation
        evaluation_order = []
        visited = set()
        dependency_map = {}  # Aggregate parents for each node

        for node in topo_sorted_nodes:
            if all(parent in visited for parent in parents[node]):
                dependency_map[node] = parents[node]
                visited.add(node)
                evaluation_order.append(node)

        self.dependency_map = dependency_map

    def _get_downstream_nodes(self, nodes: List[str]) -> List[str]:
        """
        Get all downstream nodes for a given node set.

        Args:
            node: list, containing the nodes to get the children for

        Returns:
            children: list, containing the child nodes for the given node
        """
        G = nx.DiGraph(self.edges)
        children = set()
        for node in nodes:
            children.update(nx.descendants(G, node))
        return list(children)

    def _set_data(self, data: pd.DataFrame) -> None:
        """
        Set the data for the model.

        Args:
            data: pd.DataFrame, the data to set

        Returns:
            None
        """

        # Check that data is a pandas DataFrame and contains all nodes
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Data must be a pandas DataFrame.")

        if not set(self.nodes).issubset(set(data.columns)):
            raise ValueError("Data must contain all nodes in the model.")

        self.data = data
        self.node_to_index = {node: i for i,
                              node in enumerate(self.data.columns)}
        self._set_node_bounds()

    def _set_node_bounds(self) -> None:
        """
        Set the node bounds based on self.data.

        Returns:
            None
        """
        # Set node bounds based on data
        self.node_bounds = {}
        for node in self.nodes:
            if self.node_types[node] == "continuous":
                self.node_bounds[node] = (
                    self.data[node].min(), self.data[node].max())
            elif self.node_types[node] == "binary":
                self.node_bounds[node] = (0, 1)

    def save(self, path: str) -> None:
        """
        Save the model to file as a .tar.gz archive.

        Args:
            path: str, the path to save the model to

        Returns:
            None

        Example:
        ```
        model.save("model.tar.gz")
        ```
        """

        metadata = {
            "nodes": self.nodes,
            "edges": self.edges,
            "node_types": self.node_types,
            "data": self.data.to_dict(orient='list'),
            "node_to_index": self.node_to_index,
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = os.path.join(temp_dir, "meta.json")
            # Save metadata
            with open(filepath, 'w') as f:
                json.dump(metadata, f)

            # Save mechanisms
            os.makedirs(os.path.join(temp_dir, "mechanisms"), exist_ok=True)
            for node, mechanism in self.mechanisms.items():
                mechanism.save(os.path.join(
                    temp_dir, "mechanisms", f"{node}.pkl"))

            # Save distributions
            os.makedirs(os.path.join(temp_dir, "distributions"), exist_ok=True)
            for node, distribution in self.distributions.items():
                distribution.save(os.path.join(
                    temp_dir, "distributions", f"{node}.pkl"))

            # Archive the directory
            with tarfile.open(path, "w:gz") as tar:
                tar.add(filepath, arcname="meta.json")
                tar.add(os.path.join(temp_dir, "mechanisms"),
                        arcname="mechanisms")
                tar.add(os.path.join(temp_dir, "distributions"),
                        arcname="distributions")

    @staticmethod
    def load(path: str) -> 'Model':
        """
        Load a model from a .tar.gz archive. Loading from multiple serialised pkls prevents issues with compatibility from pickling large objects.

        Args:
            path: str, the path to the model archive

        Returns:
            model: Model, the loaded model

        Example:
        ```
        model = Model.load("model.tar.gz")
        ```
        """

        # Create temp directory to extract files
        with tempfile.TemporaryDirectory() as temp_dir:
            tar = tarfile.open(path, "r:gz")
            tar.extractall(temp_dir)

            # Load metadata
            with open(os.path.join(temp_dir, "meta.json"), 'r') as f:
                metadata = json.load(f)

            # Load mechanisms from mechanisms subdirectory
            mechanisms = {}
            for node in metadata["nodes"]:
                mechanisms[node] = MechanismFactory.load_mechanism(
                    os.path.join(temp_dir, "mechanisms", f"{node}.pkl"))

            # Load distributions from distributions subdirectory
            distributions = {}
            for node in metadata["nodes"]:
                distributions[node] = DistributionFactory.load_distribution(
                    os.path.join(temp_dir, "distributions", f"{node}.pkl"))

        # Extract metadata
        nodes = metadata["nodes"]
        edges = metadata["edges"]
        node_types = metadata["node_types"]
        data = pd.DataFrame(metadata["data"])
        node_to_index = metadata["node_to_index"]

        # Convert edges to list of tuples
        edges = [tuple(edge) for edge in edges]

        # Create model
        model = Model(
            nodes=nodes,
            edges=edges,
            node_types=node_types
        )

        # Set mechanisms and distributions
        model.mechanisms = mechanisms
        model.distributions = distributions
        model.data = data
        model.node_to_index = node_to_index
        model._set_node_bounds()

        return model

    def train(self, data: pd.DataFrame) -> None:
        """
        Train the model on the given data.

        Args:
            data: pd.DataFrame, the data to train the model on

        Returns:
            None

        Example:
        ```
        model.train(data)
        ```
        """

        # Set the data and perform checks
        self._set_data(data)

        # Fit the causal mechanisms according to the dependency map
        for outcome_node, input_nodes in self.dependency_map.items():
            if len(input_nodes) == 0:
                # No parents, so fit a distribution instead
                distribution = self.distributions[outcome_node]
                distribution.fit(self.data[outcome_node].values)
                self.distributions[outcome_node] = distribution
            else:
                mechanism = self.mechanisms[outcome_node]
                # Build data from dict
                X = np.array([data[input_node]
                             for input_node in input_nodes]).T
                y = np.array(data[outcome_node])

                mechanism.fit(X, y)
                self.mechanisms[outcome_node] = mechanism

    def forward(self, values: dict, num_samples: int = 1000, return_mean: bool = False, observation_noise: bool = False, normalise: bool = True) -> np.ndarray:
        """Simulate a forward pass through the model. Any nodes not specified in values will be generated from the distribution of the data.

        Args:
            values: dict, containing the values to set for each node
            num_samples: int, the number of samples to generate
            return_mean: bool, whether to return the mean of the samples
            observation_noise: bool, whether to add observation noise to the generated samples

        Returns:
            data_samples: np.ndarray, containing the simulated data samples

        Example:
        ```
        values = {
            "A": 0,
            "B": 1
        }

        data_samples = model.forward(values, num_samples=1000)
        ```
        """
        if return_mean:
            num_samples = 1

        # Calculate the number of rows in the data from the values dict
        if len(values) == 0:
            num_rows = 1
        else:
            num_rows = values[list(values.keys())[0]].shape[0]

        #  Set up a dictionary to store the clipped nodes to avoid sending multiple warnings
        clipped_nodes = {}

        # Get nodes with no parents
        no_parent_nodes = [
            node for node, parents in self.dependency_map.items() if len(parents) == 0]

        # Generate empty dataframe with num_rows
        base_df_dict = {}
        for node in self.node_to_index.keys():
            base_df_dict[node] = np.zeros(num_rows)
        base_df = pd.DataFrame(base_df_dict)

        # Generate num_samples dataframes
        data_samples = [deepcopy(base_df) for _ in range(num_samples)]

        # For each dataframe, update the values with random samples or the specified values
        for data in data_samples:
            for node in self.nodes:
                if node in values:
                    data[node] = values[node]
                elif node in no_parent_nodes:
                    # Set exogenous nodes depending on the forward mode
                    if return_mean:
                        # Return a scalar of the mean
                        data[node] = self.distributions[node].mean()
                    elif observation_noise:
                        # Sample from the distribution
                        data[node] = self.distributions[node].sample(
                            num_rows).flatten()
                    else:
                        # Repeat the mean for each row
                        data[node] = np.repeat(
                            self.distributions[node].mean(), num_rows)

        # Run the forward pass
        for outcome_node, input_nodes in self.dependency_map.items():
            if len(input_nodes) == 0 or outcome_node in values:
                # No parents, so no need to run the mechanism
                continue

            mechanism = self.mechanisms[outcome_node]

            # Vectorise dataframes for speed
            X = np.vstack([np.array([data[input_node]
                          for input_node in input_nodes]).T for data in data_samples])

            if return_mean:
                y_samples = mechanism.predict(
                    X, observation_noise=observation_noise)
            else:
                y_samples = mechanism.sample(
                    X, num_samples=1, observation_noise=observation_noise).flatten()

                # Split y_samples into chunks of size num_rows and assign them to the data samples
                y_samples = np.split(y_samples, num_samples)

            # Assign the y_samples to the data samples
            for i, data in enumerate(data_samples):
                data[outcome_node] = y_samples[i]

                # # Apply bounds to the data samples
                # data[outcome_node] = np.clip(
                #     data[outcome_node], *self.node_bounds[outcome_node])

                # # If the data were clipped, raise a warning
                # if np.any(data[outcome_node] != y_samples[i]):
                #     clipped_nodes[outcome_node] = True

        data_samples = np.array(data_samples)

        # If any nodes were clipped, raise a warning
        # if len(clipped_nodes) > 0:
        #     warnings.warn(
        #         f"The following nodes had values outside the bounds of the training data: {list(clipped_nodes.keys())}. Extrapolation beyond the training bounds is not recommended, so values have been clipped to the training bounds.")

        return data_samples

    @staticmethod
    def from_context(context: str = None, url: str = None, nodes: List[str] = None):
        """
        Generate a causal model from a given context.

        Args:
            context: str, the context to generate the model from
            url: str, the URL to generate the model from
            nodes: list, containing the nodes to include in the model

        Returns:
            model: Model, the generated causal model

        Example:
        ```
        model = Model.from_context(
            "Studies have shown that A causes B", nodes=["A", "B"])
        ```
        """

        if context is None and url is None:
            raise ValueError(
                "Either a context or URL must be provided to generate the model.")

        if context is None:
            context = requests.get(url).text

        system_prompt = f"""
        Your job is to extract causal relationships from the context above to build a causal model.
        Nodes provided by the user (ignore if blank): {nodes}
        The response should be in JSON format. The response should contain two keys: nodes and edges.
        - nodes: Should be a list of strings, where each string is a node in the causal model. If provided by the user, the nodes should be the same as the provided nodes, and not include any additional nodes.
        - edges: Should take the form of a list of pairs, where each pair is a list of two nodes, directed from left to right.
        The edges should reflect causal relationships between nodes/variables.
        A causal relationship between two nodes A and B is defined as A causing B, meaning that changes in A will lead to changes in B.
        Make some inferences about the causal relationships in the text based on general knowledge as well as implications from the text.
        Node names should be unique and should not contain any special characters.
        Unless specific node names are provided, node names should be capitalised and contain spaces between words (e.g., 'Age at Diagnosis').
        The returned JSON should be directly parsable by the json.loads() function in Python.
        Do not wrap the JSON in ```json``` or any other structure.
        """

        client = OpenAI()

        completion = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": context + system_prompt}
            ]
        )

        response_dict = json.loads(completion.choices[0].message.content)
        nodes = response_dict['nodes']
        edges = response_dict['edges']

        model = Model(nodes, edges)
        return model
