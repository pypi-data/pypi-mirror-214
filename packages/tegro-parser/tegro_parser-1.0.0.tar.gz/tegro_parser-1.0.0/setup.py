from setuptools import setup

setup(
    name='tegro_parser',
    version='1.0.0',
    description='TegroParser - module for working with tegro.money API',
    packages=['tegro_parser'],
    install_requires=[
        'requests', 'typing'
    ],
)