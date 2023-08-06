# create a Environment where my Package(Pandas-mypackage) work

from setuptools import setup , find_packages

setup(
    name = 'pandas_func' ,
    version = 0.01,
    description= "A Python package for performing simple function",
    author= "Nimra Shahzadi",
    author_email= 'mehernimra064@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.26.0',
    ],
)