from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
name = "dbgeomparser",
version = "0.1.0",
author = 'Nino Shaw',
author_email = 'ninoshaw27@gmail.com',
description = "A package to handle conversion of shapely geometries to Oracle database compatible geometry objects",
install_requires = [
    'oracledb',
    'shapely',
    'numpy'
],
long_description_content_type='text/markdown',
long_description = long_description,
packages = find_packages(),
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
],
python_requires = ">=3.6",
)