# from distutils.core import setup
from setuptools import setup


def readme_file():
    with open("README.rst", encoding="utf-8") as rf:
        return rf.read()


setup(name="cxy_addons", version="1.0.0", description="this is a niubi lib",
    packages=["cxy_addons"], py_modules=["Tool"], author="Sz", author_email="2562891194@qq.com",
    long_description=readme_file(),
    url="https://github.com/chenxingyuan/python_code", license="MIT")


