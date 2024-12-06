"""Setup script for realpython-reader"""

# Standard library imports
import os
import pathlib
import json

# Third party imports
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).resolve().parent

# The text of the README file is used as a description
README = (HERE / "README.md").read_text()
PACKAGEINFO = (HERE / "src/package.json").read_text()
settings = json.loads(PACKAGEINFO)

thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements.txt'
install_req = []  # Here we'll get: ["gunicorn", "docutils>=0.3", "lxml==0.5a7"]
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_req = f.read().splitlines()

# This call to setup() does all the work
setup(
    name=settings["name"],
    version                         = settings["version"],
    description                     = settings["description"],
    long_description_content_type   = settings["long_description_content_type"],
    url                             = settings["url"],
    author                          = settings["author"],
    author_email                    = settings["author_email"],
    license                         = settings["license"],
    classifiers                     = settings["classifiers"],
    packages                        = settings["packages"],
    include_package_data            = settings["include_package_data"],
    install_requires                = settings["install_requires"],
    entry_points                    = {"console_scripts": ["microservicebus-py=src.start:main"]},
    long_description                = README,
)
