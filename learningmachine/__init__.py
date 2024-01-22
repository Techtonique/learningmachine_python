"""Top-level package for learningmachine."""

__author__ = """T. Moudiki"""
__email__ = "thierry.moudiki@gmail.com"
__version__ = "0.2.0"

from .base import Base
from .basemodels import BaseClassifier, BaseRegressor

__all__ = ["Base", "BaseClassifier", "BaseRegressor"]
