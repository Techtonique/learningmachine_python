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
        super().__init__()
        self.type_fit = None
        self.obj = None

    # def get_params(self, deep=True):
    #     """Get object attributes.

    #     Returns
    #     -------
    #     params : mapping of string to any
    #         Parameter names mapped to their values.
    #     """
    #     out = dict()
    #     param_names = dir(self)
    #     for key in param_names:
    #         if key.startswith("_") is False:
    #             out[key] = getattr(self, key, None)
    #     return out
