import learningmachine as lm
import numpy as np
import pandas as pd 

from sklearn.datasets import load_wine, load_iris, load_breast_cancer
from sklearn.model_selection import train_test_split, cross_val_score
from time import time


datasets = [load_wine(), load_iris(), load_breast_cancer()]

print("\n ----- fitting Kernel Ridge Regression ----- \n")   

for dataset in datasets: 

    X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
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
    print(fit_obj.summary(X=X_test, y=y_test,                           
                          class_index=0))
    

print("\n ----- fitting xgboost ----- \n")   

for dataset in datasets: 

    X = pd.DataFrame(dataset.data, columns=dataset.feature_names)
    y = dataset.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                        random_state=123)
    
    fit_obj = lm.Classifier(method = "xgboost", 
                            pi_method="kdesplitconformal",
                            type_prediction_set = 'score',
                            B=100)    

    start = time()
    fit_obj.fit(X_train, y_train, nrounds=100, eta=0.05, max__depth=4, verbose=0)
    print("Elapsed time: ", time() - start)
    print(fit_obj.predict(X_test))
    print(fit_obj.summary(X=X_test, y=y_test, 
                          class_index=1))