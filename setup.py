#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

import jenkins_cli
import os

def get_version():

    return jenkins_cli.__version__

here = os.path.abspath(os.path.dirname(__file__))
requirements_file = os.path.join(here, 'requirements.txt')
with open(requirements_file, 'r') as f:
    requirements = [d.translate(None, '\n\r') for d in f.readlines()]

setup(name='jenkins-cli',
      version=get_version(),
      description='Interact with Jenkins API',
      long_description='Interact with Jenkins API',
      author='massimone88',
      author_email='stefano.mandruzzato@gmail.com',
      license='LGPLv3',
      url='https://github.com/massimone88/python-jenkins',
      packages=find_packages(),
      install_requires=requirements,
      entry_points={
          'console_scripts': [
              'jenkins = jenkins_cli.cli:main'
          ]
      },
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows'
        ]
      )
