from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'pydfe development version'
LONG_DESCRIPTION = 'pydfe development version long description.'

# Setting up
setup(
    name="test4957",
    version=VERSION,
    author="Nate Mauney",
    author_email="<nmauney4@uncc.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={
        'pypdfe': ['pypdfe/*']
    },
    install_requires=['numpy'], # required python packages (autoinstalls them)
    keywords=['python', 'PDF'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)