from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="log-decorators",
    version="1.0.1",
    description="A Python library for decorators for functions return values logging in the console or file.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel Stefanov",
    packages=find_packages(),
)
