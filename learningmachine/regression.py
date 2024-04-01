import numpy as np
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatMatrix, FloatVector
from sklearn.base import RegressorMixin
from .base import Base
from .utils import format_value

base = importr("base")
stats = importr("stats")
utils = importr("utils")


class Regressor(Base, RegressorMixin):
    """
    Regressor.
    """

    def __init__(
            self,
        method="ranger",
        pi_method=None,
        level=None,
        type_prediction_set="score",
        B=None,
        seed=123,
    ):
        """
        Initialize the model.
        """
        super().__init__(
            method=method,
            pi_method=pi_method,
            level=level,
            type_prediction_set=type_prediction_set,
            B=B,
            seed=seed,
        )
        self.name = "Regressor"
        self.type = "regression"
        self.method = method
        self.pi_method = pi_method
        self.level = level
        self.type_prediction_set = type_prediction_set
        self.B = B
        self.seed = seed

        try:
            self.load_learningmachine()
            self.obj = r(
                f"learningmachine::Regressor$new(method = {format_value(self.method)})"
            )
        except NotImplementedError as e:
            try:
                r.library("learningmachine")
                self.obj = r(
                    f"Regressor$new(method = {format_value(self.method)})"
                )
            except NotImplementedError as e:
                try:
                    self.obj = r(
                        f"""
                                 library(learningmachine); 
                                 Regressor$new(method = {format_value(self.method)})
                                 """
                    )
                except NotImplementedError as e:
                    print("R package can't be loaded: ", e)

    def fit(self, X, y):
        """
        Fit the model according to the given training data.
        """
        self.obj["fit"](
            r.matrix(FloatVector(X.ravel()), 
                       byrow=True,
                       ncol=X.shape[1],
                       nrow=X.shape[0]),
            FloatVector(y),
        )
        return self

    def predict(self, X):
        """
        Predict using the model.
        """
        return np.asarray(
            self.obj["predict"](
                r.matrix(FloatVector(X.ravel()), 
                       byrow=True,
                       ncol=X.shape[1],
                       nrow=X.shape[0])
            )
        )
