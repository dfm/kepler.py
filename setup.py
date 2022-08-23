from setuptools import find_packages
from skbuild import setup

setup(
    name="kepler.py",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    cmake_install_dir="src/kepler",
    include_package_data=True,
)
