from setuptools import setup, find_packages

setup(
    name="AkhiCalculatorxsx",  # Ensure this name is unique on PyPI
    version="0.1.0",
    description="A simple calculator package",
    author="Akhi",
    author_email="akhildevops15@gmail.com",
    packages=find_packages(),  # Automatically include the 'calku' package
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
