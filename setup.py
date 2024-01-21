#!/usr/bin/env python

import subprocess
from installr import check_r_installed, install_r
from os import path
from setuptools import setup, find_packages

# Check if R is installed; if not, install it
if not check_r_installed():
    print("Installing R...")
    install_r()
else:
    print("No R installation needed.")

subprocess.run(['python', '-m', 'pip', 'install', '--upgrade', 'pip'])
subprocess.run(['python', '-m', 'pip', 'install', 'rpy2>=3.4.5'])

from rpy2.robjects import r

try: 
    r("utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'))")
except Exception as e1:
    try:
        r("utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.')")
    except Exception as e2: 
        try: 
            subprocess.run(['Rscript', '-e', "utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'))"])
        except Exception as e3:
            subprocess.run(['Rscript', '-e', "utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.')"])

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
