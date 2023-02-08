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
import helpers.process_json as pjson


def set_args():
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Generate a permanent ID for a specific file")
    parser.add_argument('-r', '--repo', help='Path to repository containing the files', required=True)
    parser.add_argument('-f', '--file', help='Path to file that requires the permanent ID; relative to the repository root', required=True)
    # if json file does not exist, one will be created
    parser.add_argument('-p', '--pid-file-path', help='Path to json file where containing all the information associated with the files and their permanent IDs; relative to the repository root. If the file does not exist, a new file with the specified filename will be created', required=True)
    parser.add_argument('-b', '--branch', help='Path to branch where the file is located. The default is the active branch of the repository')
    parser.add_argument('-d', '--dry-run', help='Dry run to generate a permanent ID of a specified file', action='store_true')
    args = parser.parse_args()
    return parser, args

def check_args(parser, args):
    if not(exists(args.repo) and os.path.isdir(args.repo)):
         parser.error(f"{args.repo} needs to exist and/or be a directory")
    else:
        args.repo = os.path.normpath(args.repo) + "/"
        file = args.repo + args.file
    if not(exists(file) and os.path.isfile(file)):
         parser.error(f"{file} needs to exist and/or be a file")
    return args

def git_info(args):
    g = gi.GitInfo(args.repo)
    branch = args.branch if args.branch else g.active_branch
    [file_commit_id, git_hash] = g.get_file_commit_info(args.file, branch)
    utc_datetime = g.commit_date(file_commit_id)
    return [file_commit_id, git_hash, utc_datetime]



def main():
    [parser, args] = set_args()
    args = check_args(parser, args)
    [commit_id, git_hash, utc_datetime] = git_info(args)
    id = gid.GenID().gen_default()
    json_file = pjson.ProcessJson(args.repo, args.pid_file_path, args.file)
    json_file.add_pid(id, commit_id, git_hash, utc_datetime)
    # error handling for untracked file - done
    # get file's most recent commit id - done
    # create a pid id - done
    # create a json file, if one doesn't exist for pids - done
    # if json file does exist, check to see if the file w/ pid exists in the file and update it.
    # Else create an entry - done
    # Entries key will the the commit and file name



if __name__ == "__main__":
    main()