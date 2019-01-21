from setuptools import find_packages
from setuptools import setup

setup(
    name='whmcspy',
    version='0.1.0',
    author='Smoose BV',
    description='Python interface to the WHMCS API.',
    license='GPL-3',
    packages=find_packages(),
    install_requires=[
        'requests >= 2.21.0',
    ]
)
