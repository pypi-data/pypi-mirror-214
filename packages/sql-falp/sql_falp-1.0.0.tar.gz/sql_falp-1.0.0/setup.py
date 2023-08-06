from setuptools import setup

setup(
    name='sql_falp',
    version='1.0.0',
    description='A package for falp sql databases connection',
    author='mespinoza',
    packages=['sql_falp'],
    install_requires=[
        'pandas',
        'sqlalchemy',
        'unidecode',
    ],
)
