#!/usr/bin/python3

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = list(map(str.strip, f.read().split("\n")))[:-1]

setup(
    name="brownie-token-tester",
    packages=find_packages(exclude=["tests", "tests.*"]),
    py_modules=["brownie_tokens"],
    version="0.1.0",  # don't change this manually, use bumpversion instead
    license="MIT",
    description="Helper objects for generating ERC20s while testing a Brownie project.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ben Hauser",
    author_email="ben@hauser.id",
    url="https://github.com/iamdefinitelyahuman/brownie-token-tester",
    keywords=["brownie", "ethereum", "web3py"],
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.6,<4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
