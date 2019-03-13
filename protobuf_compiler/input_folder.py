import sys, os
import shutil
from colorama import init
from termcolor import colored


def define_input(args):
    """
    :param args: command line args
    :type args: argparse.Namespace
    :return: route of the inputdir
    :type: str
    """
    input_dir = args.origin

    # cloning repository

    if args.repository != '':
        command = ''
        if str(args.repository).lower().find("gitlab") != -1:
            command = "git clone https://oauth2:" + args.token + "@" + str(args.repository).replace("https://",
                                                                                                    "").replace(
                "http://", "")
        elif str(args.repository).lower().find("github") != -1:
            command = "git clone https://" + args.token + "@" + str(args.repository).replace("https://", "").replace(
                "http://", "")
        if (command == ''):
            raise ValueError('only support gitlab and github repositories')
        print(command)
        out = os.system(command + " proto_temp")
        # change input dir for clone dir
        input_dir = os.path.join(os.getcwd(), "proto_temp")
    else:
        input_dir = os.popen("pwd").read().rstrip("\n\r")
        if str(args.origin).startswith("./"):
            input_dir = os.path.join(input_dir, str(args.origin).replace("./", ""))
        elif str(args.origin) == '.':
            raise ValueError('-d , --dir   args not target to root folder, locate proto \
files in a subfolder. example: ./myProtos')
    return str(input_dir)
