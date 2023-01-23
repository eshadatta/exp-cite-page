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

def check_path(parser, p, type="file"):
    path_types = ["file", "dir"]
    if not(type in path_types):
        raise parser.error(f"type: {type} must be one of these: {path_types}")
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    elif type == "dir" and not(os.path.isdir(p)):
        parser.error(f"{p} needs to be a directory")
    return p

def set_args():
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Generate a permanent ID for a specific file")
    parser.add_argument('-r', '--repo', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    # if json file does not exist, one will be created
    parser.add_argument('-p', '--pid-file-path', help='Path to json file where containing all the information associated with the files and their permanent IDs; relative to the repository root. If the file does not exist, a new file with the specified filename will be created', required=True)
    parser.add_argument('-b', '--branch', help='Path to branch where the file is located. The default is the active branch of the repository')
    parser.add_argument('-dry', '--dry-run', help='Dry run to generate a permanent ID of a specified file', action='store_true')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--file', help='Path to file that requires to be initialized; relative to the repository root', type=lambda s:check_path(parser,s, "file"))
    group.add_argument('-d', '--dir', help='Path to directory that contains files to be initialized; relative to the repository root', type=lambda s:check_path(parser,s, "dir"))
    args = parser.parse_args()
    return args


def main():
    args = set_args()
    print(args)

if __name__ == "__main__":
    main()