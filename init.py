import git
import json
import hashlib
import uuid
import argparse
import os
from os.path import exists
from git import Repo
import helpers.git_info as gi
import helpers.generate_id as gid
import helpers.config_file as cf
import helpers.initialize_files as i
import helpers.process_json as pjson
def check_path(parser, p, type='file'):
    path_types = ["file", "dir"]
    if not(type in path_types):
        raise parser.error(f"type: {type} must be one of these: {path_types}")
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    elif type == "dir" and not(os.path.isdir(p)):
        parser.error(f"{p} needs to be a directory")
    return os.path.normpath(p)

def set_args():
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Generate a permanent ID for a specific file")
    # if json file does not exist, one will be created
    parser.add_argument('-p', '--pid-file-path', help='Path to json file where containing all the information associated with the files and their permanent IDs; relative to the repository root. If the file does not exist, a new file with the specified filename will be created', required=True)
    parser.add_argument('-c', '--content', required=True, type=str, nargs='+', help="Examples: -c filepath1 filepath2, -c filepath3; relative to the repository root")
    parser.add_argument('-r', '--repo-path', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-cf', '--config-filename', nargs='?', type=str, default = "static.ini", help='Filename for config init, has a default filename if none is specified')
    parser.add_argument('-b', '--branch', help='Path to branch where the file is located. The default is the active branch of the repository')
    parser.add_argument('-dry', '--dry-run', help='Dry run to generate a permanent ID of a specified file', action='store_true')
    
    args = parser.parse_args()
    return args

def main():
    args = set_args()
    print(args)
    c = cf.ConfigFile(args.repo_path, args.content, args.pid_file_path, args.config_filename)
    c.create_config()
    # get list of markdown files
    file_list = c.get_file_list()
    init_files = i.InitializeFiles(args.repo_path, file_list, args.pid_file_path)
    # initializing these files with a first tag of the first version
    files = init_files.process_files()
    json_file = pjson.ProcessJson(args.repo_path, c.pid_file)
    json_file.initialize_pid_file(files)
if __name__ == "__main__":
    main()