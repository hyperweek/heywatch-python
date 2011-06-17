from setuptools import setup
import sys, os

METADATA = dict(
  name = 'heywatch-python',
  version = '1.0.0',
  py_modules = ['heywatch'],
  author='Bruno Celeste',
  author_email='bruno@particle-s.com',
  description='A python wrapper around the HeyWatch API',
  license='MIT License',
  url='http://heywatch.com',
  keywords='heywatch api',
	long_description=open('./README.md', 'r').read()
)

def Main():
  # Use setuptools if available, otherwise fallback and use distutils
  try:
    import setuptools
    setuptools.setup(**METADATA)
  except ImportError:
    import distutils.core
    distutils.core.setup(**METADATA)

if __name__ == '__main__':
  Main()