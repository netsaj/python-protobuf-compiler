import os
from protobuf_compiler.input_folder import define_input


def args_validation(
        git_repository='',
        proto_input_dir='.',
        proto_output_dir='.',
        proto_package_version='',
        git_repository_token=''
):
    # repository defined
    if git_repository != '':
        if not str(git_repository).startswith("https://") and not str(git_repository).startswith("http://"):
            raise ValueError("-g , --git  : copy clone with https. example: https://gitlab.com/netsaj/test-repo.git")
        if str(git_repository).find("gitlab") == -1 and str(git_repository).find("github") == -1:
            raise ValueError("-g , --git  : git repository support for gitlab and github")

    if proto_input_dir == proto_output_dir:
        raise ValueError("src(-d) proto path need be different to output(-o) path ")

    if proto_package_version == '':
        raise ValueError("package name can't empty")

    if git_repository == '':
        input = define_input(proto_input_dir, git_repository, git_repository_token)
        contain_proto = False
        for file in get_list_of_files(input):
            if file.lower().endswith(".proto"):
                contain_proto = True
                break
        if not contain_proto:
            raise ValueError("src(-d) proto path not contain a proto files (*.proto)")


def get_list_of_files(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + get_list_of_files(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles
