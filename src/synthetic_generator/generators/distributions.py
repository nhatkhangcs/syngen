"""
Distribution generators for SynGen.

This module provides generators for various statistical distributions
used in synthetic data generation.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from ..schemas import DataType, DistributionType
from .text_generators import TextGenerator
from .temporal_generators import TemporalGenerator


class DistributionGenerator:
    """Generator for various statistical distributions."""
    
    def __init__(self):
        """Initialize the distribution generator."""
        self.text_generator = TextGenerator()
        self.temporal_generator = TemporalGenerator()
    
    def generate(
        self,
        distribution: DistributionType,
        data_type: DataType,
        parameters: Dict[str, Any],
        n_samples: int
    ) -> np.ndarray:
        """
        Generate data based on the specified distribution.
        
        Args:
            distribution: Type of distribution to use
            data_type: Target data type
            parameters: Distribution parameters
            n_samples: Number of samples to generate
            
        Returns:
            Array of generated values
        """
        
        if distribution == DistributionType.NORMAL:
            return self._generate_normal(parameters, n_samples)
        elif distribution == DistributionType.UNIFORM:
            return self._generate_uniform(parameters, n_samples)
        elif distribution == DistributionType.EXPONENTIAL:
            return self._generate_exponential(parameters, n_samples)
        elif distribution == DistributionType.GAMMA:
            return self._generate_gamma(parameters, n_samples)
        elif distribution == DistributionType.BETA:
            return self._generate_beta(parameters, n_samples)
        elif distribution == DistributionType.WEIBULL:
            return self._generate_weibull(parameters, n_samples)
        elif distribution == DistributionType.POISSON:
            return self._generate_poisson(parameters, n_samples)
        elif distribution == DistributionType.BINOMIAL:
            return self._generate_binomial(parameters, n_samples)
        elif distribution == DistributionType.GEOMETRIC:
            return self._generate_geometric(parameters, n_samples)
        elif distribution == DistributionType.CATEGORICAL:
            return self._generate_categorical(parameters, n_samples)
        elif distribution == DistributionType.CONSTANT:
            return self._generate_constant(parameters, n_samples)
        else:
            raise ValueError(f"Unsupported distribution: {distribution}")
    
    def _generate_normal(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate normal distribution."""
        mean = parameters.get('mean', 0.0)
        std = parameters.get('std', 1.0)
        return np.random.normal(mean, std, n_samples)
    
    def _generate_uniform(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate uniform distribution."""
        low = parameters.get('low', 0.0)
        high = parameters.get('high', 1.0)
        return np.random.uniform(low, high, n_samples)
    
    def _generate_exponential(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate exponential distribution."""
        scale = parameters.get('scale', 1.0)
        return np.random.exponential(scale, n_samples)
    
    def _generate_gamma(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate gamma distribution."""
        shape = parameters.get('shape', 1.0)
        scale = parameters.get('scale', 1.0)
        return np.random.gamma(shape, scale, n_samples)
    
    def _generate_beta(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate beta distribution."""
        a = parameters.get('a', 1.0)
        b = parameters.get('b', 1.0)
        return np.random.beta(a, b, n_samples)
    
    def _generate_weibull(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate Weibull distribution."""
        shape = parameters.get('shape', 1.0)
        scale = parameters.get('scale', 1.0)
        return np.random.weibull(shape, n_samples) * scale
    
    def _generate_poisson(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate Poisson distribution."""
        lam = parameters.get('lam', 1.0)
        return np.random.poisson(lam, n_samples)
    
    def _generate_binomial(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate binomial distribution."""
        n = parameters.get('n', 1)
        p = parameters.get('p', 0.5)
        return np.random.binomial(n, p, n_samples)
    
    def _generate_geometric(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate geometric distribution."""
        p = parameters.get('p', 0.5)
        return np.random.geometric(p, n_samples)
    
    def _generate_categorical(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate categorical distribution."""
        categories = parameters.get('categories', [])
        probabilities = parameters.get('probabilities', None)
        
        if not categories:
            raise ValueError("Categorical distribution requires 'categories' parameter")
        
        if probabilities is None:
            # Equal probabilities
            probabilities = [1.0 / len(categories)] * len(categories)
        
        if len(categories) != len(probabilities):
            raise ValueError("Number of categories must match number of probabilities")
        
        # Normalize probabilities
        probabilities = np.array(probabilities)
        probabilities = probabilities / probabilities.sum()
        
        return np.random.choice(categories, size=n_samples, p=probabilities)
    
    def _generate_constant(self, parameters: Dict[str, Any], n_samples: int) -> np.ndarray:
        """Generate constant values."""
        value = parameters.get('value', 0)
        return np.full(n_samples, value)
    
    def generate_text(
        self,
        data_type: DataType,
        parameters: Dict[str, Any],
        n_samples: int
    ) -> np.ndarray:
        """Generate text data based on type."""
        
        if data_type == DataType.EMAIL:
            return self.text_generator.generate_emails(parameters, n_samples)
        elif data_type == DataType.PHONE:
            return self.text_generator.generate_phones(parameters, n_samples)
        elif data_type == DataType.ADDRESS:
            return self.text_generator.generate_addresses(parameters, n_samples)
        elif data_type == DataType.NAME:
            return self.text_generator.generate_names(parameters, n_samples)
        elif data_type == DataType.STRING:
            return self.text_generator.generate_strings(parameters, n_samples)
        else:
            raise ValueError(f"Unsupported text data type: {data_type}")
    
    def generate_temporal(
        self,
        data_type: DataType,
        parameters: Dict[str, Any],
        n_samples: int
    ) -> np.ndarray:
        """Generate temporal data based on type."""
        
        if data_type == DataType.DATE:
            return self.temporal_generator.generate_dates(parameters, n_samples)
        elif data_type == DataType.DATETIME:
            return self.temporal_generator.generate_datetimes(parameters, n_samples)
        else:
            raise ValueError(f"Unsupported temporal data type: {data_type}") 