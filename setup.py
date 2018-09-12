# -*-coding:utf-8 -*-
from setuptools import setup, find_packages

setup(
    name = "tscantarget",
    description = "parse input file",
    version = "1.0",
    author = "shaochuyu",
    author_email = "shaochuyu@qq.com",
    #install_requires = ["pymongo","elasticsearch","MySQL-Python","requests","geoip2"],
	packages=find_packages(),
    entry_points={
        "console_scripts":[
            'tscantarget=tscantarget.__main__:main'
        ]
    }
)