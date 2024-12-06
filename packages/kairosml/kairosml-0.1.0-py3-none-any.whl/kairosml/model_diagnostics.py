import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


class ModelDiagnostics:
    """Class for diagnosing the model fit and structure.

    Args:
        model (CausalModel): The fitted causal model.
    """

    def __init__(self, model):
        self.model = model

    def plot(self):
        G = nx.DiGraph(self.model.edges)
        pos = nx.layout.circular_layout(G)
        nx.draw(
            G,
            pos=pos,
            arrows=True,
            with_labels=True,
            node_size=1500,
            node_color="#D6D6D6"
        )

    def loglikelihood(self) -> float:
        """Returns log-likelihood of the model on the training data.

        Args:
            None

        Returns:
            loglikelihood: float, the log-likelihood of the model

        Example:
        ```
        loglikelihood = model.loglikelihood()
        ```

        """

        # Calculate the log-likelihood of the model as the sum of the log-likelihoods of each mechanism
        loglikelihood = 0
        for node, mechanism in self.model.mechanisms.items():
            if mechanism.model is not None:
                loglikelihood += mechanism.loglik()

        return loglikelihood

    def summary(self):
        summary_dict = []
        for node, mechanism in self.mechanisms.items():
            summary_dict.append({
                "node": node,
                "coefficients": mechanism.summary().tolist()
            })
        return pd.DataFrame.from_dict(summary_dict)

    def plot_causal_mechanisms(self):
        """
        Plot the causal mechanisms of the model for each directed edge.

        Returns:
            None
        """
        import numpy as np

        for output_node in self.model.dependency_map.keys():
            for input_node in self.model.dependency_map[output_node]:
                input_scan = np.linspace(
                    self.model.data[input_node].min(), self.model.data[input_node].max(), 100)
                # Set other input nodes to their mean
                scan_data = self.model.data[self.model.dependency_map[output_node]
                                            ].mean().to_dict()
                # Set the input node to the scan across its range
                scan_data[input_node] = input_scan
                scan_data = pd.DataFrame(scan_data)
                output_values = self.model.mechanisms[output_node].predict(scan_data.values)[
                    0]

                plt.plot(input_scan, output_values)
                plt.title(f"{input_node} -> {output_node}")
                plt.xlabel(input_node)
                plt.ylabel(output_node)
                plt.show()
