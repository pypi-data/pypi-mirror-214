from re import L
from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.7'
DESCRIPTION = 'Microsoft Adaptive Cards'
LONG_DESCRIPTION = 'A package that helps you design adaptive cards in an object-oriented manner.'

setup(
    name="adaptivecard",
    version=VERSION,
    author="cabutchei (Luan Paz)",
    author_email="<luropa_paz@hotmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    keywords=['python', 'card', 'adaptive card', 'microsoft'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)