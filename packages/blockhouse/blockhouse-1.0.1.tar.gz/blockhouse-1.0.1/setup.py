# setup.py

import setuptools
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the contents of README.md
README = (HERE / "README.md").read_text(encoding="utf-8")

setuptools.setup(
    name="blockhouse",  # Unique package name on PyPI
    version="1.0.1",
    author="Karan",
    author_email="karanallaghsingh@gmail.com",
    description="A Python SDK for interacting with JSONPlaceholder and your custom APIs.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/Blockhouse-Repo/Blockhouse/tree/main/Backend/PythonSDK",  # Repository URL
    packages=setuptools.find_packages(include=["blockhouse", "blockhouse.*"]),
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
    install_requires=[
        "requests>=2.25.1",
    ],
    entry_points={
        'console_scripts': [
            'blockhouse=blockhouse.sdk:main',  # Command-line interface
        ],
    },
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
)
