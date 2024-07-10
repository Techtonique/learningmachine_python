import learningmachine as lm
import numpy as np

from sklearn.datasets import load_diabetes, load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from rpy2.robjects.vectors import FloatMatrix, FloatVector, StrVector
from time import time
from sklearn.metrics import mean_squared_error
from math import sqrt


# 1. Regression
fit_obj = lm.Regressor(method="ranger", 
                       pi_method="none")
diabetes = load_diabetes()
X = diabetes.data[:150]
y = diabetes.target[:150]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=1213)

start = time()
fit_obj.fit(X_train, y_train, num_trees = 50)
print("Elapsed time: ", time() - start)

print(f"fit_obj.get_params(): {fit_obj.get_params()}")
print(f"fit_obj: {fit_obj}")

preds = fit_obj.predict(X_test)
print(f"preds: {preds}")

## Compute RMSE
rms1 = sqrt(mean_squared_error(y_test, preds))
print(rms1)
print(fit_obj.score(X_test, y_test))
print(-cross_val_score(fit_obj, X, y, cv=5, scoring='neg_root_mean_squared_error'))

fit_obj2 = lm.Regressor(method="extratrees", B=10, 
                        pi_method="kdesplitconformal")
start = time()
fit_obj2.fit(X_train, y_train, num_trees = 25, mtry = 3)
print("Elapsed time: ", time() - start)

print(f"fit_obj.get_params(): {fit_obj2.get_params()}")
print(f"fit_obj: {fit_obj2}")

fit_obj4 = lm.Regressor(method="extratrees", B=10, 
                        pi_method="kdesplitconformal")
start = time()
fit_obj4.fit(X_train, y_train, num_trees = 50, mtry = 4)
print("Elapsed time: ", time() - start)

print(f"fit_obj.get_params(): {fit_obj4.get_params()}")
print(f"fit_obj: {fit_obj4}")

print(fit_obj2.predict(X_test))
print(fit_obj4.predict(X_test))

