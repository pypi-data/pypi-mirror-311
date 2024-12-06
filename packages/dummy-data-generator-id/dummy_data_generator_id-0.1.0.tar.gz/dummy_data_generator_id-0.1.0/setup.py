from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dummy-data-generator-id",
    version="0.1.0",
    author="Brian Adi",
    author_email="uix.brianadi@gmail.com",
    description="A library for generating realistic dummy data for Indonesian context",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bri-anadi/dummy-data-generator-id",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[],
    keywords="dummy-data generator indonesia random",
)
