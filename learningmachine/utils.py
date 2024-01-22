import subprocess
from rpy2.robjects import r


def check_pkg_installed():
    """Check if a package is installed in R."""
    return len(r(f"system.file(package = 'learningmachine')")) > 0


def check_install_r_pkg():
    """Install an R package."""
    if check_pkg_installed() == False:
        try:
            r(
                "utils::install.packages('R6', repos = 'https://cran.r-project.org', dependencies = TRUE)"
            )
            r(
                "utils::install.packages('Rcpp', repos = 'https://cran.r-project.org', dependencies = TRUE)"
            )
            r(
                "utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), dependencies = TRUE)"
            )
        except Exception as e1:
            try:
                r(
                    "utils::install.packages('R6', repos = 'https://cran.r-project.org', lib = '.', dependencies = TRUE)"
                )
                r(
                    "utils::install.packages('Rcpp', repos = 'https://cran.r-project.org', lib = '.', dependencies = TRUE)"
                )
                r(
                    "utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.', dependencies = TRUE)"
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
                            "utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), dependencies = TRUE)",
                        ]
                    )
                except Exception as e3:
                    subprocess.run(
                        [
                            "Rscript",
                            "-e",
                            "utils::install.packages('R6', repos = 'https://cran.r-project.org', lib = '.')",
                        ]
                    )
                    subprocess.run(
                        [
                            "Rscript",
                            "-e",
                            "utils::install.packages('Rcpp', repos = 'https://cran.r-project.org', lib = '.')",
                        ]
                    )
                    subprocess.run(
                        [
                            "Rscript",
                            "-e",
                            "utils::install.packages('learningmachine', repos = c('https://techtonique.r-universe.dev', 'https://cran.r-project.org'), lib = '.')",
                        ]
                    )
    if check_pkg_installed() == True:
        return 1
    return 0
