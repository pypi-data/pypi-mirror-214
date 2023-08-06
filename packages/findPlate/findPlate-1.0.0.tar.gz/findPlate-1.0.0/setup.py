from setuptools import setup, find_packages
import codecs
import os


# Setting up
setup(
    name="findPlate",
    version='1.0.0',
    author="Guido Xhindoli",
    author_email="<mail@gmail.com>",
    description='A package finds the car plate',
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pandas==2.0.2",
        "openpyxl==3.1.2"
    ],
    keywords=[ 'SDAfindPlate', 'findPlate', 'find plate'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)