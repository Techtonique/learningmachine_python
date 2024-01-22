#!/usr/bin/env python

import subprocess
from installr import check_r_installed, install_r
from os import path
from setuptools import setup, find_packages
from setuptools.dist import Distribution
from setuptools.command.install import install


# Define a custom install command
class CustomInstall(install):
    def run(self):
        # List of packages to install before setup
        pre_install_packages = ['pip', 'rpy2>=3.4.5']

        # Install pre-requisite packages
        self.distribution.fetch_build_eggs(pre_install_packages)

        # Continue with the default installation process
        install.run(self)

# Use the custom install command
class CustomDistribution(Distribution):
    def get_command_class(self, command):
        if command == 'install':
            return CustomInstall
        return Distribution.get_command_class(self, command)

# Check if R is installed; if not, install it
if not check_r_installed():
    print("Installing R...")
    install_r()
else:
    print("No R installation needed.")

# Install R packages
print("Installing R packages...")
commands = ['try(utils::install.packages("R6", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)', 
            'try(utils::install.packages("Rcpp", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)',
            'try(utils::install.packages("skimr", repos="https://cloud.r-project.org", dependencies = TRUE), silent=FALSE)', 
            'try(utils::install.packages("learningmachine", repos="https://techtonique.r-universe.dev", dependencies = TRUE), silent=FALSE)',
            'try(utils::install.packages("learningmachine", repos="https://techtonique.r-universe.dev", dependencies = TRUE, lib="."), silent=FALSE)']
for cmd in commands:
    try:
        subprocess.run(['Rscript', '-e', cmd])
    except Exception as e:
        pass

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
    cmdclass={'install': CustomInstall},
    distribution=CustomDistribution,
)
