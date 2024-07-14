import learningmachine as lm
import numpy as np
import pandas as pd 
from sklearn.datasets import load_diabetes, load_wine
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split, cross_val_score
from rpy2.robjects.vectors import FloatMatrix, FloatVector, StrVector
from time import time
from sklearn.metrics import mean_squared_error
from math import sqrt


# 1. Regression
fit_obj = lm.Regressor(method="ranger")
diabetes = load_diabetes()
X = pd.DataFrame(diabetes.data[:150], columns=diabetes.feature_names)
y = diabetes.target[:150]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=1213)


start = time()
fit_obj.fit(X_train, y_train, num__trees = 500)
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
print(f"fit_obj.predict(X_test): {fit_obj.predict(X_test)}")
print(fit_obj.summary(X=X_test, y=y_test))

fit_obj2 = lm.Regressor(method="krr", pi_method="none")
start = time()
fit_obj2.fit(X_train, y_train, lambda_=0.05)
print("Elapsed time: ", time() - start)
print(fit_obj2.summary(X=X_test, y=y_test))


X, y = fetch_california_housing(return_X_y=True, as_frame=True)
#features = ["MedInc", "AveOccup", "HouseAge", "AveRooms"]
fit_obj3 = lm.Regressor(method="extratrees", B=100, 
                        pi_method="kdesplitconformal")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=1213)
start = time()
fit_obj3.fit(X_train, y_train, num__trees = 100, mtry = 4)
print("Elapsed time: ", time() - start)
print(f"fit_obj3.predict(X_test).lower: {fit_obj3.predict(X_test).lower}")
print(f"fit_obj3.predict(X_test).upper: {fit_obj3.predict(X_test).upper}")
print(fit_obj3.summary(X=X_test, y=y_test))
