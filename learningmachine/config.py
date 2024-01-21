import pickle
import subprocess
from rpy2.robjects import r
from subprocess import Popen, PIPE

proc = Popen(["which", "R"], stdout=PIPE, stderr=PIPE)
R_IS_INSTALLED = proc.wait() == 0
RPY2_ERROR_MESSAGE = ""

try:
    import rpy2.robjects.packages as rpackages
    from rpy2.robjects.packages import importr
    from rpy2.robjects.vectors import FloatMatrix, FloatVector, StrVector
    from rpy2 import rinterface, robjects
    from rpy2.robjects import r, default_converter, NULL
    from rpy2.rinterface import RRuntimeWarning
    from rpy2.rinterface_lib import callbacks
    from rpy2.rinterface_lib.embedded import RRuntimeError
    import rpy2.robjects.conversion as cv
except ImportError as e:
    RPY2_ERROR_MESSAGE = str(e)
    RPY2_IS_INSTALLED = False
else:
    RPY2_IS_INSTALLED = True

USAGE_MESSAGE = """
This Python class is based on R package 'learningmachine' (https://techtonique.github.io/learningmachine/). 
You need to install R (https://www.r-project.org/) and rpy2 (https://pypi.org/project/rpy2/).

Then, install R package 'learningmachine' (if necessary): 
>> RScript -e 'install.packages("learningmachine", repos = https://techtonique.r-universe.dev)'    
"""

r["options"](warn=-1)


def _none2null(none_obj):
    return r("NULL")


none_converter = cv.Converter("None converter")
none_converter.py2rpy.register(type(None), _none2null)

required_packages = ["learningmachine", "bcn"]  # list of required R packages

packages_to_install = [
    x for x in required_packages if not rpackages.isinstalled(x)
]

base = importr("base")
utils = importr("utils")
graphics = importr("graphics")

print(f" required_packages: {required_packages} \n")
# print(f" packages_to_install: {packages_to_install} \n")
# print(f" len(packages_to_install): {len(packages_to_install)} \n")

if len(packages_to_install) > 0:
    subprocess.check_call(
        [
            "RScript",
            "-e",
            f'install.packages({", ".join([f"{x}" for x in packages_to_install])}, repos = "https://techtonique.r-universe.dev", dependencies = TRUE)',
        ]
    )

# check R version
print(f" R version of 'learningmachine' installed: {utils.packageVersion('learningmachine')}")

FLOATMATRIX = FloatMatrix
FLOATVECTOR = FloatVector
STRVECTOR = StrVector
LEARNINGMACHINE_PACKAGE = importr("learningmachine")
CHECK_PACKAGES = True
DEEP_COPY = lambda x: pickle.loads(pickle.dumps(x, -1))
NONE_CONVERTER = none_converter
PLOT_BASE = r["plot"]
R_NULL = NULL

if not R_IS_INSTALLED:
    raise ImportError("R is not installed! \n" + USAGE_MESSAGE)

if not RPY2_IS_INSTALLED:
    raise ImportError(RPY2_ERROR_MESSAGE + USAGE_MESSAGE)