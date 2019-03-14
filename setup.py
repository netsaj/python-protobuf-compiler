import pathlib
from setuptools import setup
from protobuf_compiler.main import __version__
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='protobuf_compiler',
    version=__version__,
    packages=['protobuf_compiler'],
    url='https://github.com/netsaj/python-protobuf-compiler',
    license='MIT',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Fabio Moreno',
    author_email='fabiomoreno@outlook.com',
    description='compile all protobuf files and create a single package distribution for can be installed with pip',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    install_requires=[
        'grpcio==1.18.0',
        'grpcio-tools==1.18.0',
        'colorama==0.3.3',
        'termcolor==1.1.0',
        'tqdm==4.31.1'
    ],
    entry_points={
        'console_scripts': [
            'protopy = protobuf_compiler.main:main',
            'protobuf-compiler = protobuf_compiler.main:main',
        ],
    },
    scripts=['protopy.py', 'protobuf-compiler.py']
)
