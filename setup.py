#!/usr/bin/env python

from distutils.core import setup

setup(name='Checkthat',
      version='1.0',
      description='A automated Arch Linux AUR package builder and analyzer written in Python',
      author='Andrew Crerar',
      author_email='andrew@crerar.io',
      url='https://github.com/andrewSC/checkthat',
      license='MIT',
      packages=['checkthat'],
      entry_points={
          'console_scripts': [
              'checkthat = checkthat.checkthat:main'
          ]
      })
