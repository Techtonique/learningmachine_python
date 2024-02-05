import subprocess
from sklearn.base import BaseEstimator
from rpy2.robjects.vectors import StrVector


class Base(BaseEstimator):
    """
    Base class.
    """

    def __init__(self):
        """
        Initialize the model.
        """
        self.type_fit = None
        self.obj = None
