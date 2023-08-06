from setuptools import setup, find_packages

setup(
    name='playlisterUtil',
    version='2.0.1',
    packages=find_packages(),
    install_requires=[
        'pymongo==4.3.3'
    ],
)