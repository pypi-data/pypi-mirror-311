from setuptools import setup, find_packages

setup(
    name="uniprot",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
