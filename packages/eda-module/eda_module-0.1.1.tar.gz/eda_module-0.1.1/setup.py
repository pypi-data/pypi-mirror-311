from setuptools import setup, find_packages

setup(
    name="eda_module",  # Your package name
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'plotly',
        'streamlit',  # Add Streamlit as a requirement
    ],
    entry_points={
        'console_scripts': [
            'launch-eda-dashboard=eda_module.dashboard:main',  # Entry point for running Streamlit app
        ],
    },
    # Additional metadata (optional)
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jhansi Siriprolu',
    author_email='siriprolu2018@gmail.com',
    description='A package for EDA with Streamlit dashboard',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
