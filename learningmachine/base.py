import numpy as np
import pandas as pd
from .config import (
    LEARNINGMACHINE_PACKAGE,
    FLOATMATRIX,
    FLOATVECTOR,
    INTVECTOR,
    FACTORVECTOR,
    STRVECTOR,
    R_NULL,
)

from rpy2.robjects import r
from rpy2.robjects.packages import importr
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin

base = importr("base")
stats = importr("stats")

class BaseRegressor(BaseEstimator, RegressorMixin):
    """
        Base Regressor.
    """

    def __init__(self):
        """
            Initialize the model.
        """
        self.obj = r('''
                 library(learningmachine)
                 learningmachine::BaseRegressor$new()
                 ''')

    def fit(self, X, y):
        """
            Fit the model according to the given training data.
        """    
        X_ = r.matrix(FLOATVECTOR(X), 
                  byrow = True, 
                  nrow = X.shape[0], 
                  ncol = X.shape[1]) 
        self.obj["fit"](X_, FLOATVECTOR(y))        
        return self
    
    def predict(self, X):
        """
            Predict using the model.
        """        
        X_ = r.matrix(FLOATMATRIX(X), 
                  byrow = True, 
                  nrow = X.shape[0], 
                  ncol = X.shape[1]) 
        return self.obj["predict"](X_)
    

class BaseClassifier(BaseEstimator, ClassifierMixin):
    """
        Base Classifier.
    """

    def __init__(self):
        """
            Initialize the model.
        """
        self.obj = r('''
                 library(learningmachine)
                 learningmachine::BaseClassifier$new()
                 ''')

    def fit(self, X, y):
        """
            Fit the model according to the given training data.
        """    
        X_ = r.matrix(FLOATVECTOR(X), 
                  byrow = True, 
                  nrow = X.shape[0], 
                  ncol = X.shape[1])         
        y_ = base.as_factor(INTVECTOR(y))
        self.obj["fit"](X_, y_)        
        return self
    
    def predict(self, X):
        """
            Predict classes using the model.
        """        
        X_ = r.matrix(FLOATMATRIX(X), 
                  byrow = True, 
                  nrow = X.shape[0], 
                  ncol = X.shape[1]) 
        return self.obj["predict"](X_)
    
    def predict_proba(self, X):
        """
            Predict probabilities using the model.
        """        
        X_ = r.matrix(FLOATMATRIX(X), 
                  byrow = True, 
                  nrow = X.shape[0], 
                  ncol = X.shape[1]) 
        return self.obj["predict_proba"](X_)    