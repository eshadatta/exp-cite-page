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
    if not(file_commit_id):
        raise ValueError(f"File {args.file} must be tracked in the git repository: {args.repo} in the specified branch: {branch} to continue processing")
    utc_datetime = g.commit_date(file_commit_id)
    return [file_commit_id, utc_datetime]

def add_pid(pid, commit_id, utc_datetime, args):
    path = os.path.normpath(args.repo)
    file_path = args.file.split(path+"/")[1]
    id = {"git_commit_id": commit_id, "current_id": pid, "file": file_path, "utc_commit_date": utc_datetime}
    if (exists(args.pid_file_path)):
        if not(os.path.isfile(args.pid_file_path)):
            raise ValueError(f"{args.pid_file_path} must be a json file")
        else:
            # handle file processing
            contents = []
            try:
                with open(args.pid_file_path, "r") as outfile:
                    contents.append(json.load(outfile))
            except Exception as e:
                raise IOError(f"Error reading file: {e}")
            try:
                with open(args.pid_file_path, "w") as outfile:
                    contents.append(id)
                    json.dump(contents, outfile)
            except Exception as e:
                raise IOError(f"Error writing to file: {e}")
    elif not(exists(args.pid_file_path)):
        try:
            with open(args.pid_file_path, "w") as outfile:
                json.dump(id, outfile)
        except Exception as e:
            raise IOError(f"Error writing to file: {e}")

def main():
    args = set_args()
    [commit_id, utc_datetime] = git_info(args)
    id = gid.GenID().gen_default()
    add_pid(id, commit_id, utc_datetime, args)
    # error handling for untracked file - done
    # get file's most recent commit id - done
    # create a pid id - done
    # create a json file, if one doesn't exist for pids - done
    # if json file does exist, check to see if the file w/ pid exists in the file and update it.
    # Else create an entry - done
    # Do the entries need their own key? Like a unique id of their own?



if __name__ == "__main__":
    main()