from setuptools import setup

setup(
    name='tegro_parser',
    version='1.0.1',
    description='TegroParser - module for working with tegro.money API',
    long_description='TegroParser - module for working with https://tegro.money API \nMade by @PyDevNik',
    packages=['tegro_parser'],
    install_requires=[
        'requests', 'typing'
    ],
)