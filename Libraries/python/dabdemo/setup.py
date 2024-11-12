from setuptools import setup, find_packages
import dabdemo

setup(
    name = "dabdemo",
    version = dabdemo.__version__,
    author = dabdemo.__author__,
    url = "https://your-url.com",
    author_email = "your.email@example.com",
    description = "Demo package for Jenkins CI/CD with Databricks",
    packages = find_packages(include = ["dabdemo"]),
    entry_points={"group_1": "run=dabdemo.__main__:main"},
    install_requires = ["setuptools"]
)