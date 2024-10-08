# learningmachine 

![PyPI](https://img.shields.io/pypi/v/learningmachine) [![PyPI - License](https://img.shields.io/pypi/l/learningmachine)](https://github.com/thierrymoudiki/learningmachine/blob/master/LICENSE) [![Downloads](https://pepy.tech/badge/learningmachine)](https://pepy.tech/project/learningmachine) [![Documentation](https://img.shields.io/badge/documentation-is_here-green)](https://techtonique.github.io/learningmachine_python/)


Machine Learning with uncertainty quantification and interpretability.

## Install

If R packages are not installed automatically when running `pip`, [install them manually](https://cloud.r-project.org/).

**Development version**

```bash
!pip install git+https://github.com/Techtonique/learningmachine_python.git --verbose 
```

## Example

See also:
- [this notebook](https://colab.research.google.com/github/Techtonique/learningmachine_python/blob/main/learningmachine/demo/thierrymoudiki_20240401_calib.ipynb)
- [this notebook](https://colab.research.google.com/github/Techtonique/learningmachine_python/blob/main/learningmachine/demo/thierrymoudiki_20240508_calib.ipynb)

```python
import learningmachine as lm
import numpy as np
import pandas as pd 
from sklearn.datasets import load_diabetes, load_wine
from sklearn.datasets import load_wine, load_iris, load_breast_cancer
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from rpy2.robjects.vectors import FloatMatrix, FloatVector, StrVector
from time import time
from sklearn.metrics import mean_squared_error
from math import sqrt


# 1. Regression

diabetes = load_diabetes()
X = pd.DataFrame(diabetes.data[:150], columns=diabetes.feature_names)
y = diabetes.target[:150]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=1213)

print("\n ----- fitting krr ----- \n")   

fit_obj2 = lm.Regressor(method="krr", pi_method="none")
start = time()
fit_obj2.fit(X_train, y_train, lambda_=0.05) # R's `lambda` is renamed as `lambda_` in Python as `lambda` is reserved 
print("Elapsed time: ", time() - start)
print(fit_obj2.summary(X=X_test, y=y_test))

# 2. Classification

datasets = [load_wine(), load_iris(), load_breast_cancer()]

print("\n ----- fitting Kernel Ridge Regression ----- \n")   

for dataset in datasets: 
    
    print(f"Description: {dataset.DESCR}")
    X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    y = dataset.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=123)
    
    fit_obj = lm.Classifier(method = "krr", 
                            pi_method="none")    

    start = time()
    fit_obj.fit(X_train, y_train, reg_lambda = 0.05)
    print("Elapsed time: ", time() - start)

    ## Compute accuracy
    print(fit_obj.summary(X=X_test, y=y_test,                           
                          class_index=0))
    

print("\n ----- fitting xgboost ----- \n")   

for dataset in datasets: 
    
    print(f"Description: {dataset.DESCR}")
    X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    y = dataset.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=123)
    
    fit_obj = lm.Classifier(method = "xgboost", 
                            pi_method="kdesplitconformal",
                            type_prediction_set = 'score',
                            B=100)   
                            
    print("nb_hidden = 0 -----") # no hidden layer
    start = time()
    fit_obj.fit(X_train, y_train, nrounds=100, eta=0.05, max__depth=4, verbose=0) # dot ('.') in R parameters is replaced by '__'
    print("Elapsed time: ", time() - start)
    print(fit_obj.predict(X_test))
    print(fit_obj.summary(X=X_test, y=y_test, 
                          class_index=1)) # specify the class whose probability is of interest
    
    fit_obj = lm.Classifier(method = "xgboost", 
                            pi_method="kdesplitconformal",
                            type_prediction_set = 'score',
                            nb_hidden = 5,
                            B=100) 
                            
    print("nb_hidden = 5 -----") # hidden layer with 5 nodes 
    start = time()
    fit_obj.fit(X_train, y_train, nrounds=100, eta=0.05, max__depth=4, verbose=0) # dot ('.') in R parameters is replaced by '__'
    print("Elapsed time: ", time() - start)
    print(fit_obj.predict(X_test))
    print(fit_obj.summary(X=X_test, y=y_test, 
                          class_index=1)) # specify the class whose probability is of interest
```
