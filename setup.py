import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='protobuf_compiler',
    version='1.0.0',
    packages=['protobuf_compiler'],
    url='https://github.com/netsaj/python-protobuf-compiler',
    license='ISC',
    long_description=README,
    author='Fabio Moreno',
    author_email='fabiomoreno@outlook.com',
    description='compile all protobuf files and create a single package distribution for can be installed with pip',
classifiers=[
        "License :: ISC",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=[
        'grpcio==1.18.0',
        'grpcio-tools==1.18.0',
    ],
    entry_points={
        'console_scripts': [
            'protopy = protobuf_compiler.main:main',
        ],
    },
)
