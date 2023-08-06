from setuptools import setup, find_packages

setup(
    name='playlisterUtil',
    version='2.0.4',
    packages=find_packages(),
    install_requires=[
        'pymongo==4.3.3'
    ],
    author='Your Name',
    author_email='your@email.com',
    description='A description of your module',
)