from setuptools import setup, find_packages
import codecs
import os

NAME = 'test4957'
VERSION = '0.1.1'
DESCRIPTION = 'pydfe development version'
LONG_DESCRIPTION = 'pydfe development version long description.'

# Setting up
setup(
    name=NAME,
    version=VERSION,
    author="Nate Mauney",
    author_email="<nmauney4@uncc.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    # package_data={
    #     'pypdfe': [f'pypdfe/*']
    # },
    install_requires=['numpy'], # required python packages (autoinstalls them)
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)