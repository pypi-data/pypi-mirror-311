from setuptools import setup, find_packages

setup(
    name="fixparser",  # Name of the library
    version="1.0.0",  # Version of the library
    description="A Python library for parsing FIX protocol messages and exporting to text and CSV.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Meet Jethwa",
    author_email="meetjethwa3@gmail.com",  # Link to your GitHub repository
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "fixparser=fixparser.cli:main",
        ],
    },
    install_requires=[],  # Add any dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)