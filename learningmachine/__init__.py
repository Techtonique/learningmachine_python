"""Top-level package for learningmachine."""

__author__ = """T. Moudiki"""
__email__ = "thierry.moudiki@gmail.com"

from .base import Base
from .basemodels import BaseClassifier, BaseRegressor

__all__ = ["Base", "BaseClassifier", "BaseRegressor"]
