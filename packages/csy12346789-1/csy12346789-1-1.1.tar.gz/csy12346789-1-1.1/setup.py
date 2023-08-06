from distutils.core import  setup
import setuptools
packages = ['csy12346789-1']# 唯一的包名，自己取名
setup(name='csy12346789-1',
	version='1.1',
	author='wjl',
    packages=packages, 
    package_dir={'requests': 'requests'},)
