import numpy as np
import pandas as pd
from .config import (
    LEARNINGMACHINE_PACKAGE,
    FLOATMATRIX,
    FLOATVECTOR,
    STRVECTOR,
    R_NULL,
)

from rpy2.robjects.packages import importr
from rpy2.robjects import conversion, default_converter, pandas2ri, r
from sklearn.base import BaseEstimator, RegressorMixin

base = importr("base")
stats = importr("stats")

class BaseRegressor(BaseEstimator, RegressorMixin):
    """
        Base Regressor.
    """

    def __init__(self,):
        self = LEARNINGMACHINE_PACKAGE.BaseRegressor        
 