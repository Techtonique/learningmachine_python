import learningmachine as lm
import numpy as np

from sklearn.datasets import load_diabetes, load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from rpy2.robjects.vectors import FloatMatrix, FloatVector, StrVector
from time import time
from sklearn.metrics import mean_squared_error
from math import sqrt


# 1. Regression
fit_obj = lm.Regressor()
diabetes = load_diabetes()
X = diabetes.data[:150]
y = diabetes.target[:150]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=1213)

start = time()
fit_obj.fit(X_train, y_train)
print("Elapsed time: ", time() - start)

print(dir(fit_obj))
print(fit_obj.get_params())
print(fit_obj.type_fit)
print(fit_obj.obj)


## Compute RMSE
rms1 = sqrt(mean_squared_error(y_test, fit_obj.predict(X_test)))
print(rms1)

print(np.sqrt(fit_obj.score(X_test, y_test)))

print(np.sqrt(-cross_val_score(fit_obj, X, y, cv=5, scoring='neg_mean_squared_error')))