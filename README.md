# python protobuf compiler

compile all protobuf files and create a single package distribution for can be
installed with pip


## usage: 

protopy [-h] [-d PROTO_DIR] [-p PACKAGE_NAME] [-o OUTPUT_DIR]

### example:

* compile from git repository:

you can clone a git repository from gitlab and github
```bash
python3 -m protopy -o /my/target/dir -p testpackage -g https://github.com/netsaj/testing.git -t my-private-token
```

* compile from folder:

```bash
python3 -m protopy -o /my/output/dir -p testpackage -d /my/protofile/source/dir 
```


##  arguments:

* -h, --help : show this help message and exit
* -d PROTO_DIR, --dir PROTO_DIR : folder path where the .proto files are located
* -p PACKAGE_NAME, --package PACKAGE_NAME : package name
* -o OUTPUT_DIR, --output OUTPUT_DIR: output folder for save single package .tar.gz
* -g URL, --git URL : git reopsitory url where the .proto files are located
* -t TOKEN, --token TOKEN : git server api token
* -v VERSION, --version VERSION : tag version for build pacakge



## Authors:

* Fabio Moreno <fabiomoreno@outlook.com>