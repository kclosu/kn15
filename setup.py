from setuptools import setup, find_packages
from kn15 import __version__

setup(
    name='kn15',
    version=__version__,
    description='a python package that parses coded КН-15 hydrology reports',
    packages=find_packages()
)
