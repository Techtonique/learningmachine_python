import learningmachine as lm
import numpy as np

from sklearn.datasets import load_diabetes, load_wine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from rpy2.robjects.vectors import FloatMatrix, FloatVector, StrVector
from rpy2.robjects import pandas2ri, r
from time import time


fit_obj = lm.BaseClassifier()
dataset = load_wine()
X = dataset.data
y = dataset.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=1213)

start = time()
fit_obj.fit(X_train, y_train)
print("Elapsed time: ", time() - start)

## Compute accuracy

preds = fit_obj.predict(X_test)
acc = np.mean(y_test == preds)
print(acc)
