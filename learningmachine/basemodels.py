from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import (
    FloatMatrix,
    FloatVector,
    IntVector,
)

from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin
from .base import Base

base = importr("base")
stats = importr("stats")


class BaseRegressor(Base, BaseEstimator, RegressorMixin):
    """
    Base Regressor.
    """

    def __init__(self):
        """
        Initialize the model.
        """
        super(Base, self).__init__()        

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
        return self.obj["predict"](
            r.matrix(
                FloatMatrix(X), byrow=True, nrow=X.shape[0], ncol=X.shape[1]
            )
        )


class BaseClassifier(Base, BaseEstimator, ClassifierMixin):
    """
    Base Classifier.
    """

    def __init__(self):
        """
        Initialize the model.
        """
        super(Base, self).__init__()

    def fit(self, X, y):
        """
        Fit the model according to the given training data.
        """
        self.obj["fit"](
            r.matrix(
                FloatMatrix(X), byrow=True, nrow=X.shape[0], ncol=X.shape[1]
            ),
            base.as_factor(IntVector(y)),
        )
        return self

    def predict(self, X):
        """
        Predict classes using the model.
        """
        return self.obj["predict"](
            r.matrix(
                FloatMatrix(X), byrow=True, nrow=X.shape[0], ncol=X.shape[1]
            )
        )

    def predict_proba(self, X):
        """
        Predict probabilities using the model.
        """
        return self.obj["predict_proba"](
            r.matrix(
                FloatMatrix(X), byrow=True, nrow=X.shape[0], ncol=X.shape[1]
            )
        )
