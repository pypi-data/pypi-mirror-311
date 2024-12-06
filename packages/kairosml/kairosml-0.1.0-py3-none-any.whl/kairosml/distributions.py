import numpy as np
import dill
from scipy.stats import gaussian_kde
from typing import Any


class BaseDistribution:
    def __init__(self) -> None:
        """
        Initializes a base distribution.

        Args:
            None
        """


class ContinuousDistribution(BaseDistribution):
    def __init__(self) -> None:
        """
        Initializes a continuous distribution using Gaussian KDE.

        Args:
            None
        """
        self.model = None

    def save(self, path: str) -> None:
        """
        Saves the distribution to a file.

        Args:
            path (str): File path.

        Returns:
            None
        """
        payload = {
            "model": self.model,
            "class": self.__class__
        }
        with open(path, 'wb') as f:
            dill.dump(payload, f)

    @staticmethod
    def load(path: str):
        """
        Loads a distribution from a file.

        Args:
            path (str): File path.

        Returns:
            ContinuousDistribution: Distribution object.
        """
        with open(path, 'rb') as f:
            payload = dill.load(f)

        model = payload["model"]
        instance = ContinuousDistribution()
        instance.model = model
        return instance

    def fit(self, X: np.ndarray) -> None:
        """
        Fits a continuous distribution to data.

        Args:
            X (np.ndarray): Input features.

        Returns:
            None
        """
        self.model = gaussian_kde(X)

    def sample(self, num_samples: int) -> np.ndarray:
        """
        Samples from the continuous distribution.

        Args:
            num_samples (int): Number of samples to draw.

        Returns:
            np.ndarray: Samples from the continuous distribution.
        """
        return self.model.resample(num_samples)

    def mean(self) -> np.ndarray:
        """
        Returns the mean of the distribution.

        Args:
            None

        Returns:
            np.ndarray: Mean of the distribution.
        """
        return self.model.dataset.mean()


class BinaryDistribution(BaseDistribution):
    def __init__(self) -> None:
        """
        Initializes a binary distribution.

        Args:
            None
        """
        self.prob = None

    def save(self, path: str) -> None:
        """
        Saves the distribution to a file.

        Args:
            path (str): File path.

        Returns:
            None
        """
        payload = {
            "prob": self.prob,
            "class": self.__class__
        }
        with open(path, 'wb') as f:
            dill.dump(payload, f)

    @staticmethod
    def load(path: str):
        """
        Loads a distribution from a file.

        Args:
            path (str): File path.

        Returns:
            BinaryDistribution: Distribution object.
        """
        with open(path, 'rb') as f:
            payload = dill.load(f)
        prob = payload["prob"]
        instance = BinaryDistribution()
        instance.prob = prob
        return instance

    def fit(self, X: np.ndarray) -> None:
        """
        Fits a binary distribution to data.

        Args:
            X (np.ndarray): Input features.

        Returns:
            None
        """
        self.prob = np.mean(X)

    def sample(self, num_samples: int) -> np.ndarray:
        """
        Samples from the binary distribution.

        Args:
            num_samples (int): Number of samples to draw.

        Returns:
            np.ndarray: Samples from the binary distribution.
        """
        return np.random.binomial(1, self.prob, num_samples)

    def mean(self) -> np.ndarray:
        """
        Returns the mean of the distribution.

        Args:
            None

        Returns:
            np.ndarray: Mean of the distribution.
        """
        return self.prob


class DistributionFactory:
    @staticmethod
    def create_distribution(distribution_type: str) -> Any:
        if distribution_type == "continuous":
            return ContinuousDistribution()
        elif distribution_type == "binary":
            return BinaryDistribution()
        else:
            raise ValueError("Invalid distribution type.")

    @staticmethod
    def load_distribution(path: str) -> Any:
        with open(path, 'rb') as f:
            payload = dill.load(f)
        distribution_type = payload["class"]
        return distribution_type.load(path)
