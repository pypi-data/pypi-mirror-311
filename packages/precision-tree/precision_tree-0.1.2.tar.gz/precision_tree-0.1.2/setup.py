from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="precision-tree",
    version="0.1.2",
    author="Oleh Danylevych",
    author_email="danylevych123@gmail.com",
    description="Precision Tree Module for precision decision analysis, supporting custom nodes (Decision, Chance, and Payoff) with visualization and optimal path calculation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/danylevych/precision-tree",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=requirements,
)
