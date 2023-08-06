from distutils.core import  setup
import setuptools
packages = ['csy12346']# 唯一的包名，自己取名
setup(name='csy12346',
	version='1.0',
	author='wjl',
    packages=packages, 
    package_dir={'requests': 'requests'},)
