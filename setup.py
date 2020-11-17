#!/usr/bin/env python

from setuptools import setup, Command, find_packages


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='copdaiagents',
      version='0.0.1',
      description='COPDAI Python Agents',
      license='Apache License 2.0',
      author='RABBAH Mahmoud Almostafa',
      author_email='mrabbah@ieee.org',
      url='https://github.com/mrabbah/copdaipythonagent',
      packages=find_packages(),
      install_requires=required,
      long_description=("Collaborative Open Platform for "
                        "Distributed Artificial Intelligence Agents")
     )
