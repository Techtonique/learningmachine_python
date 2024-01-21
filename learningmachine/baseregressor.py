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

base = importr("base")
stats = importr("stats")

def BaseRegressor():
    """Base Regressor."""

    res = LEARNINGMACHINE_PACKAGE.BaseRegressor()

    # convert R object to pandas dataframe
    return res
 