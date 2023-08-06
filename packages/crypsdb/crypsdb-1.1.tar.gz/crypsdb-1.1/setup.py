from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="crypsdb",
    version="1.1",
    author="Pawan kumar",
    author_email="control@vvfin.in",
    description="A lightweight JSON-based database system for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/E491K8/crypsDb",
    packages=find_packages(),
    py_modules=['crypsdb'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
