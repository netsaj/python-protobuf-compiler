# python protobuf compiler

compile all protobuf files and create a single package distribution for can be
installed with pip

## requirements

* python >= 3.6
* git (only for build from git repository)

## features
- [x] support for multiples folders
- [x] support multiples proto files
- [x] Create self package for pip
- [x] Support for build from github and gitlab repository
- [X] Support for build from local directory
- [X] support imports into proto file (see test folder for show example )

## install

```bash
pip3 install protobuf-compiler
```

for check install, execute in your terminal:

```bash
protopy -h
```

##  arguments

* -h, --help : show this help message and exit
* -d PROTO_DIR, --dir PROTO_DIR : folder path where the .proto files are located
* -p PACKAGE_NAME, --package PACKAGE_NAME : package name
* -o OUTPUT_DIR, --output OUTPUT_DIR: output folder for save single package .tar.gz
* -g URL, --git URL : git reopsitory url where the .proto files are located
* -t TOKEN, --token TOKEN : git server api token
* -v VERSION, --version VERSION : tag version for build package


## usage

```bash
protopy [-h] [-d PROTO_DIR] [-p PACKAGE_NAME] [-o OUTPUT_DIR]
```

### example

* compile from git repository:

you can clone a git repository from gitlab and github
```bash
python3 -m protopy -o /my/target/dir -p testpackage -g https://github.com/netsaj/testing.git -t my-private-token
```

* compile from folder:

```bash
python3 -m protopy -o /my/output/dir -p testpackage -d /my/protofile/source/dir 
```

## install generate package in your app

run in your app folder:

```bash
pip3 install /my/output/dir/package-version.tar.gz
```

### example:
* installing generate package:
```bash
pip3 install /Users/netsaj/temp/mytest-1.0.0.tar.gz
```

* import into you .py files:

```python
from mytest.analytics import analytics_pb2
```

## Authors

* Fabio Moreno <fabiomoreno@outlook.com>