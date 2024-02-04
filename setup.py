#!/usr/bin/env python

# 1 - import Python packages -----------------------------------------------

import subprocess

subprocess.run(["pip", "install", "setuptools"])
subprocess.run(["pip", "install", "rpy2"])

from os import path
import platform
from setuptools import setup, find_packages
from rpy2.robjects.vectors import StrVector
from rpy2.robjects import r
from rpy2.robjects.packages import importr

# 2 - utility functions -----------------------------------------------


def check_r_installed():
    current_platform = platform.system()

    if current_platform == "Windows":
        # Check if R is installed on Windows by checking the registry
        try:
            subprocess.run(
                ["reg", "query", "HKLM\\Software\\R-core\\R"], check=True
            )
            print("R is already installed on Windows.")
            return True
        except subprocess.CalledProcessError:
            print(
                "R is required but not installed on Windows (check manually: https://cloud.r-project.org/)."
            )
            return False

    elif current_platform == "Linux":
        # Check if R is installed on Linux by checking if the 'R' executable is available
        try:
            subprocess.run(["which", "R"], check=True)
            print("R is already installed on Linux.")
            return True
        except subprocess.CalledProcessError:
            print(
                "R is required but not installed on Linux (check manually: https://cloud.r-project.org/)."
            )
            return False

    elif current_platform == "Darwin":  # macOS
        # Check if R is installed on macOS by checking if the 'R' executable is available
        try:
            subprocess.run(["which", "R"], check=True)
            print("R is already installed on macOS.")
            return True
        except subprocess.CalledProcessError:
            print(
                "R is required but not installed on macOS (check manually: https://cloud.r-project.org/)."
            )
            return False

    else:
        print("Unsupported platform (check manually: https://cloud.r-project.org/)")
        return False


def install_r():
    current_platform = platform.system()

    if current_platform == "Windows":
        # Install R on Windows using PowerShell
        install_command = "Start-Process powershell -Verb runAs -ArgumentList '-Command \"& {Invoke-WebRequest https://cran.r-project.org/bin/windows/base/R-4.1.2-win.exe -OutFile R.exe}; Start-Process R.exe -ArgumentList '/SILENT' -Wait}'"
        subprocess.run(install_command, shell=True)

    elif current_platform == "Linux":
        # Install R on Linux using the appropriate package manager (e.g., apt-get)
        install_command = (
            "sudo apt update -qq && sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9"
            + "&& sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu focal-cran40/'"
            + "&& sudo apt update"
            + "&& sudo apt install r-base"
        )
        try: 
            subprocess.run(install_command, shell=True)
        except Exception as e:
            print("Error installing R on this Linux distribution. Please check manually: https://cloud.r-project.org/")

    elif current_platform == "Darwin":  # macOS
        # Install R on macOS using Homebrew
        install_command = "brew install r"
        try: 
            subprocess.run(install_command, shell=True)
        except Exception as e:
            print("Error installing R on macOS. Please check manually: https://cloud.r-project.org/")

    else:
        print("Unsupported platform. Unable to install R.")


# 3 - Install packages -----------------------------------------------

# Check if R is installed; if not, install it
if check_r_installed() == False:
    print("Installing R...")
    install_r()
else:
    print("R is already installed, no R installation needed.")

# Install R packages
commands1_lm = (
    'base::system.file(package = "learningmachine")'  # check "learningmachine" is installed
)
commands2_lm = 'base::system.file("learningmachine_r", package = "learningmachine")'  # check "learningmachine" is installed locally
exec_commands1_lm = subprocess.run(
    ["Rscript", "-e", commands1_lm], capture_output=True, text=True
)
exec_commands2_lm = subprocess.run(
    ["Rscript", "-e", commands2_lm], capture_output=True, text=True
)
if (
    len(exec_commands1_lm.stdout) == 7 and len(exec_commands2_lm.stdout) == 7
):  # kind of convoluted, but works
    print("Installing R packages...")
    commands1 = [
        'try(utils::install.packages(c("R6", "Rcpp", "skimr"), repos="https://cloud.r-project.org", dependencies = TRUE), silent=TRUE)',
        'try(utils::install.packages("learningmachine", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=TRUE)',
    ]
    commands2 = [
        'try(utils::install.packages(c("R6", "Rcpp", "skimr"), lib="./learningmachine_r", repos="https://cloud.r-project.org", dependencies = TRUE), silent=TRUE)',
        'try(utils::install.packages("learningmachine", lib="./learningmachine_r", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=TRUE)',
    ]
    try:
        for cmd in commands1:
            subprocess.run(["Rscript", "-e", cmd])
    except Exception as e: # can't install packages globally
        subprocess.run(["mkdir", "learningmachine_r"])
        for cmd in commands2:
            subprocess.run(["Rscript", "-e", cmd])

    base = importr("base")

    try:
        base.library(StrVector(["learningmachine"]))
    except Exception as e1: # can't load the package from the global environment
        try:
            base.library(
                StrVector(["learningmachine"]), lib_loc="learningmachine_r"
            )
        except Exception as e2: # well, we tried
            try:
                r("try(library('learningmachine'), silence=TRUE)")
            except NotImplementedError as e3: # well, we tried everything at this point
                r(
                    "try(library('learningmachine', lib.loc='learningmachine_r'), silence=TRUE)"
                )

"""The setup script."""
here = path.abspath(path.dirname(__file__))

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]

setup(
    author="T. Moudiki",
    author_email="thierry.moudiki@gmail.com",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Machine Learning with uncertainty quantification and interpretability",
    install_requires=install_requires,
    license="BSD Clause Clear license",
    long_description="Machine Learning with uncertainty quantification and interpretability.",
    include_package_data=True,
    keywords="learningmachine",
    name="learningmachine",
    packages=find_packages(include=["learningmachine", "learningmachine.*"]),
    test_suite="tests",
    url="https://github.com/Techtonique/learningmachine",
    version="0.2.2",
    zip_safe=False,
)
