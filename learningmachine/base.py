import subprocess
from rpy2.robjects import r
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatMatrix, FloatVector, IntVector, FactorVector
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
        try: 
            r("utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'))")
        except Exception as e1:
            try: 
                r("utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.')")
            except Exception as e2:
                try: 
                    subprocess.run(['Rscript', '-e', "utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'))"])
                except Exception as e3:
                    subprocess.run(['Rscript', '-e', "utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.')"])

        self.obj = r("library(learningmachine); learningmachine::BaseRegressor$new()")

    def fit(self, X, y):
        """
            Fit the model according to the given training data.
        """    
        X_ = r.matrix(FloatVector(X), 
                  byrow = True, 
                  nrow = X.shape[0], 
                  ncol = X.shape[1]) 
        self.obj["fit"](X_, FloatVector(y))        
        return self
    
    def predict(self, X):
        """
            Predict using the model.
        """        
        X_ = r.matrix(FloatMatrix(X), 
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
        try: 
            r("utils.install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'))")
        except Exception as e1:
            try: 
                r("utils.install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.')")
            except Exception as e2:
                try: 
                    subprocess.run(['Rscript', '-e', "utils.install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'))"])
                except Exception as e3:
                    subprocess.run(['Rscript', '-e', "utils.install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.')"])

        self.obj = r("library(learningmachine); learningmachine::BaseClassifier$new()")

    def fit(self, X, y):
        """
            Fit the model according to the given training data.
        """    
        X_ = r.matrix(FloatMatrix(X), 
                  byrow = True, 
                  nrow = X.shape[0], 
                  ncol = X.shape[1])         
        y_ = base.as_factor(IntVector(y))
        self.obj["fit"](X_, y_)        
        return self
    
    def predict(self, X):
        """
            Predict classes using the model.
        """        
        X_ = r.matrix(FloatMatrix(X), 
                  byrow = True, 
                  nrow = X.shape[0], 
                  ncol = X.shape[1]) 
        return self.obj["predict"](X_)
    
    def predict_proba(self, X):
        """
            Predict probabilities using the model.
        """        
        X_ = r.matrix(FloatMatrix(X), 
                  byrow = True, 
                  nrow = X.shape[0], 
                  ncol = X.shape[1]) 
        return self.obj["predict_proba"](X_)    