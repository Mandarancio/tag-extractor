#!/usr/bin/env python3
"""Details regarding the setup.

Details here

"""

from setuptools import setup

setup(
    name='tag-extractor',
    description='A tool to extract GIS from photo tag.',
    author='Martino Ferrari',
    author_email='manda.mgf@gmail.com',
    version='0.1.0',
    url='https://github.com/Mandarancio/tag-extractor',
    license='MIT',
    platforms=["any"],
    packages=['tagextractor'],
    install_requires=['requests', 'nltk', 'pyyaml', 'twitter', 'unidecode',
                      'flickrapi'],
    # Add test suite
    # Add entry point
    # entry_points={
    #     'console_scripts': [
    #         'tagextractor = tagextractor.main:main'
    #     ],
    # },
)
