from setuptools import setup, find_packages

setup(
    name="onenode",
    version="0.1.0",  # Initial version
    author="OneNode",
    author_email="hello@onenode.ai",
    description="The official Python library for the OneNode API",
    packages=find_packages(),  # Automatically find submodules
    python_requires=">=3.8",  # Minimum Python version
)
