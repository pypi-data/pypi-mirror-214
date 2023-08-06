from distutils.core import  setup
import setuptools
packages = ['shenhui']# 唯一的包名，自己取名
setup(name='BKshenhui',
	version='1.0',
	author='shenhui',
    packages=packages, 
    package_dir={'requests': 'requests'},)
