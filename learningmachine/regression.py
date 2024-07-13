import numpy as np
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector, ListVector
from sklearn.base import RegressorMixin
from .base import Base
from .utils import format_value, r_list_to_namedtuple

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
        pi_method="none",
        level=95,
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
            name = "Regressor",
            type = "regression",
            method=method,
            pi_method=pi_method,
            level=level,
            B=B,
            nb_hidden=nb_hidden,
            nodes_sim=nodes_sim,
            activ=activ,
            seed=seed,
        )
        
        try: 
            r_obj_command = (
    'suppressWarnings(suppressMessages(library(learningmachine))); '
    'Regressor$new(method = ' + str(format_value(self.method)) + ', '
    'pi_method = ' + str(format_value(self.pi_method)) + ', '
    'level = ' + str(format_value(self.level)) + ', '
    'B = ' + str(format_value(self.B)) + ', '
    'nb_hidden = ' + str(format_value(self.nb_hidden)) + ', '
    'nodes_sim = ' + str(format_value(self.nodes_sim)) + ', '
    'activ = ' + str(format_value(self.activ)) + ', '
    'seed = ' + str(format_value(self.seed)) + ')')
            self.obj = r(r_obj_command)
        except Exception: 
            try:                 
                self.obj = r(f"suppressWarnings(suppressMessages(library(learningmachine))); Regressor$new(method = {format_value(self.method)}, pi_method = {format_value(self.pi_method)}, level = {format_value(self.level)}, B = {format_value(self.B)}, nb_hidden = {format_value(self.nb_hidden)}, nodes_sim = {format_value(self.nodes_sim)}, activ = {format_value(self.activ)}, seed = {format_value(self.seed)})")
            except Exception: 
                self.obj = r(
                    f"learningmachine::Regressor$new(method = {format_value(self.method)}, pi_method = {format_value(self.pi_method)}, level = {format_value(self.level)}, B = {format_value(self.B)}, nb_hidden = {format_value(self.nb_hidden)}, nodes_sim = {format_value(self.nodes_sim)}, activ = {format_value(self.activ)}, seed = {format_value(self.seed)})"
                )
        
    def fit(self, X, y, **kwargs):
        """
        Fit the model according to the given training data.
        """        
        params_dict = {}
        for k, v in kwargs.items():
            params_dict[k.replace('_', '.')] = v
        self.obj["fit"](
            r.matrix(FloatVector(X.ravel()), 
                       byrow=True,
                       ncol=X.shape[1],
                       nrow=X.shape[0]),
            FloatVector(y), 
            **params_dict            
        )
        return self

    def predict(self, X):
        """
        Predict using the model.
        """
        if self.pi_method == "none":
            return(np.asarray(self.obj["predict"](
                r.matrix(FloatVector(X.ravel()), 
                       byrow=True,
                       ncol=X.shape[1],
                       nrow=X.shape[0])
            )))
        return r_list_to_namedtuple(self.obj["predict"](
                r.matrix(FloatVector(X.ravel()), 
                       byrow=True,
                       ncol=X.shape[1],
                       nrow=X.shape[0])
            ))
        
