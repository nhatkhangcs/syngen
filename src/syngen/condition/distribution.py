from abc import ABC, abstractmethod
import numpy as np
from typing import Iterable
from .base import BaseCondition


class Distribution(BaseCondition, ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def __call__(self, n_samples: int) -> np.ndarray:
        pass

    def __str__(self):
        return self.__class__.__name__

class UniformDistribution(Distribution):

    def __init__(self, begin: float, stop: float):
        super().__init__()
        self.begin: float = begin
        self.stop: float = stop

    def __call__(self, n_samples: int) -> np.ndarray:
        return np.random.uniform(self.begin, self.stop, n_samples)


class NormalDistribution(Distribution):

    def __init__(self, mean: float, std: float):
        assert std > 0, ValueError('bla bla')

        super().__init__()
        self.mean = mean
        self.std = std

    def __call__(self, n_samples: int) -> np.ndarray:
        return np.random.normal(self.mean, self.std, n_samples)


class BinomialDistribution(Distribution):

    def __init__(self, n: int, p: float):
        assert 0 <= p <= 1, ValueError('Binomial distribution: p must be between 0 and 1')

        super().__init__()
        self.n = n
        self.p = p

    def __call__(self, n_samples: int, ) -> np.ndarray:
        return np.random.binomial(self.n, self.p, n_samples)


class PoissonDistribution(Distribution):

    def __init__(self, lambda_val: float):
        assert lambda_val >= 0, ValueError('Poisson distribution: x, lambda must be >= 0')

        super().__init__()
        self.lambda_val = lambda_val

    def __call__(self, n_samples: int) -> np.ndarray:
        return np.random.poisson(self.lambda_val, n_samples)


class ExponentialDistribution(Distribution):

    def __init__(self, rate: float):
        assert rate >= 0, ValueError('Exponential distribution: rate must be >= 0')

        super().__init__()
        self.rate = rate

    def __call__(self, n_samples: int) -> np.ndarray:
        return np.random.exponential(self.rate, n_samples)


class CustomDistribution(Distribution):
    def __init__(self, arr: Iterable, weights: Iterable):
        super().__init__()
        self.arr: np.ndarray = np.array(arr)
        self.weights: np.ndarray = np.array(weights)
        w_sum = self.weights.sum()

        assert all((
            len(self.arr) == len(self.weights),
            np.all(self.weights >= 0),
            w_sum > 0,
        )), ValueError()

        self.weights: np.ndarray = self.weights / w_sum

    def __call__(self, n_samples: int) -> np.ndarray:
        return np.random.choice(self.arr, size=n_samples, replace=True, p=self.weights)