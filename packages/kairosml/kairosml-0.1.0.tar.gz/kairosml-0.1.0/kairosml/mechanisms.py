import numpy as np
import dill
from pygam import LinearGAM, LogisticGAM
from scipy.special import expit, logit
from typing import Any
import warnings


class BaseMechanism:
    def __init__(self) -> None:
        """
        Initializes a base mechanism.

        Args:
            None
        """
        self.model = None

    def save(self, path: str) -> None:
        """
        Saves the mechanism to a file.

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
        Loads a mechanism from a file.

        Args:
            path (str): File path.

        Returns:
            BaseMechanism: Mechanism object.
        """
        with open(path, 'rb') as f:
            payload = dill.load(f)
        instance = payload["class"]()
        instance.model = payload["model"]
        return instance

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Fits a mechanism to the data.

        Args:
            X (np.ndarray): Input features.
            y (np.ndarray): Response variable.

        Returns:
            None
        """
        raise NotImplementedError

    def predict(self, X: np.ndarray, observation_noise: bool = True) -> tuple:
        """
        Predicts the mean and standard deviation of the response variable.

        Args:
            X (np.ndarray): Input features.

        Returns:
            tuple: Mean and standard deviation of the response variable.
        """
        raise NotImplementedError

    def loglik(self) -> float:
        """
        Returns the log-likelihood of the model.

        Args:
            None

        Returns:
            float: Log-likelihood of the model.
        """
        raise NotImplementedError

    def sample(self, X: np.ndarray, num_samples: int = 1000, observation_noise: bool = True) -> np.ndarray:
        """
        Samples from the predictive distribution.

        Args:
            X (np.ndarray): Input features.
            num_samples (int): Number of samples to draw.
            observation_noise (bool): Whether to include observation noise.

        Returns:
            np.ndarray: Samples from the predictive distribution.

        """
        raise NotImplementedError


class ContinuousMechanism(BaseMechanism):
    def __init__(self) -> None:
        """
        Initializes a continuous mechanism.

        Args:
            None
        """
        super().__init__()

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Fits a Generalized Additive Model (GAM) to the data.

        Args:
            X (np.ndarray): Input features.
            y (np.ndarray): Response variable.

        Returns:
            None
        """
        self.model = LinearGAM().gridsearch(X, y, progress=False)

    def predict(self, X: np.ndarray, interval_width: float = 0.95, observation_noise: bool = True) -> tuple:
        """
        Predicts the mean, lower, and upper bounds of the response variable.

        Args:
            X (np.ndarray): Input features.
            interval_width (float): Width of the prediction interval.
            observation_noise (bool): Whether to include observation noise.

        Returns:
            tuple: Mean, lower, and upper bounds of the response variable.

        """
        y_pred = self.model.predict(X)
        if observation_noise:
            y_interval = self.model.prediction_intervals(
                X, width=interval_width)
        else:
            y_interval = self.model.confidence_intervals(
                X, width=interval_width)
        y_lower, y_upper = y_interval[:, 0], y_interval[:, 1]
        return y_pred, y_lower, y_upper

    def sample(self, X: np.ndarray, num_samples: int = 1000, observation_noise: bool = True) -> np.ndarray:
        """
        Samples from the predictive distribution.

        Args:
            X (np.ndarray): Input features.
            num_samples (int): Number of samples to draw.
            observation_noise (bool): Whether to include observation noise.

        Returns:
            np.ndarray: Samples from the predictive distribution.

        """
        y_mean, y_lower, y_upper = self.predict(
            X, interval_width=0.6827, observation_noise=observation_noise)
        y_std = (y_upper - y_lower) / 2

        samples = np.random.normal(
            y_mean, y_std, size=(num_samples, len(y_mean)))
        return samples

    def loglik(self) -> float:
        """
        Returns the log-likelihood of the model on the training data.

        Args:
            None

        Returns:
            float: Log-likelihood of the model.
        """
        return self.model.statistics_['loglikelihood']


class BinaryMechanism(BaseMechanism):
    def __init__(self) -> None:
        """
        Initializes a binary mechanism.

        Args:
            None
        """
        super().__init__()

    def fit(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Fits a Generalized Additive Model (GAM) to the data.

        Args:
            X (np.ndarray): Input features.
            y (np.ndarray): Response variable.

        Returns:
            None
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.model = LogisticGAM().gridsearch(X, y, progress=False)

    def predict(self, X: np.ndarray, interval_width: float = 0.95, observation_noise: bool = True) -> tuple:
        """
        Predicts the mean and lower and upper bounds of the response variable.

        Args:
            X (np.ndarray): Input features.
            interval_width (float): Width of the prediction interval.
            observation_noise (bool): Whether to include observation noise.

        Returns:
            tuple: Mean and lower and upper bounds of the response variable.
        """
        y_pred = self.model.predict_mu(X)
        y_interval = self.model.confidence_intervals(X, width=interval_width)
        y_lower, y_upper = y_interval[:, 0], y_interval[:, 1]

        return y_pred, y_lower, y_upper

    def sample(self, X: np.ndarray, num_samples: int = 1000, observation_noise: bool = True) -> np.ndarray:
        """
        Samples from the predictive distribution.

        Args:
            X (np.ndarray): Input features.
            num_samples (int): Number of samples to draw.

        Returns:
            np.ndarray: Samples from the predictive distribution.

        """

        logit_median = logit(self.model.predict_mu(X))
        logit_ci = logit(self.model.confidence_intervals(X, width=0.6875))
        logit_lower, logit_upper = logit_ci[:, 0], logit_ci[:, 1]
        logit_std = (logit_upper - logit_lower) / 2
        samples = expit(np.random.normal(
            logit_median[:, np.newaxis], logit_std[:, np.newaxis], size=(X.shape[0], num_samples)))

        return samples

    def loglik(self) -> float:
        """
        Returns the log-likelihood of the model.

        Args:
            None

        Returns:
            float: Log-likelihood of the model.
        """
        return self.model.statistics_['loglikelihood']


class MechanismFactory:
    """
    Factory class for creating causal mechanisms.
    """
    _mechanisms = {}

    @staticmethod
    def register_mechanism(key, mechanism):
        MechanismFactory._mechanisms[key] = mechanism

    @staticmethod
    def create_mechanism(key: str, model: Any = None):
        mechanism = MechanismFactory._mechanisms.get(key)
        if not mechanism:
            raise ValueError(f"Mechanism {key} does not exist.")

        if model:
            return mechanism.load(model)
        else:
            return mechanism()

    @staticmethod
    def load_mechanism(path: str):
        with open(path, 'rb') as f:
            payload = dill.load(f)
        mechanism_type = payload["class"]
        return mechanism_type.load(path)


# Register mechanisms. TODO: Move this inside the factory class.
MechanismFactory.register_mechanism(
    'continuous', ContinuousMechanism)
MechanismFactory.register_mechanism(
    'binary', BinaryMechanism)
