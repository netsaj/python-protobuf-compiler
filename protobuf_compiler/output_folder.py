import sys, os
import shutil
from colorama import init
from termcolor import colored


def preparing_output(proto_output_dir, proto_package_name):
    output_dir = os.popen("pwd").read().rstrip("\n\r")
    if str(proto_output_dir).startswith("./"):
        output_dir = os.path.join(output_dir, str(proto_output_dir).replace("./", ""))
    elif str(proto_output_dir) != '.':
        output_dir = proto_output_dir
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if os.path.exists(os.path.join(output_dir, proto_package_name)):
        shutil.rmtree(os.path.join(output_dir, proto_package_name))
    os.mkdir(os.path.join(output_dir, proto_package_name))
    asd = os.path.join(output_dir, proto_package_name, "__init__.py")
    os.system("touch " + asd)
    return str(output_dir)
