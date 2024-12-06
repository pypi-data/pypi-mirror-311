from setuptools import setup, find_packages

setup(
    name="eda_module",  # Package name
    version="0.1.0",  # Initial version
    description="A reusable EDA module for exploratory data analysis",
    long_description=open("README.md").read(),  # README as the package description
    long_description_content_type="text/markdown",
    author="Jhansi Siriprolu",
    author_email="siriprolu2018@gmail.com",
    url="https://github.com/jhansi-siriprolu/eda_module",
    license="MIT",
    packages=find_packages(),  # Automatically find all packages in this directory
    install_requires=[
        "pandas>=1.0",
        "numpy>=1.19",
        "matplotlib>=3.0",
        "seaborn>=0.11",
        "scipy>=1.5",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)