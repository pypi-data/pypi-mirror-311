# setup.py
from setuptools import setup, find_packages

setup(
    name="numpy_package",  
    version="0.1",
    description="A package for numerical operations using NumPy",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),  
    install_requires=[
        "numpy",  
    ],
)
