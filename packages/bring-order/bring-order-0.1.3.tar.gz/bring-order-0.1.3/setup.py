from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="bring-order",
    version="0.1.3",
    description="The tool library is aimed at guiding data scientists with their analysis using custom widgets inside Jupyter Notebook.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Order-Team/bring-order/tree/main",
    author="Bring-Order team",
    author_email="example@email.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent"
    ],
    packages=["bring_order"],
    include_package_data=True,
    install_requires=requirements
)
