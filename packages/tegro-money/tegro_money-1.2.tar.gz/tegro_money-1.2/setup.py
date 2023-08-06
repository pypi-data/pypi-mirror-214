from setuptools import setup

setup(
    name='tegro_money',
    version='1.2',
    description='TegroMoneyParser - module for working with tegro.money API',
    long_description='TegroMoneyParser - module for working with https://tegro.money API \nMade by @PyDevNik',
    packages=['tegro_money'],
    install_requires=[
        'requests', 'typing', 'pydantic'
    ],
)