# -*- coding: utf-8 -*-
from os.path import abspath, dirname, exists, join

from setuptools import find_packages, setup

long_description = None
if exists("README.rst"):
    with  open("README.rst") as file:
        long_description = file.read()

install_reqs = []

setup(
        name='pywinregistry',
        version="0.0.1",
        description="A windows registry script generator written in pure Python.",
        long_description_content_type="text/x-rst",
        long_description=long_description,
        author='songs18',
        author_email='sounghaohao@gmail.com',
        license='MIT',
        packages=find_packages(),
        url="https://github.com/songs18/PyWinRegistry",
        zip_safe=False,
        include_package_data=True,
        install_requires=install_reqs,
)
