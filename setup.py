from setuptools import setup

setup(
    name='protobuf_compiler',
    version='1.0.0',
    packages=['protobuf_compiler'],
    url='github.com/netsaj',
    license='ISC',
    author='Fabio Moreno',
    author_email='fabiomoreno@outlook.com',
    description='compile all protobuf files and create a single package distribution for can be installed with pip',
    install_requires=[
        'grpcio==1.18.0',
        'grpcio-tools==1.18.0',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'protopy = protobuf_compiler.main:main',
        ],
    },
)
