from setuptools import find_packages
from setuptools import setup


with open('README.md', 'r') as readme:
    long_description = readme.read()


version = '0.1.6'


setup(
    name='whmcspy',
    version=version,
    author='Smoose BV',
    description='Python interface to the WHMCS API.',
    url='https://github.com/Smoose-bv/whmcspy',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='GPL-3',
    keywords='whmcs api library',
    packages=find_packages(),
    install_requires=[
        'requests >= 2.21.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    command_options={
        'build_sphinx': {
            'version': ('setup.py', version),
        },
    },
)
