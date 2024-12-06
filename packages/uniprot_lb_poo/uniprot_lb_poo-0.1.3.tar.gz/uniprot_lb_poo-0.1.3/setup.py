from setuptools import setup, find_packages

setup(
    name="uniprot_lb_poo",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
