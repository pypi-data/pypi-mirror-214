from distutils.core import  setup
import setuptools
packages = ['csy3513']# 唯一的包名，自己取名
setup(name='csy3513',
	version='1.1',
	author='wjl',
    packages=packages, 
    package_dir={'requests': 'requests'},)
