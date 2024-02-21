import learningmachine as lm
import numpy as np

from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, cross_val_score
from time import time


fit_obj = lm.Classifier()
dataset = load_wine()
X = dataset.data
y = dataset.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=123)

start = time()
fit_obj.fit(X_train, y_train)
print("Elapsed time: ", time() - start)

print(dir(fit_obj))
print(fit_obj.get_params())
print(fit_obj.type_fit)
print(fit_obj.obj)

## Compute accuracy
preds = fit_obj.predict(X_test)
acc = np.mean(y_test == preds)
print(acc)

print(fit_obj.score(X_test, y_test))

print(cross_val_score(fit_obj, X, y, cv=5, scoring='accuracy'))