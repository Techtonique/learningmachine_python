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
from .utils import format_value

base = importr("base")
stats = importr("stats")
utils = importr("utils")


class Classifier(Base, ClassifierMixin):
    """
    Classifier.
    """

    def __init__(
        self,
        method="ranger",
        pi_method="kdesplitconformal",
        level=95,
        type_prediction_set="score",
        B=100,
        nb_hidden = 0,
        nodes_sim = "sobol",
        activ = "relu",
        seed=123,
    ):
        """
        Initialize the model.
        """
        super().__init__(
            name = "Classifier",
            type = "classification",
            method=method,
            pi_method=pi_method,
            level=level,
            type_prediction_set=type_prediction_set,
            B=B,
            nb_hidden=nb_hidden,
            nodes_sim=nodes_sim,
            activ=activ,
            seed=seed,
        )

        try:
            self.load_learningmachine()
            self.obj = r(
                f"learningmachine::Classifier$new(method = {format_value(self.method)}, pi_method = {format_value(self.pi_method)}, level = {format_value(self.level)}, type_prediction_set = {format_value(self.type_prediction_set)}, B = {format_value(self.B)}, nb_hidden = {format_value(self.nb_hidden)}, nodes_sim = {format_value(self.nodes_sim)}, activ = {format_value(self.activ)}, seed = {format_value(self.seed)})"
            )
        except NotImplementedError as e:
            try:
                r.library("learningmachine")
                self.obj = r(
                    f"Classifier$new(method = {format_value(self.method)}, pi_method = {format_value(self.pi_method)}, level = {format_value(self.level)}, type_prediction_set = {format_value(self.type_prediction_set)}, B = {format_value(self.B)}, nb_hidden = {format_value(self.nb_hidden)}, nodes_sim = {format_value(self.nodes_sim)}, activ = {format_value(self.activ)}, seed = {format_value(self.seed)})"
                )
            except NotImplementedError as e:
                try:
                    self.obj = r(
                        f"""
                                 library(learningmachine); 
                                 Classifier$new(method = {format_value(self.method)}, pi_method = {format_value(self.pi_method)}, level = {format_value(self.level)}, type_prediction_set = {format_value(self.type_prediction_set)}, B = {format_value(self.B)}, nb_hidden = {format_value(self.nb_hidden)}, nodes_sim = {format_value(self.nodes_sim)}, activ = {format_value(self.activ)}, seed = {format_value(self.seed)})
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
            FactorVector(IntVector(y)),
        )
        self.classes_ = np.unique(y)  # /!\ do not remove
        return self
    
    def predict_proba(self, X):
        """
        Predict using the model.
        """    
        if self.level is None:               
            res = self.obj["predict_proba"](
                    r.matrix(FloatVector(X.ravel()), 
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0])
                )
            return np.asarray(res)
        res = self.obj["predict_proba"](
                    r.matrix(FloatVector(X.ravel()), 
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0])
                )
        return np.asarray(res[0])                                    

    def predict(self, X):
        """
        Predict using the model.
        """    
        if self.level is None:               
            return (
            np.asarray(
                self.obj["predict"](
                    r.matrix(FloatVector(X.ravel()), 
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0])
                )
            ) - 1 
        )
        return (
            np.asarray(
                self.obj["predict"](
                    r.matrix(FloatVector(X.ravel()), 
                byrow=True,
                ncol=X.shape[1],
                nrow=X.shape[0])
                )
            )            
        )
