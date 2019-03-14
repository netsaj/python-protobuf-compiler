import sys, os
import shutil
from colorama import init
from termcolor import colored


def define_input(proto_input_dir,git_repository_url,git_repository_token):
    """
    :param args: command line args
    :type args: argparse.Namespace
    :return: route of the inputdir
    :type: str
    """
    input_dir = proto_input_dir

    # cloning repository

    if git_repository_url != '':
        command = ''
        if str(git_repository_url).lower().find("gitlab") != -1:
            command = "git clone https://oauth2:" + git_repository_token + "@" + str(git_repository_url).replace("https://",
                                                                                                    "").replace(
                "http://", "")
        elif str(git_repository_url).lower().find("github") != -1:
            command = "git clone https://" + git_repository_token + "@" + str(git_repository_url).replace("https://", "").replace(
                "http://", "")
        if (command == ''):
            raise ValueError('only support gitlab and github repositories')
        print(command)
        out = os.system(command + " proto_temp")
        # change input dir for clone dir
        input_dir = os.path.join(os.getcwd(), "proto_temp")
    else:
        input_dir = os.popen("pwd").read().rstrip("\n\r")
        if str(proto_input_dir).startswith("./"):
            input_dir = os.path.join(input_dir, str(proto_input_dir).replace("./", ""))
        elif str(proto_input_dir) == '.':
            raise ValueError('-d , --dir   args not target to root folder, locate proto \
files in a subfolder. example: ./myProtos')
        else:
            input_dir = proto_input_dir
    return str(input_dir)
