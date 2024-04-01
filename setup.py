#!/usr/bin/env python

import platform 
import subprocess
from os import path
from setuptools import setup, find_packages

# 0 - utility functions -----------------------------------------------

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
        except subprocess.CalledProcessError as e:
            install_r(prompt=True)
            return True            

    elif current_platform in ("Darwin", "Linux"):
        # Check if R is installed on Linux by checking if the 'R' executable is available
        
        if len(subprocess.run(["which", "R"], capture_output=True, text=True).stdout) > 0:
            print(f"R is already installed on {current_platform}.")
            return True
        else:
            install_r(prompt=True) 
            return True           

    else:
        print("Unsupported platform (check manually: https://cloud.r-project.org/)")
        return False

def install_r(prompt=False):

    current_platform = platform.system()

    if prompt == True:
        print("Installing R...")    
        # choice = input("Would you like to install R? (yes/no): ").strip().lower()
        # if choice == 'yes':
        #     print("Installing R...")    
        # elif choice == 'no':
        #     print("No problem. R will not be installed.")
        #     return 
        # else:
        #     print("Invalid input. Please enter 'yes' or 'no'.")
        #     return

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
        except NotImplementedError as e:
            print("Error installing R on this Linux distribution. Please check manually: https://cloud.r-project.org/")

    elif current_platform == "Darwin":  # macOS
        # Install R on macOS using Homebrew
        install_command = "brew install r"
        try: 
            subprocess.run(install_command, shell=True)
        except NotImplementedError as e:
            print("Error installing R on macOS. Please check manually: https://cloud.r-project.org/")

    else:
        print("Unsupported platform. Unable to install R.")

def load_learningmachine():
    # Install R packages
    commands1_lm = 'base::system.file(package = "learningmachine")'  # check "learningmachine" is installed
    commands2_lm = 'base::system.file("learningmachine_r", package = "learningmachine")'  # check "learningmachine" is installed locally
    exec_commands1_lm = subprocess.run(
        ["Rscript", "-e", commands1_lm], capture_output=True, text=True
    )
    exec_commands2_lm = subprocess.run(
        ["Rscript", "-e", commands2_lm], capture_output=True, text=True
    )
    if (
        len(exec_commands1_lm.stdout) == 7
        and len(exec_commands2_lm.stdout) == 7
    ):  # kind of convoluted, but works
        print("Installing R packages along with 'learningmachine'...")
        commands1 = [
            'try(utils::install.packages(c("R6", "Rcpp", "skimr"), repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)',
            'try(utils::install.packages("learningmachine", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=FALSE)',
        ]
        commands2 = [
            'try(utils::install.packages(c("R6", "Rcpp", "skimr"), lib="./learningmachine_r", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)',
            'try(utils::install.packages("learningmachine", lib="./learningmachine_r", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=FALSE)',
        ]
        commands3 = [
            'try(utils::install.packages(c("R6", "Rcpp", "remotes", "skimr"), repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)',
            'try(remotes::install_github("Techtonique/learningmachine"), silent=FALSE)',
        ]
        commands4 = [
            'try(utils::install.packages(c("R6", "Rcpp", "remotes", "skimr"), lib="./learningmachine_r", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)',
            'try(remotes::install_github("Techtonique/learningmachine", lib="./learningmachine_r", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=FALSE)',
        ]

        try:
            for cmd in commands1:
                subprocess.run(["Rscript", "-e", cmd])
        except NotImplementedError as e:  # can't install packages globally
            try: 
                subprocess.run(["mkdir", "learningmachine_r"])
                for cmd in commands2:
                    subprocess.run(["Rscript", "-e", cmd])
            except NotImplementedError as e:
                try: 
                    for cmd in commands3:
                        subprocess.run(["Rscript", "-e", cmd])
                except NotImplementedError as e:
                    subprocess.run(["mkdir", "learningmachine_r"])
                    for cmd in commands4:
                        subprocess.run(["Rscript", "-e", cmd])

        try:
            base.library(StrVector(["learningmachine"]))
        except (
            NotImplementedError
        ) as e1:  # can't load the package from the global environment
            try:
                base.library(
                    StrVector(["learningmachine"]), lib_loc="learningmachine_r"
                )
            except NotImplementedError as e2:  # well, we tried
                try:
                    r("try(library('learningmachine'), silence=TRUE)")
                except (
                    NotImplementedError
                ) as e3:  # well, we tried everything at this point
                    r(
                        "try(library('learningmachine', lib.loc='learningmachine_r'), silence=TRUE)"
                    )

# 1 - import Python packages -----------------------------------------------

subprocess.run(["pip", "install", "rpy2"])
try: 
    subprocess.run(["pip", "install", "setuptools"])
except ModuleNotFoundError as e:
    print("Error installing setuptools. Please install setuptools manually.")

from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector
from rpy2.robjects import r

base = importr("base")

if not check_r_installed():
    install_r()
else:
    print("R is already installed.")

load_learningmachine()

# 4 - Package setup -----------------------------------------------
    
"""The setup script."""

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
    install_requires=['numpy', 'pandas', 'rpy2>=3.4.5', 'scikit-learn', 'scipy'],
    license="BSD Clause Clear license",
    long_description="Machine Learning with uncertainty quantification and interpretability.",
    include_package_data=True,
    keywords="learningmachine",
    name="learningmachine",
    packages=find_packages(include=["learningmachine", "learningmachine.*"]),
    test_suite="tests",
    url="https://github.com/Techtonique/learningmachine_python",
    version="1.1.0",
    zip_safe=False,
)
