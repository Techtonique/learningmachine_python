import learningmachine as lm
import numpy as np

from sklearn.datasets import load_wine, load_iris, load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from time import time


datasets = [load_wine(), load_iris(), load_breast_cancer()]

for dataset in datasets: 

    X = dataset.data
    y = dataset.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=123)
    
    fit_obj = lm.Classifier(method = "krr", 
                            pi_method="none")    

    start = time()
    fit_obj.fit(X_train, y_train, reg_lambda = 0.05)
    print("Elapsed time: ", time() - start)

    print(f"fit_obj.get_params(): {fit_obj.get_params()}")

    print(f"fit_obj.predict(X_test): {fit_obj.predict(X_test)}")

    ## Compute accuracy
    #print(fit_obj.score(X_test, y_test))
    #print(cross_val_score(fit_obj, X, y, cv=5, scoring='accuracy'))
    print(fit_obj.summary(X=X_test, y=y_test, class_index=0))

for dataset in datasets: 

    X = dataset.data
    y = dataset.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=123)
    
    fit_obj = lm.Classifier(method = "ranger", 
                            pi_method="kdesplitconformal",
                            type_prediction_set = 'score',
                            B=100)    

    start = time()
    fit_obj.fit(X_train, y_train, num__trees = 150)
    print("Elapsed time: ", time() - start)
    print(fit_obj.predict(X_test))
    print(fit_obj.summary(X=X_test, y=y_test, class_index=0))