# coding: utf-8
from distutils.core import  setup
import setuptools

packages = ['ShuaiToolBox']
setup(name='ShuaiToolBox',
	version='1.1.2.7',
	author='ShuaiZ',
	description="packages for experiments process",
    packages=setuptools.find_packages(), 
    install_requires=['numpy','natsort','opencv-python'],
    package_dir={'requests': 'requests'},
    python_requires='>=3.7',
    include_package_data=True,
    )
