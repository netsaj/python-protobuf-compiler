#!/usr/bin/python3
# app version
__version__ = "1.0.18"  # type: str

import os
import shutil
from colorama import init
from termcolor import colored
from argparse import ArgumentParser

# use Colorama to make Termcolor work on Windows too
init()

# functions imports
from protobuf_compiler.output_folder import preparing_output
from protobuf_compiler.input_folder import define_input
from protobuf_compiler.args_validation import args_validation

# global vars
packages = [];
packages_no_added = set()
package_name = ''
package_version = ''
input_dir = ''
output_dir = ''
git_repository = ''
git_repository_token = ''

def main():
    """
    app main
    :return:
    """
    parser = ArgumentParser(
        prog="protopy.py",
        description='Compile all protobuf files and create a single package \
        distribution for can be installed with pip. app version: ' + __version__

    )
    parser.add_argument("-d", "--dir", dest="origin",
                        help="folder path where the .proto files are located, can be relative \
                        ./protos or absolute /path/to/protos", metavar="PROTO_DIR", default=os.getcwd())
    parser.add_argument("-p", "--package", dest="package", default="1.0.0",
                        help="build package name", metavar="PACKAGE_NAME")
    parser.add_argument("-o", "--output", dest="output", default=".",
                        help="output folder for save single package .tar.gz, can be relative \
                        ./dist or absolute /path/to/dist", metavar="OUTPUT_DIR")
    parser.add_argument("-g", "--git", dest="repository",
                        help="git reopsitory clone http url where the .proto files are located", metavar="URL",
                        default="")
    parser.add_argument("-t", "--token", dest="token",
                        help="github or gitlab auth api token", metavar="TOKEN",
                        default="")
    parser.add_argument("-v", "--version", dest="version", default="1.0.0",
                        help="tag version for build pacakge", metavar="VERSION")
    parser.add_argument("-env", "--envars", dest="envars", default="false",
                        help="load inputs from envars \n\
                        -d=PROTO_INPUT_DIR \
                        -o=PROTO_OUTPUT_DIR \
                        -g=PROTO_GIT_REPO_URL \
                        -t=PROTO_GIT_REPO_TOKEN \
                        -v=PROTO_PACKAGE_VERSION \
                        -p=PROTO_PACKAGE_NAME)", metavar="true")


    args = parser.parse_args()
    if args.envars is not None and str().lower() == "true":
        package_name = os.getenv("PROTO_PACKAGE_NAME", "")
        package_version = os.getenv("PROTO_PACKAGE_VERSION", "")
        git_repository = os.getenv("PROTO_GIT_REPO_URL", "")
        git_repository_token = os.getenv("PROTO_GIT_REPO_TOKEN", "")
        input_dir = define_input(os.getenv("PROTO_INPUT_DIR", ""), git_repository, git_repository_token)
        output_dir = preparing_output(os.getenv("PROTO_OUTPUT_DIR", ""), package_name)
    else:
        # define package name
        package_name = args.package
        # define package version
        package_version = args.version
        # define the input dir
        input_dir = define_input(args.origin, args.repository, args.token)
        print(colored("* input dir: ", "yellow"), input_dir)
        # define the output dir
        output_dir = preparing_output(args.output, package_name)
        print(colored("* output dir: ", "green"), output_dir)
        git_repository_token = args.token
        git_repository = args.repository

    args_validation(git_repository=git_repository,
                    proto_input_dir=input_dir,
                    proto_output_dir=output_dir,
                    proto_package_version=package_version,
                    git_repository_token=git_repository_token)

    errors = 0
    files=[]
    for r, d, f in os.walk(input_dir):
        for file in f:
            if ".proto" in file.lower():
                files.append(os.path.join(r, file))
    for f in files:
        file_name = f.split(os.path.sep)[-1]
        folder = f.replace(file_name,"").replace(input_dir + os.path.sep, "")
        command = "python3 -m grpc_tools.protoc -I. \
                                 --proto_path=" + input_dir + " \
                                 --python_out=" + os.path.join(output_dir, package_name) + " \
                                 --grpc_python_out=" + os.path.join(output_dir, package_name) + " \
                                " + f
        os.system("touch __init__.py")
        out = os.system(command)
        if out == 0:
            packages.append(folder.replace(os.path.sep, ".").replace("-", "_"))
            asd = os.path.join(output_dir, package_name, folder.replace("-", "_"),
                               "__init__.py")
            os.system("touch " + asd)
            # print("DONE: ", os.path.join(input_dir, folder, file))
        else:
            errors += 1
            packages_no_added.add(folder.replace("-", "_"))
    with open(os.path.join(output_dir, package_name, "setup.py"), "+w") as setup:
        setup.write("""
from setuptools import setup

setup(
    name='""" + package_name + """',
    version='""" + package_version + """',
    packages=""" + str(packages) + """,
    url='github.com/netsaj',
    license='ISC',
    author='internal',
    author_email='me@localhost',
    description=''
)
        """)
    command = "cd " + os.path.join(output_dir, package_name) + " && python3 setup.py sdist"
    out = os.system(command)
    # print(out)
    if args.repository != '':
        shutil.rmtree(os.path.join(input_dir))
    if errors > 0:
        print("compilation done with ", errors, " errors")
        if len(packages_no_added) > 0:
            print("modules no added in package:\n", packages_no_added)
    final_file = os.path.join(output_dir, package_name + "-" + package_version + ".tar.gz")
    shutil.copyfile(
        os.path.join(output_dir, package_name, "dist", package_name + "-" + package_version + ".tar.gz"),
        final_file
    )
    shutil.rmtree(os.path.join(output_dir, package_name))
    print(colored("package dist save in:\n", "green"), final_file)
    print(colored("install with:\n", "green"), colored("pip3 install", "yellow"), final_file)


if __name__ == "__main__":
    main()
