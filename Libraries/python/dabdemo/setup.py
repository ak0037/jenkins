from setuptools import setup, find_packages

# Define version directly here instead of importing
__version__ = '0.0.1'

setup(
    name = "dabdemo",
    version = __version__,
    author = "Your Name",
    url = "https://github.com/ak0037/jenkins",
    author_email = "abhinav.katiyar@space-multimedia.com",
    description = "Demo package for Jenkins CI/CD with Databricks",
    packages = find_packages(include = ["dabdemo"]),
    entry_points={"group_1": "run=dabdemo.__main__:main"},
    install_requires = ["setuptools"]
)