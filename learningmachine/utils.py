import subprocess
from rpy2.robjects import r


def check_pkg_installed(pkg_name):
    """Check if a package is installed in R."""
    return len(r(f"system.file(package = '{pkg_name}')")) > 0


def check_install_r_pkg(pkg_name):
    """Install an R package."""
    if check_pkg_installed(pkg_name) == False:
        try:
            r(
                f"utils::install.packages('R6', repos = 'https://cran.r-project.org', dependencies = TRUE)"
            )
            r(
                f"utils::install.packages('Rcpp', repos = 'https://cran.r-project.org', dependencies = TRUE)"
            )
            r(
                f"utils::install.packages('{pkg_name}', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), dependencies = TRUE)"
            )
        except Exception as e1:
            try:
                r(
                f"utils::install.packages('R6', repos = 'https://cran.r-project.org', dependencies = TRUE)"
                )
                r(
                    f"utils::install.packages('Rcpp', repos = 'https://cran.r-project.org', dependencies = TRUE)"
                )
                r(
                    f"utils::install.packages('{pkg_name}', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.', dependencies = TRUE)"
                )
            except Exception as e2:
                try:
                    subprocess.run(
                        [
                            "Rscript",
                            "-e",
                            f"utils::install.packages('R6', repos = 'https://cran.r-project.org', dependencies = TRUE)",
                        ]
                    )
                    subprocess.run(
                        [
                            "Rscript",
                            "-e",
                            f"utils::install.packages('Rcpp', repos = 'https://cran.r-project.org', dependencies = TRUE)",
                        ]
                    )
                    subprocess.run(
                        [
                            "Rscript",
                            "-e",
                            f"utils::install.packages('{pkg_name}', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), dependencies = TRUE)",
                        ]
                    )
                except Exception as e3:
                    subprocess.run(
                        [
                            "Rscript",
                            "-e",
                            f"utils::install.packages('R6', repos = 'https://cran.r-project.org', lib = '.')",
                        ]
                    )
                    subprocess.run(
                        [
                            "Rscript",
                            "-e",
                            f"utils::install.packages('Rcpp', repos = 'https://cran.r-project.org', lib = '.')",
                        ]
                    )
                    subprocess.run(
                        [
                            "Rscript",
                            "-e",
                            f"utils::install.packages('{pkg_name}', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.')",
                        ]
                    )
    if check_pkg_installed(pkg_name) == True:
        return 1
    return 0
