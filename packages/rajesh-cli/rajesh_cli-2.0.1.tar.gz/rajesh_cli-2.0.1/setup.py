from setuptools import setup, find_packages

setup(
    name='rajesh_cli',
    version='2.0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'rajesh_cli=src.cli:activate_cli',
        ],
    },
)
