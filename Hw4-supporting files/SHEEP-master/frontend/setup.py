from setuptools import setup, find_packages

setup(
    name="pysheep",
    version="0.1.0",
    description="Python client for SHEEP (Homomorphic Encryption Evaluation Platform)",
    packages=find_packages(),
    install_requires=[
        "requests",
        "flask",
        "wtforms",
        "sqlalchemy",
        "python-nvd3",
        "pytest",
        "jupyter",
        "matplotlib",
        "pandas",
    ],
    python_requires=">=3.6",
)

