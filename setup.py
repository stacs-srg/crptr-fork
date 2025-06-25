from setuptools import setup, find_packages

setup(
    name="crptr-populations",
    version="v2.0.0",
    packages=find_packages(where="src/main/python"),
    package_dir={"": "src/main/python"},
)