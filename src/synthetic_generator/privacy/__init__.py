"""
Privacy features for SynGen.

This module provides privacy-preserving features such as
differential privacy and anonymization.
"""

from .differential_privacy import DifferentialPrivacy
from .anonymization import Anonymizer

__all__ = [
    'DifferentialPrivacy',
    'Anonymizer',
    'apply_privacy_settings'
]

def apply_privacy_settings(schema, privacy_level: str):
    """Apply privacy settings to a schema."""
    if privacy_level == 'differential':
        return DifferentialPrivacy.apply(schema)
    elif privacy_level == 'basic':
        return Anonymizer.apply_basic(schema)
    else:
        return schema 