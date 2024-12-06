import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from scipy.stats.qmc import Sobol
from sklearn.metrics import pairwise_distances
from typing import List, Union
import warnings


class ModelQuery:
    def __init__(self, model):
        self.model = model

    def causal_effects(
        self,
        actions: Union[str, dict[str, tuple[np.ndarray, np.ndarray]]],
        fixed: dict[str, np.ndarray] = None,
        interval: float = 0.90,
        observation_noise=False,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Calculate the causal effects of the model. Equivalent to the ATE/ACE or CATE/CACE depending on whether or not fixed is empty.

        Args:
            actions: dict, containing the actions to simulate
            fixed: dict, containing the values of the nodes to fix
            interval: float, the credible interval around the outcome
            kwargs: additional keyword arguments to pass to the model's forward method

        Returns:
            pd.DataFrame: the causal effect of the model
        """
        if isinstance(actions, str):
            # actions = {actions: np.array([0, 1])}
            mu = self.model.data[actions].mean()
            sigma = self.model.data[actions].std()
            actions = {actions: (mu - 0.5 * sigma, mu + 0.5 * sigma)}

        # Check that actions and fixed are dictionaries
        if not isinstance(actions, dict):
            raise TypeError("Actions must be a string or dictionary.")

        if not isinstance(fixed, dict) and fixed is not None:
            raise TypeError("Fixed must be a dictionary.")

        # Convert all values to numpy arrays
        actions = {k: np.array(v) for k, v in actions.items()}
        if fixed is not None:
            fixed = {k: np.array(v) for k, v in fixed.items()}
        else:
            fixed = {}

        # If action and value are not the same length, check that fixed is a single value
        actions_shapes = [v.shape for v in actions.values()]
        if fixed is not None:
            fixed_shapes = [v.shape for v in fixed.values()]
        else:
            fixed_shapes = []

        if len(set(actions_shapes)) > 1:
            raise ValueError("Action values must have the same length.")

        if len(set(fixed_shapes)) > 1:
            raise ValueError("Fixed values must have the same length.")

        # Get the shape of the action and fixed
        actions_shape = actions_shapes[0]

        if len(fixed_shapes) == 0:
            fixed_shape = (1,)
        else:
            fixed_shape = fixed_shapes[0]

        if actions_shape[0] != fixed_shape[0]:
            if fixed_shape[0] != 1:
                raise ValueError(
                    "Fixed must be a single value or the same length as action."
                )
            fixed = {k: np.repeat(v, actions_shape[0]) for k, v in fixed.items()}

        values = {**actions, **fixed}
        outcome = self.model.forward(
            values, observation_noise=observation_noise, **kwargs
        )

        effect = outcome[:, 1, :] - outcome[:, 0, :]

        effect_quantiles = np.quantile(
            effect, [0.5, (1 - interval) / 2, 1 - (1 - interval) / 2], axis=0
        )

        effect_df = pd.DataFrame(
            effect_quantiles.T,
            columns=["median", "lower", "upper"],
            index=self.model.node_to_index.keys(),
        )

        # # # Filter outputs by the downstream nodes of action set
        # downstream_nodes = self.model._get_downstream_nodes(
        #     list(actions.keys()))
        # effect_df = effect_df.loc[downstream_nodes]

        return effect_df

    def simulate_actions(
        self,
        actions: dict[str, Union[np.ndarray, float]],
        fixed: dict[str, Union[np.ndarray, float]] = {},
        interval: float = 0.90,
        observation_noise: bool = False,
        **kwargs,
    ) -> dict[str, pd.DataFrame]:
        """
        Simulate the outcome of a set of actions. A wrapper for the model's forward method.

        Args:
            action: dict, containing the action to simulate
            fixed: dict, containing the values of the nodes to fix
            interval: float, the credible interval around the outcome
            observation_noise: bool, whether to include observation noise
            kwargs: additional keyword arguments to pass to the model's forward method

        Returns:
            pd.DataFrame: the outcome of the action
            pd.DataFrame: the lower bound of the outcome
            pd.DataFrame: the upper bound of the outcome

        Example:
        ```
        action = {"A": np.array([0, 1])}
        fixed = {"B": np.array([0.5, 0.5])}

        outcome, lower, upper = model.query.simulate_action(action, fixed)
        ```
        """

        if not isinstance(actions, dict):
            raise TypeError("Action must be a dictionary.")

        if not isinstance(fixed, dict):
            raise TypeError("Fixed must be a dictionary.")

        # Convert all values to numpy arrays
        actions = {
            k: np.array([v]) if not isinstance(v, np.ndarray) else v
            for k, v in actions.items()
        }

        fixed = {
            k: np.array([v]) if not isinstance(v, np.ndarray) else v
            for k, v in fixed.items()
        }

        # If action and value are not the same length, check that fixed is a single value
        actions_shapes = [v.shape for v in actions.values()]
        fixed_shapes = [v.shape for v in fixed.values()]

        if len(set(actions_shapes)) > 1:
            raise ValueError("Action values must have the same length.")

        if len(set(fixed_shapes)) > 1:
            raise ValueError("Fixed values must have the same length.")

        # Get the shape of the action and fixed
        actions_shape = actions_shapes[0]

        if len(fixed_shapes) == 0:
            fixed_shape = (1,)
        else:
            fixed_shape = fixed_shapes[0]

        if actions_shape[0] != fixed_shape[0]:
            if fixed_shape[0] != 1:
                raise ValueError(
                    "Fixed must be a single value or the same length as action."
                )
            fixed = {k: np.repeat(v, actions_shape[0]) for k, v in fixed.items()}

        # Simulate the outcome of the action for each entry in the action

        values = {**actions, **fixed}
        forward_samples = self.model.forward(
            values, observation_noise=observation_noise, **kwargs
        )

        # Calculate the mean, lower and upper bounds of the outcome
        outcome = np.mean(forward_samples, axis=0)
        lower = np.quantile(forward_samples, (1 - interval) / 2, axis=0)
        upper = np.quantile(forward_samples, (1 + interval) / 2, axis=0)

        # Convert to pandas DataFrame
        outcome = pd.DataFrame(outcome, columns=self.model.node_to_index.keys())
        lower = pd.DataFrame(lower, columns=self.model.node_to_index.keys())
        upper = pd.DataFrame(upper, columns=self.model.node_to_index.keys())

        # Filter outputs by the downstream nodes of action set
        # downstream_nodes = self.model._get_downstream_nodes(
        #     list(actions.keys()))
        # outcome = outcome[downstream_nodes]
        # lower = lower[downstream_nodes]
        # upper = upper[downstream_nodes]

        response = {"median": outcome, "lower": lower, "upper": upper}

        return response

    def _find_best_action_single(
        self,
        targets: dict[str, float],
        actionable: List[str],
        fixed: dict[str, np.ndarray] = {},
        constraints: dict[str, tuple] = {},
        target_importance: dict[str, float] = {},
    ) -> pd.DataFrame:
        """
        Private method to find the best action to achieve a desired outcome for a single row of data.

        Args:
            target: dict, containing the target outcome for each node
            actionable: list, containing the nodes that can be intervened on
            fixed: dict, containing the values of the nodes to fix
            constraints: dict, containing the constraints on the actionable nodes
            target_importance: dict, containing the importance of each target, if more than one target is specified

        Returns:
            dict: containing the optimal action for each actionable node
        """
        # Check that there are no nodes in both actionable and fixed
        if len(set(actionable).intersection(set(fixed.keys()))) > 0:
            raise ValueError("Actionable nodes and fixed nodes cannot overlap.")

        # Merge constraints with self.model.node_bounds. Constraints take precedence.
        constraints = {**self.model.node_bounds, **constraints}

        # If any of the targets are "minimum" or "maximum", replace with the minimum or maximum value of the data.
        for k, v in targets.items():
            if v == "minimise":
                targets[k] = self.model.data[k].min()
            elif v == "maximise":
                targets[k] = self.model.data[k].max()

        # Convert all values to numpy arrays
        fixed = {
            k: np.array([v]) if not isinstance(v, np.ndarray) else v
            for k, v in fixed.items()
        }
        targets = {
            k: np.array([v]) if not isinstance(v, np.ndarray) else v
            for k, v in targets.items()
        }

        # If fixed is not the same length as the target, check that fixed is a single value
        fixed_shapes = [v.shape for v in fixed.values()]
        targets_shapes = [v.shape for v in targets.values()]

        if len(set(fixed_shapes)) > 1:
            raise ValueError("Fixed values must have the same length.")

        if len(set(targets_shapes)) > 1:
            raise ValueError("Target values must have the same length.")

        # Define the loss function
        def loss(x):
            action = {actionable[i]: np.array([x[i]]) for i in range(len(actionable))}
            values = {**action, **fixed}

            outcome = self.model.forward(values, return_mean=True)

            penalty = 1

            # If any constraints in outcome are violated, apply a large penalty
            for k, v in constraints.items():
                if (
                    v[0] is not None
                    and v[0] > outcome[:, :, self.model.node_to_index[k]]
                ):
                    penalty = 1e6  # Make penalty proportional to the difference
                if (
                    v[1] is not None
                    and v[1] < outcome[:, :, self.model.node_to_index[k]]
                ):
                    penalty = 1e6  # Make penalty proportional to the difference

            # Normalise targets by dividing by the standard deviation
            targets_norm = {k: v / self.model.data[k].std() for k, v in targets.items()}

            outcome_norm = {
                k: outcome[:, 0, self.model.node_to_index[k]] / self.model.data[k].std()
                for k in targets.keys()
            }

            # Calculate the weighted mean squared error
            squared_errors = np.array(
                [(targets_norm[k] - outcome_norm[k]) ** 2 for k in targets.keys()]
            ).flatten()

            weights = np.array(
                [target_importance.get(k, 1) for k in targets.keys()]
            ).flatten()

            wmse = np.average(squared_errors, weights=weights)

            return penalty * wmse

        # Set initial values for the actionable nodes to the mean of the data
        initial_values = [self.model.data[action].mean() for action in actionable]

        # Optimize the loss function
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            res = scipy.optimize.minimize(loss, initial_values, method="Nelder-Mead")

        if not res.success:
            print(res.message)

        # Return the optimal treatment values
        optimal_action = {actionable[i]: res.x[i] for i in range(len(actionable))}

        optimal_action = pd.DataFrame.from_dict(optimal_action, orient="index").T

        return optimal_action

    def find_best_actions(
        self,
        targets: dict[str, float],
        actionable: List[str],
        fixed: dict[str, np.ndarray] = {},
        constraints: dict[str, tuple] = {},
        data: pd.DataFrame = None,
        target_importance: dict[str, float] = {},
    ) -> pd.DataFrame:
        """
        Find the best action to achieve a desired outcome.

        Args:
            targets: dict, containing the target outcome for each node
            actionable: list, containing the nodes that can be intervened on
            fixed: dict, containing the values of the nodes to fix
            constraints: dict, containing the constraints on the actionable nodes
            data: pd.DataFrame, containing the data to find the best action for
            target_importance: dict, containing the importance of each target, if more than one target is specified

        Returns:
            dict: containing the optimal action for each actionable node

        Example:
        ```
        best_action = model.query.find_best_actions(
            targets={"w": 2},
            actionable=["x"],
        )
        ```
        """

        if data is None:
            optimal_action = self._find_best_action_single(
                targets, actionable, fixed, constraints, target_importance
            )
            return optimal_action
        else:
            # Set fixed to be only nodes upstream of actionable unless specified otherwise
            if len(fixed) == 0:
                G = nx.DiGraph()
                G.add_edges_from(self.model.edges)

                upstream_nodes = {}
                for node in actionable:
                    upstream_nodes[node] = nx.ancestors(G, node)
                fixed = list(set.intersection(*upstream_nodes.values()))

            optimal_actions = []
            for row in data.to_dict(orient="records"):
                fixed_values = {k: row[k] for k in fixed}
                optimal_action = self._find_best_action_single(
                    targets,
                    actionable,
                    fixed=fixed_values,
                    constraints=constraints,
                    target_importance=target_importance,
                )
                optimal_actions.append(optimal_action)
            return pd.concat(optimal_actions, ignore_index=True)

    def causal_attributions(
        self, outcome: str, normalise: bool = False, epsilon: float = 0.001
    ) -> pd.DataFrame:
        """
        Calculate the causal attributions of each node.

        Args:
            outcome: str, the node to calculate the causal attribution for
            normalise: bool, whether to normalise the causal attribution
            epsilon: float, the size of the perturbation

        Returns:
            pd.DataFrame: containing the causal attribution of each node

        Example:
        ```
        causal_attributions = model.query.causal_attributions("A")
        ```
        """
        # Loop through each node and calculate the causal attribution
        causal_attributions = {}
        for node in self.model.nodes:
            # Establish the baseline
            baseline_data = self.model.forward(
                {}, return_mean=True
            )  # .squeeze().mean(axis=0)

            epsilon = self.model.data[node].std()

            # Intervene on the node (wiggle the node by epsilon * std)
            wiggle = {
                node: baseline_data[:, :, self.model.node_to_index[node]].flatten()
                + epsilon
            }
            intervened_data = self.model.forward(wiggle, return_mean=True)

            baseline_effect = baseline_data[
                :, :, self.model.node_to_index[outcome]
            ].flatten()
            intervened_effect = intervened_data[
                :, :, self.model.node_to_index[outcome]
            ].flatten()

            if normalise:
                causal_attributions[node] = abs(intervened_effect - baseline_effect)
            else:
                causal_attributions[node] = (
                    intervened_effect - baseline_effect
                ) / self.model.data[outcome].std()

            if node == outcome:
                causal_attributions[node] = 0

        # Normalize by the total change
        if normalise:
            total_change = sum(causal_attributions.values())
            for node in causal_attributions:
                causal_attributions[node] /= total_change

        # Remove outcome node
        del causal_attributions[outcome]

        causal_attributions_df = pd.DataFrame.from_dict(
            causal_attributions, orient="index"
        )
        causal_attributions_df.columns = [outcome]
        return causal_attributions_df

    def plot_causal_attributions(
        self,
        outcome: str,
        normalise: bool = False,
        epsilon: float = 0.1,
        ax=None,
        **kwargs,
    ):
        """
        Plot the causal attribution of each node.

        Args:
            outcome: str, the node to calculate the causal attribution for
            normalise: bool, whether to normalise the causal attribution
            epsilon: float, the size of the perturbation
            ax: matplotlib axis, the axis to plot the causal attribution on
            kwargs: additional keyword arguments to pass to the seaborn barplot function

        Returns:
            ax: matplotlib axis, the axis containing the causal attribution plot

        Example:
        ```
        ax = model.query.causal_attribution_plot("A")
        ```
        """
        # Calculate the causal attribution
        causal_attributions = self.causal_attributions(
            outcome, normalise=normalise, epsilon=epsilon
        )

        # Plot the causal attribution
        if ax is None:
            fig, ax = plt.subplots()

        # Set bar colors. If normalised, use a single color, else determine based on value.
        if normalise:
            bar_colors = ["#119488"] * len(causal_attributions)
        else:
            bar_colors = (
                causal_attributions.iloc[:, 0]
                .map(lambda x: "#8AB17D" if x > 0 else "#B85450")
                .tolist()
            )

        sns.barplot(
            x=causal_attributions.iloc[:, 0],
            y=causal_attributions.index,
            hue=causal_attributions.index,
            palette=bar_colors,
            ax=ax,
            **kwargs,
        )
        ax.set_title(f"Causal Attribution of {outcome}")
        ax.set_xlabel("Causal Attribution")
        ax.set_ylabel("Node")

        # Loop through the bars and place the text annotation inside or next to the bars
        for bar in ax.patches:
            bar_value = bar.get_width()
            text_x_position = bar.get_x() + bar.get_width()
            if bar_value < 0:  # Adjust text position for negative bars if necessary
                text_x_position = bar.get_x()
            ax.text(
                text_x_position,
                bar.get_y() + bar.get_height() / 2,
                f"{bar_value:.2f}",
                va="center",
                ha="left" if bar_value < 0 else "left",
                color="black",
                fontsize=9,
            )

        return ax

    def next_experiment(self, actionable: list, batch_size: int = 1) -> pd.DataFrame:
        """
        Find the next best experiment to run.

        Args:
            actionable: list, containing the nodes that can be intervened on
            batch_size: int, the number of experiments to run

        Returns:
            dict: containing the next best experiment to run

        Example:
        ```
        next_experiment = model.query.next_experiment(["A", "B"], batch_size=1)
        ```
        """
        # Check actionable nodes are in the model
        if not set(actionable).issubset(set(self.model.nodes)):
            raise ValueError("Actionable nodes must be in the model.")

        # Convert self.data to a numpy array
        current_samples = self.model.data[actionable].values
        new_samples = np.zeros((batch_size, len(actionable)))

        for i in range(batch_size):
            # Get the dimensionality of the data
            d = current_samples.shape[1]

            # Generate Sobol samples
            m = int(np.ceil(np.log2(d) + 10))
            candidate_samples = Sobol(d).random_base2(m)
            bounds_lower = current_samples.min(axis=0)
            bounds_upper = current_samples.max(axis=0)
            candidate_samples = (
                candidate_samples * (bounds_upper - bounds_lower) + bounds_lower
            )

            distances = pairwise_distances(
                candidate_samples, current_samples, metric="l1"
            )
            sample_idx = distances.min(axis=1).argmax()
            new_sample = candidate_samples[sample_idx]

            new_samples[i] = new_sample
            # Add new sample to current samples
            current_samples = np.vstack([current_samples, new_sample])

        # Build dictionary of actionable nodes and their values
        new_sample_dict = dict(zip(actionable, new_samples.T))

        # Convert to pandas DataFrame
        response = pd.DataFrame(new_sample_dict)

        return response
