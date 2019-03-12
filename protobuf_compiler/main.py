#!/usr/bin/python3
__version__ = "0.2.0"
import sys, os
import subprocess
import shutil
from argparse import ArgumentParser
from tqdm import tqdm


def main():
    parser = ArgumentParser(
        prog="protopy",
        description='compile all protobuf files and create a single package distribution for can be installed with pip'
    )
    parser.add_argument("-d", "--dir", dest="origin",
                        help="folder path where the .proto files are located", metavar="PROTO_DIR", default=os.getcwd())
    parser.add_argument("-p", "--package", dest="package", default="protobuf",
                        help="package name", metavar="PACKAGE_NAME")
    parser.add_argument("-o", "--output", dest="output", default=".",
                        help="output folder for save single package .tar.gz", metavar="OUTPUT_DIR")
    args = parser.parse_args()
    if args.help:
        parser.print_help()
        exit(0)
    output_dir = os.getcwd() if args.output == "." else args.output
    print(args)
    if os.path.exists(os.path.join(output_dir, args.package)):
        shutil.rmtree(os.path.join(output_dir, args.package))
    os.mkdir(os.path.join(output_dir, args.package))
    os.mkdir(os.path.join(output_dir, args.package, args.package))
    asd = os.path.join(output_dir, args.package, args.package, "__init__.py")
    os.system("touch " + asd)
    print("read main folder: ", args.origin)
    packages = [];
    errors = 0
    for folder in (os.listdir(args.origin)):
        if os.path.isdir(os.path.join(args.origin, folder)):
            for file in os.listdir(os.path.join(args.origin, folder)):
                if file.lower().endswith(".proto"):
                    packages.append(args.package + "." + folder.replace("-", "_"))
                    os.system("touch __init__.py")
                    out = os.system(
                        "python3 -m grpc_tools.protoc -I. "
                        "--proto_path=" + args.origin + "\
                         --python_out=" + os.path.join(output_dir, args.package, args.package) + " \
                         --grpc_python_out=" + os.path.join(output_dir, args.package, args.package) + " \
                        " + os.path.join(args.origin, folder, file))

                    if out == 0:
                        asd = os.path.join(output_dir, args.package, args.package, folder.replace("-", "_"),
                                           "__init__.py")
                        os.system("touch " + asd)
                        # print("DONE: ", os.path.join(args.origin, folder, file))
                    else:
                        errors += 1
    with open(os.path.join(output_dir, args.package, "setup.py"), "+w") as setup:
        setup.write("""
from setuptools import setup

setup(
    name='""" + args.package + """',
    version='1.0.0',
    packages=""" + str(packages) + """,
    url='github.com/netsaj',
    license='ISC',
    author='Fabio Moreno',
    author_email='fabiomoreno@outlook.com',
    description='',
    entry_points={
        'console_scripts': [
            'protopy = protobuf_compiler.main:main',
        ],
    },
)
        """)
    out = os.system("cd " + os.path.join(output_dir, args.package) + " && python3 setup.py sdist")
    print(out)
    if errors > 0:
        print("compilation done with ",errors," errors")
    print("package dist save in:\n",os.path.join(output_dir,args.package,"dist"))

if __name__ == "__main__":
    main()
