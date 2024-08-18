import learningmachine as lm
import pandas as pd 
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from time import time

print("\n ----- fitting rvfl and update ----- \n")   

# 1. Regression
fit_obj = lm.Regressor(method="rvfl", 
                       pi_method = "kdejackknifeplus",
                       nb_hidden = 3)

data = fetch_california_housing()
X, y = data.data[:600], data.target[:600]
X = pd.DataFrame(X, columns=data.feature_names)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=123)


start = time()
fit_obj.fit(X_train, y_train, reg_lambda=1)
print("Elapsed time: ", time() - start)

print(fit_obj.summary(X=X_test, y=y_test))
preds = fit_obj.predict(X_test)
print(f"preds: {preds}")


# update
fit_obj.update(X_test.iloc[0,:], y_test[0])
print(fit_obj.summary(X=X_test.iloc[:-1,:], y=y_test[:-1]))
preds = fit_obj.predict(X_test.iloc[:-1,:])
print(f"preds: {preds}")
