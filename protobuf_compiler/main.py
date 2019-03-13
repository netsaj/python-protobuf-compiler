#!/usr/bin/python3
__version__ = "0.2.0"
import sys, os
import shutil
from colorama import init
from termcolor import colored
from argparse import ArgumentParser
# use Colorama to make Termcolor work on Windows too
init()

# functions imports
from protobuf_compiler.output_folder import preparing_output
from protobuf_compiler.input_folder import  define_input
from protobuf_compiler.args_validation import  args_validation


def main():
    parser = ArgumentParser(
        prog="protopy",
        description='compile all protobuf files and create a single package distribution for can be installed with pip'
    )
    parser.add_argument("-d", "--dir", dest="origin",
                        help="folder path where the .proto files are located, can be relative \
                        ./protos or absolute /path/to/protos", metavar="PROTO_DIR", default=os.getcwd())
    parser.add_argument("-p", "--package", dest="package", default="1.0.0",
                        help="build package name", metavar="PACKAGE_NAME")
    parser.add_argument("-o", "--output", dest="output", default=".",
                        help="output folder for save single package .tar.gz, can be relative \
                        ./dist or absolute /path/to/dist", metavar="OUTPUT_DIR", required=True)
    parser.add_argument("-g", "--git", dest="repository",
                        help="git reopsitory clone http url where the .proto files are located", metavar="URL", default="")
    parser.add_argument("-t", "--token", dest="token",
                        help="github or gitlab auth api token", metavar="TOKEN",
                        default="")
    parser.add_argument("-v", "--version", dest="version", default="1.0.0",
                        help="tag version for build pacakge", metavar="VERSION")
    args = parser.parse_args()

    args_validation(args)


    # define the input dir
    input_dir = define_input(args)
    print(colored("* input dir: ", "yellow"), input_dir)
    # define the output dir
    output_dir = preparing_output(args)
    print(colored("* output dir: ", "green"), output_dir)
    packages = [];
    packages_no_added = set()
    errors = 0
    for folder in (os.listdir(input_dir)):
        if os.path.isdir(os.path.join(input_dir, folder)):
            for file in os.listdir(os.path.join(input_dir, folder)):
                if file.lower().endswith(".proto"):
                    os.system("touch __init__.py")
                    command = "python3 -m grpc_tools.protoc -I. \
                         --proto_path=" + input_dir + " \
                         --python_out=" + os.path.join(output_dir, args.package, args.package) + " \
                         --grpc_python_out=" + os.path.join(output_dir, args.package, args.package) + " \
                        " + os.path.join(input_dir, folder, file)
                    out = os.system(command)
                    if out == 0:
                        packages.append(args.package + "." + folder.replace("-", "_"))
                        asd = os.path.join(output_dir, args.package, args.package, folder.replace("-", "_"),
                                           "__init__.py")
                        os.system("touch " + asd)
                        # print("DONE: ", os.path.join(input_dir, folder, file))
                    else:
                        errors += 1
                        packages_no_added.add(args.package + "." + folder.replace("-", "_"))
    with open(os.path.join(output_dir, args.package, "setup.py"), "+w") as setup:
        setup.write("""
from setuptools import setup

setup(
    name='""" + args.package + """',
    version='"""+args.version+"""',
    packages=""" + str(packages) + """,
    url='github.com/netsaj',
    license='ISC',
    author='internal',
    author_email='me@localhost',
    description=''
)
        """)
    command = "cd " + os.path.join(output_dir, args.package) + " && python3 setup.py sdist"
    out = os.system(command)
    #print(out)
    if args.repository != '':
        shutil.rmtree(os.path.join(input_dir))
    if errors > 0:
        print("compilation done with ",errors," errors")
        if len(packages_no_added)>0:
            print("modules no added in package:\n",packages_no_added)
    final_file = os.path.join(output_dir,args.package + "-" + args.version + ".tar.gz")
    shutil.copyfile(
        os.path.join(output_dir, args.package, "dist", args.package + "-" + args.version + ".tar.gz"),
        final_file
    )
    shutil.rmtree(os.path.join(output_dir,args.package))
    print(colored("package dist save in:\n", "green"),final_file)
    print(colored("install with:\n", "green"), colored("pip3 install", "yellow"), final_file)

if __name__ == "__main__":
    main()
