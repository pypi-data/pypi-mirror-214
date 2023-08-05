import os

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# README as the long description
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

REQUIREMENTS = [i.strip() for i in open('requirements.txt').readlines()]
tests_require = [
    # 'pytest',
]

setup(name='env-yaml',
      version=os.getenv('RELEASE_VERSION'),
      # setup_requires=['setuptools_scm'],
      description='Provides a yaml loader which substitutes '
                  'environment variables and supports defaults',
      long_description=long_description,
      long_description_content_type='text/markdown',

      url='https://github.com/iamKunal/env-yaml-python',
      author='Kunal Gupta',

      packages=find_packages(),

      tests_require=tests_require,
      extras_require={
          'test': tests_require,
      },
      # test_suite='pytest.collector',
      install_requires=REQUIREMENTS,

      include_package_data=True,
      package_dir={'': 'src'},
      )
