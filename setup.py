#!/usr/bin/env python
from setuptools import setup
from io import open

def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

setup(name='SmartHomeBot',
      version='0.0.1',
      description="Implementation of author's vision of smart home bot ",
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      author='sashkoiv',
      author_email='sashkoiv@gmail.com',
      url='https://github.com/Sashkoiv/SmartHomeBot',
      packages=['SmartHomeBot'],
      license='Beerware',
      keywords='smart home telegram bot telemetry automation diy',
    #   install_requires=['requests', 'six'],
      extras_require={
          'json': 'ujson',
      },
      classifiers=[
        #   'Development Status :: 5 - Production/Stable',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Environment :: Console',
        #   'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
      ]
      )
