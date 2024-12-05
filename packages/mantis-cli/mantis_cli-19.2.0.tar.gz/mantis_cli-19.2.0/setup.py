#!/usr/bin/env python
from setuptools import setup, find_packages

from mantis import VERSION

setup(
    name='mantis-cli',
    version=VERSION,
    description='Management command to build and deploy webapps, especially based on Django',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Erik Telepovský',
    author_email='info@pragmaticmates.com',
    maintainer='Pragmatic Mates',
    maintainer_email='info@pragmaticmates.com',
    url='https://github.com/PragmaticMates/mantis-cli',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['cffi', 'cryptography', 'pycryptodome', 'PyYAML', 'prettytable'],
    entry_points={
        'console_scripts': ['mantis=mantis.command_line:run'],
    },
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Development Status :: 5 - Production/Stable'
    ],
    license='GNU General Public License (GPL)',
    keywords="management deployment docker command",
)
