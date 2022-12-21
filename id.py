import git
import json
import hashlib
import uuid
import argparse
import os
from os.path import exists
from git import Repo
import helpers.git_info as gi

def check_path(parser, p, type="file"):
    path_types = ["file", "dir"]
    if not(type in path_types):
        raise("error")
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
    parser.add_argument('-f', '--file', help='Path to file that requires the permanent ID; relative to the repository root', type=lambda s:check_path(parser,s, "file"), required=True)
    # if json file does not exist, one will be created
    parser.add_argument('-p', '--pid-file-path', help='Path to json file where containing all the information associated with the files and their permanent IDs; relative to the repository root. If the file does not exist, a new file with the specified filename will be created', required=True)
    parser.add_argument('-b', '--branch', help='Path to branch where the file is located. The default is the active branch of the repository')
    parser.add_argument('-d', '--dry-run', help='Dry run to generate a permanent ID of a specified file', action='store_true')
    args = parser.parse_args()
    return args

def git_info(args):
    g = gi.GitInfo(args.repo)
    branch = args.branch if args.branch else g.active_branch
    file_commit_id = g.get_file_commit_id(args.file, branch)
    print(g.active_branch)
    print(file_commit_id)
    if not(file_commit_id):
        raise ValueError(f"File {args.file} must be tracked in the git repository: {args.repo} in the specified branch: {branch} to continue processing")

def main():
    args = set_args()
    git_info(args)
    # error handling for untracked file - done
    # get file's most recent commit id - done
    # create a pid id
    # create a json file, if one doesn't exist for pids
    # if json file does exist, check to see if the file w/ pid exists in the file and update it.
    # Else create an entry
    # Do the entries need their own key? Like a unique id of their own?



if __name__ == "__main__":
    main()