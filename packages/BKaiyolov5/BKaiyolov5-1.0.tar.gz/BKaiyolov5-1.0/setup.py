from distutils.core import  setup
import setuptools
packages = ['YOLOV5D']# 唯一的包名，自己取名
setup(name='BKaiyolov5',
	version='1.0',
	author='shenhui',
    packages=packages,
    package_dir={'requests': 'requests'},)
