import sys, os
import shutil
from colorama import init
from termcolor import colored


def preparing_output(args):
    """
    preparing the output folder for create package
    :param args: command line args
    :type: argparse.Namespace
    :return: the output dir route
    :type: str
    """
    output_dir = os.popen("pwd").read().rstrip("\n\r")
    if str(args.output).startswith("./"):
        output_dir = os.path.join(output_dir, str(args.output).replace("./", ""))
    elif str(args.output) != '.':
        output_dir = args.output
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    if os.path.exists(os.path.join(output_dir, args.package)):
        shutil.rmtree(os.path.join(output_dir, args.package))
    os.mkdir(os.path.join(output_dir, args.package))
    os.mkdir(os.path.join(output_dir, args.package, args.package))
    asd = os.path.join(output_dir, args.package, args.package, "__init__.py")
    os.system("touch " + asd)
    return str(output_dir)
