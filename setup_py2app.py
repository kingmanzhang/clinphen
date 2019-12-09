import setuptools
from setuptools.command.develop import develop
from setuptools.command.install import install
import sys
import os

def post_install_script():
    import nltk
    nltk.download('wordnet')
    
class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        post_install_script()
        install.run(self)

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        post_install_script()
        develop.run(self)

with open("README.md", "r") as fh:
    long_description = fh.read()

#OPTIONS = {'argv_emulation': True,
#           'plist': {
#               'PyRuntimeLocations': [
#                '@executable_path/../Frameworks/libpython3.6m.dylib',
#                '~/anaconda/lib/libpython3.6m.dylib'
#               ]
#           }}
OPTIONS = {'iconfile': 'ClinPhen_Logo_small.icns'}


setuptools.setup(
    name='clinphen',
    version='1.26',
    app=['ClinPhenApp'],
    scripts=['clinphen', 'clinphen_bulk'],
    options={'py2app': OPTIONS},
    author="Cole A. Deisseroth",
    author_email="cdeisser@stanford.edu",
    description="An automatic phenotype extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://bejerano.stanford.edu/clinphen/",
    packages=setuptools.find_packages() + ['clinphen_src', 'appJar'],
    include_package_data=True,
    install_requires=['nltk==3.4', 'six==1.12.0', 'pandas==0.20.1'],
    setup_requires=['py2app'],
    classifiers=[
         "Programming Language :: Python :: 2.7",
         "Operating System :: OS Independent",
     ],
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
 )

