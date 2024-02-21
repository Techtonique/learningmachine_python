import numpy as np
import sklearn.metrics as skm
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import (
    FloatMatrix,
    FloatVector,
    IntVector,
    FactorVector,
)
from sklearn.base import ClassifierMixin
from .base import Base

base = importr("base")
stats = importr("stats")
utils = importr("utils")


class Classifier(Base, ClassifierMixin):
    """
    Classifier.
    """

    def __init__(self):
        """
        Initialize the model.
        """
        super().__init__()
        self.type_fit = "classification"
        try:
            self.load_learningmachine()
            self.obj = r("learningmachine::Classifier$new()")
        except NotImplementedError as e:
            try:
                r.library("learningmachine")
                self.obj = r("Classifier$new()")
            except NotImplementedError as e:
                try:
                    self.obj = r(
                        """
                                 library(learningmachine); 
                                 Classifier$new()
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
            FactorVector(IntVector(y)),
        )
        self.classes_ = np.unique(y)  # /!\ do not remove
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
