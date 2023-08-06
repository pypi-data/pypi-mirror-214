# -*- coding: UTF-8 -*-
# @Time : 2022/8/17 16:07 
# @Author : 刘洪波

import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ebooksp',
    version='0.0.6',
    packages=setuptools.find_packages(),
    url='https://gitee.com/maxbanana',
    license='Apache',
    author='hongbo liu',
    author_email='782027465@qq.com',
    description='A Conversion Tool for e-book',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['epubs>=0.0.3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
