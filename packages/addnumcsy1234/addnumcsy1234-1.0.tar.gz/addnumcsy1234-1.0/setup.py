from distutils.core import  setup
import setuptools
from setuptools import setup, find_packages
packages = ['addnumcsy1234']# 唯一的包名，自己取名
setup(name='addnumcsy1234',
	version='1.0',
	author='wjl',
    packages=packages, 
    package_dir={'requests': 'requests'},)
