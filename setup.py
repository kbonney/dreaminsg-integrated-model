#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = [
    "ipykernel>=6.29.5",
    "wntr>=1.3.2",
    "pandas>=2.2.3",
    "pandapower>=3.0.0",
    "contextily>=1.6.2",
    "seaborn>=0.13.2",
    "bokeh>=3.7.3",
    "geopandas>=1.0.1",
    "jupyter_bokeh>=4.0.5",
    "jupyter>=1.1.1",
    "notebook>=7.4.2",
    "numpy>=1.26.4",  # Required by pandas and other dependencies
    "matplotlib>=3.10.3",  # Required for plotting
    "networkx>=3.4.2",  # Required for graph operations
    "scipy>=1.13.1",  # Required for scientific computations
    "shapely>=2.1.0",  # Required by geopandas
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "nbformat>=5.10.4",
    "nbconvert>=7.16.6",
]

setup(
    author="Srijith Balakrishnan",
    author_email="srijith.balakrishnan@sec.ethz.ch",
    python_requires=">=3.8,<3.12",  # Updated Python version requirements
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    description="An integrated power-water-transportation model for urban simulations.",
    entry_points={
        "console_scripts": [
            "infrarisk=infrarisk.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="infrarisk",
    name="infrarisk",
    packages=find_packages(include=["infrarisk", "infrarisk.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/srijithabalakrishnan/dreaminsg_integrated_model",
    version="0.1.0",
    zip_safe=False,
)
