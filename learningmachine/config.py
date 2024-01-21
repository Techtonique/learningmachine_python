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
>> Rscript -e 'install.packages("learningmachine", repos = https://techtonique.r-universe.dev)'    
"""

r["options"](warn=-1)


def _none2null(none_obj):
    return r("NULL")


none_converter = cv.Converter("None converter")
none_converter.py2rpy.register(type(None), _none2null)

required_packages = ["learningmachine", "bcn", "Rcpp", "R6", "dfoptim"]  # list of required R packages

packages_to_install = [
    x for x in required_packages if not rpackages.isinstalled(x)
]

base = importr("base")
utils = importr("utils")
graphics = importr("graphics")

print(f" required_packages: {required_packages} \n")

if len(packages_to_install) > 0:
    base.options(
        repos=base.c(
            techtonique="https://techtonique.r-universe.dev",
            CRAN="https://cloud.r-project.org",
        )
    )

if len(packages_to_install) > 0:
    try:
        print("INSTALLING AS USUAL...")   
        if len(packages_to_install) > 0:     
            utils.install_packages(
                    StrVector(packages_to_install),
                    dependencies=True,
                )
    except Exception as e1:
        try:  
            print("INSTALLING in '.' ...")
            if len(packages_to_install) > 0:
                utils.install_packages(
                    StrVector(packages_to_install),
                    dependencies=True,
                    lib_loc=".",
                )
        except Exception as e2: 
            try:  
                print("INSTALLING FROM COMMAND LINE...")
                for pkg in packages_to_install:
                    subprocess.run(['Rscript', 'e', f"utils.install_packages({pkg}, repos=c('https://cloud.r-project.org', 'https://techtonique.r-universe.dev'))"])
            except Exception as e3:
                print("INSTALLING FROM COMMAND LINE in '.' ...")
                for pkg in packages_to_install:
                    subprocess.run(['Rscript', 'e', f"utils.install_packages({pkg}, repos=c('https://cloud.r-project.org', 'https://techtonique.r-universe.dev'), lib='.')"])
        
FLOATMATRIX = FloatMatrix
FLOATVECTOR = FloatVector
STRVECTOR = StrVector
try: 
    print("IMPORTING IN PYTHON AS USUAL...")
    LEARNINGMACHINE_PACKAGE = importr("learningmachine")
except Exception as e:
    print("IMPORTING IN PYTHON FROM '.' ...")
    LEARNINGMACHINE_PACKAGE = importr("learningmachine", lib_loc=".")
CHECK_PACKAGES = True
DEEP_COPY = lambda x: pickle.loads(pickle.dumps(x, -1))
NONE_CONVERTER = none_converter
PLOT_BASE = r["plot"]
R_NULL = NULL

if not R_IS_INSTALLED:
    raise ImportError("R is not installed! \n" + USAGE_MESSAGE)

if not RPY2_IS_INSTALLED:
    raise ImportError(RPY2_ERROR_MESSAGE + USAGE_MESSAGE)