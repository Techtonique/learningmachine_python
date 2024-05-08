# learningmachine 

![PyPI](https://img.shields.io/pypi/v/learningmachine) [![PyPI - License](https://img.shields.io/pypi/l/learningmachine)](https://github.com/thierrymoudiki/learningmachine/blob/master/LICENSE) [![Downloads](https://pepy.tech/badge/learningmachine)](https://pepy.tech/project/learningmachine) 


Machine Learning with uncertainty quantification and interpretability.

## Install

If R packages are not installed automatically when running `pip`, [install it manually](https://cloud.r-project.org/).

**Development version**

```bash
!pip install git+https://github.com/Techtonique/learningmachine_python.git --verbose 
```

**Stable version**

```bash
!pip install learningmachine --verbose
```

## Example

See also:
- [this notebook](https://colab.research.google.com/github/Techtonique/learningmachine_python/blob/main/learningmachine/demo/thierrymoudiki_20240401_calib.ipynb)
- [this notebook](https://colab.research.google.com/github/Techtonique/learningmachine_python/blob/main/learningmachine/demo/thierrymoudiki_20240508_calib.ipynb)

```python
import learningmachine as lm

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from time import time
from sklearn.metrics import mean_squared_error

# Regression (linear)
fit_obj = lm.BaseRegressor()
diabetes = load_diabetes()
X = diabetes.data[:150]
y = diabetes.target[:150]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, 
                                                    random_state=1213)

start = time()
fit_obj.fit(X_train, y_train)
print("Elapsed time: ", time() - start)

## Compute RMSE
rms1 = sqrt(mean_squared_error(y_test, fit_obj.predict(X_test), squared=False))
print(rms1)
```
