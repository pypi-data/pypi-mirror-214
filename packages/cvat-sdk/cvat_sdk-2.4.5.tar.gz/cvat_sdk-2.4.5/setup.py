# Copyright (C) 2022 CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

# CVAT REST API
#
# REST API for Computer Vision Annotation Tool (CVAT)  # noqa: E501
#
# The version of the OpenAPI document: 2.4.5
# Contact: support@cvat.ai
# Generated by: https://openapi-generator.tech


import os.path as osp
import re
from setuptools import find_packages, setup

# To install the library, run the following
#
# python -m pip install .
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

def find_version(project_dir=None):
    if not project_dir:
        project_dir = osp.dirname(osp.abspath(__file__))

    file_path = osp.join(project_dir, "version.py")

    with open(file_path, "r") as version_file:
        version_text = version_file.read()

    # PEP440:
    # https://www.python.org/dev/peps/pep-0440/#appendix-b-parsing-version-strings-with-regular-expressions
    pep_regex = r"([1-9]\d*!)?(0|[1-9]\d*)(\.(0|[1-9]\d*))*((a|b|rc)(0|[1-9]\d*))?(\.post(0|[1-9]\d*))?(\.dev(0|[1-9]\d*))?"
    version_regex = r"VERSION\s*=\s*.(" + pep_regex + ")."
    match = re.match(version_regex, version_text)
    if not match:
        raise RuntimeError("Failed to find version string in '%s'" % file_path)

    version = version_text[match.start(1) : match.end(1)]
    return version


BASE_REQUIREMENTS_FILE = "requirements/base.txt"


def parse_requirements(filename=BASE_REQUIREMENTS_FILE):
    with open(filename) as fh:
        reqs = [line.strip() for line in fh.readlines()]

    for req in reqs[:]:
        if req.startswith('-r '):
            dep = req.split(maxsplit=2)[1]
            reqs.extend(parse_requirements(osp.join(osp.dirname(filename), dep.lstrip('/\\'))))

    for req in reqs[:]:
        if req.startswith('-r '):
            reqs.remove(req)

    return reqs


BASE_REQUIREMENTS = parse_requirements(BASE_REQUIREMENTS_FILE)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cvat_sdk",
    version=find_version(project_dir="cvat_sdk"),
    description="CVAT REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="CVAT.ai team",
    author_email="support@cvat.ai",
    url="https://github.com/cvat-ai/cvat",
    keywords=["OpenAPI", "OpenAPI-Generator", "CVAT REST API"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=BASE_REQUIREMENTS,
    extras_require={
        "pytorch": ['torch', 'torchvision'],
    },
    package_dir={"": "."},
    packages=find_packages(include=["cvat_sdk*"]),
    include_package_data=True,
    license="MIT License",
)
