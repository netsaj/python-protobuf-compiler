#!/usr/bin/python3
__version__ = "0.2.0"
import sys, os
import shutil
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(
        prog="protopy",
        description='compile all protobuf files and create a single package distribution for can be installed with pip'
    )
    parser.add_argument("-d", "--dir", dest="origin",
                        help="folder path where the .proto files are located", metavar="PROTO_DIR", default=os.getcwd())
    parser.add_argument("-p", "--package", dest="package", default="1.0.0",
                        help="build package name", metavar="PACKAGE_NAME")
    parser.add_argument("-o", "--output", dest="output", default=".",
                        help="output folder for save single package .tar.gz", metavar="OUTPUT_DIR", required=True)
    parser.add_argument("-g", "--git", dest="repository",
                        help="git reopsitory url where the .proto files are located", metavar="URL", default="")
    parser.add_argument("-t", "--token", dest="token",
                        help="git server api token", metavar="TOKEN",
                        default="")
    parser.add_argument("-v", "--version", dest="version", default="1.0.0",
                        help="tag version for build pacakge", metavar="VERSION")
    args = parser.parse_args()
    input_dir = args.origin

    #cloning repository
    if args.repository != '':
        command = ''
        if str(args.repository).lower().find("gitlab")!=-1:
                command = "git clone https://oauth2:"+args.token+"@"+str(args.repository).replace("https://","").replace("http://","")
        elif str(args.repository).lower().find("github")!=-1:
                command = "git clone https://"+args.token+"@"+str(args.repository).replace("https://","").replace("http://","")
        if(command==''):
            raise ValueError('only support gitlab and github repositories')
        print(command)
        out = os.system(command+" proto_temp")
        #change input dir for clone dir
        input_dir=os.path.join(os.getcwd(),"proto_temp")

    output_dir = os.getcwd() if args.output == "." else args.output

    if os.path.exists(os.path.join(output_dir, args.package)):
        shutil.rmtree(os.path.join(output_dir, args.package))
    os.mkdir(os.path.join(output_dir, args.package))
    os.mkdir(os.path.join(output_dir, args.package, args.package))
    asd = os.path.join(output_dir, args.package, args.package, "__init__.py")
    os.system("touch " + asd)
    print("read main folder: ", input_dir)
    packages = [];
    packages_no_added = set()
    errors = 0
    for folder in (os.listdir(input_dir)):
        if os.path.isdir(os.path.join(input_dir, folder)):
            for file in os.listdir(os.path.join(input_dir, folder)):
                if file.lower().endswith(".proto"):
                    os.system("touch __init__.py")
                    out = os.system(
                        "python3 -m grpc_tools.protoc -I. "
                        "--proto_path=" + input_dir + "\
                         --python_out=" + os.path.join(output_dir, args.package, args.package) + " \
                         --grpc_python_out=" + os.path.join(output_dir, args.package, args.package) + " \
                        " + os.path.join(input_dir, folder, file))

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
    print("package dist save in:\n",final_file)
    print("install with:\npip3 install", final_file)

if __name__ == "__main__":
    main()
