#!/usr/bin/env python

import subprocess
from installr import check_r_installed, install_r
from os import path
from setuptools import setup, find_packages
from rpy2.robjects import r

# Check if R is installed; if not, install it
if not check_r_installed():
    print("Installing R...")
    install_r()
else:
    print("No R installation needed.")

subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.run(['python', '-m', 'pip', 'install', 'rpy2>=3.4.5'])

try:   
    r("options(repos = c(techtonique = 'https://techtonique.r-universe.dev', CRAN = 'https://cloud.r-project.org')); install.packages(c('Rcpp', 'R6'), dependencies = TRUE)") 
    r("options(repos = c(techtonique = 'https://techtonique.r-universe.dev', CRAN = 'https://cloud.r-project.org')); install.packages('learningmachine', dependencies = TRUE)")        
except Exception as e:
    r("options(repos = c(techtonique = 'https://techtonique.r-universe.dev', CRAN = 'https://cloud.r-project.org')); install.packages(c('Rcpp', 'R6'), dependencies = TRUE, lib='.', verbose=FALSE, quiet=TRUE)")    
    r("options(repos = c(techtonique = 'https://techtonique.r-universe.dev', CRAN = 'https://cloud.r-project.org')); install.packages('learningmachine', dependencies = TRUE, lib='.', verbose=FALSE, quiet=TRUE)")    

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
