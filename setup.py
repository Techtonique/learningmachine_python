#!/usr/bin/env python

import subprocess
import sys 
from installr import check_r_installed, install_r
from os import path
from setuptools import setup, find_packages
from setuptools.dist import Distribution
from setuptools.command.install import install

# Check if R is installed; if not, install it
if not check_r_installed():
    print("Installing R...")
    install_r()
else:
    print("No installation needed.")

# Install R packages
commands1_lm = 'base::system.file(package = "learningmachine")' # check is installed 
commands2_lm = 'base::system.file("learningmachine_r", package = "learningmachine")' # check is installed locally 
exec_commands1_lm = subprocess.run(['Rscript', '-e', commands1_lm], capture_output=True, text=True)
exec_commands2_lm = subprocess.run(['Rscript', '-e', commands2_lm], capture_output=True, text=True)
if (len(exec_commands1_lm.stdout) == 7 and len(exec_commands2_lm.stdout) == 7): # kind of convoluted, but works    
    print("Installing R packages...")
    commands1 = ['try(utils::install.packages("R6", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)', 
                'try(utils::install.packages("Rcpp", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)',
                'try(utils::install.packages("skimr", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)', 
                'try(utils::install.packages("learningmachine", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=FALSE)']
    commands2 = ['try(utils::install.packages("R6", lib="./learningmachine_r", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)', 
                'try(utils::install.packages("Rcpp", lib="./learningmachine_r", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)',
                'try(utils::install.packages("skimr", lib="./learningmachine_r", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)', 
                'try(utils::install.packages("learningmachine", lib="./learningmachine_r", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=FALSE)']
    try:             
        for cmd in commands1:
            subprocess.run(['Rscript', '-e', cmd])
    except Exception as e:
        subprocess.run(['mkdir', 'learningmachine_r'])
        for cmd in commands2:
            subprocess.run(['Rscript', '-e', cmd])

"""The setup script."""
here = path.abspath(path.dirname(__file__))

# get the dependencies and installs
with open(
    path.join(here, "requirements.txt"), encoding="utf-8"
) as f:
    all_reqs = f.read().split("\n")

install_requires = [
    x.strip() for x in all_reqs if "git+" not in x
]
dependency_links = [
    x.strip().replace("git+", "")
    for x in all_reqs
    if x.startswith("git+")
]

setup(
    author="T. Moudiki",
    author_email='thierry.moudiki@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Machine Learning with uncertainty quantification and interpretability",
    install_requires=install_requires,
    license="BSD Clause Clear license",
    long_description="Machine Learning with uncertainty quantification and interpretability.",
    include_package_data=True,
    keywords='learningmachine',
    name='learningmachine',
    packages=find_packages(include=['learningmachine', 'learningmachine.*']),
    test_suite='tests',
    url='https://github.com/Techtonique/learningmachine',
    version='0.2.0',
    zip_safe=False,
)
