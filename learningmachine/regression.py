import numpy as np
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatMatrix, FloatVector
from sklearn.base import RegressorMixin
from .base import Base

base = importr("base")
stats = importr("stats")
utils = importr("utils")


class Regressor(Base, RegressorMixin):
    """
    Regressor.
    """

    def __init__(self):
        """
        Initialize the model.
        """
        super().__init__()
        self.type_fit = "regression"
        try:
            self.load_learningmachine()
            self.obj = r("learningmachine::Regressor$new()")
        except NotImplementedError as e:
            try:
                r.library("learningmachine")
                self.obj = r("Regressor$new()")
            except NotImplementedError as e:
                try:
                    self.obj = r(
                        """
                                 library(learningmachine); 
                                 Regressor$new()
                                 """
                    )
                except NotImplementedError as e:
                    print("R package can't be loaded: ", e)

    def fit(self, X, y):
        """
        Fit the model according to the given training data.
        """
        self.obj["fit"](
            r.matrix(
                FloatVector(X), byrow=True, nrow=X.shape[0], ncol=X.shape[1]
            ),
            FloatVector(y),
        )
        return self

    def predict(self, X):
        """
        Predict using the model.
        """
        return np.asarray(
            self.obj["predict"](
                r.matrix(
                    FloatMatrix(X), byrow=True, nrow=X.shape[0], ncol=X.shape[1]
                )
            )
        )
