#!/usr/bin/env python3
"""Details regarding the setup.

Details here

"""

from setuptools import setup
from setuptools.command.install import install as _install


class Install(_install):
    """Custom installer."""
    def run(self):
        """Installs the nltk modules."""
        _install.do_egg_install(self)
        import nltk
        nltk.download("omw")
        nltk.download("brown")


setup(
    name='tag-extractor',
    cmdclass={'install': Install},
    description='A tool to extract GIS from photo tag.',
    author='Martino Ferrari',
    author_email='manda.mgf@gmail.com',
    version='0.1.0',
    url='https://github.com/Mandarancio/tag-extractor',
    license='MIT',
    platforms=["any"],
    packages=['tagextractor'],
    install_requires=['requests', 'nltk', 'pyyaml', 'twitter', 'unidecode',
                      'flickrapi', 'SQLAlchemy', 'Owlready'],
    setup_requires=['nltk'],
    # Add test suite
    # Add entry point
    entry_points={
        'console_scripts': [
            'tagextractor = tagextractor.main:main'
        ],
    },
)
