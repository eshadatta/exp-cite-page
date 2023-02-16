import git
import json
import hashlib
import uuid
import argparse
import os
from os.path import exists, basename
from git import Repo
import helpers.git_info as gi
import helpers.generate_id as gid
import helpers.process_json as pjson
import helpers.utilities as u
import sys

def check_path(parser, p, type='dir'):
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
    parser.add_argument('-r', '--repo', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-cf', '--config-filename', nargs='?', type=str, default = "static.ini", help='Filename for config init, has a default filename if none is specified')
    parser.add_argument('-d', '--dry-run', help='Dry run to generate a permanent ID of a specified file or files', action='store_true')
    args = parser.parse_args()
    return parser, args

def check_args(parser, file):
    if not(exists(file) and os.path.isfile(file)):
         parser.error(f"{file} needs to exist and/or be a file. Please run the following command to initialize the id generator: python init.py  -c [content-paths] -p pid-file-name.json -r repo-path")

def git_info(args):
    g = gi.GitInfo(args.repo)
    branch = args.branch if args.branch else g.active_branch
    [file_commit_id, git_hash] = g.get_file_commit_info(args.file, branch)
    utc_datetime = g.commit_date(file_commit_id)
    return [file_commit_id, git_hash, utc_datetime]

def check_config_args(config_args, arg_type=None):
    script_name = basename(__file__)
    method_name = check_config_args.__name__
    all_messages = []
    for k, v in config_args.items():
        if k == "pid_file":
            all_messages.append(u.check_path(v, "file"))
        elif k == "content_paths":
            for i in v:
                all_messages.append(u.check_path(i))
    
    messages = list(filter(lambda x: x is not None, all_messages))
    if messages:
        raise ValueError(f"From {script_name}.{method_name}: Cannot continue processing. See errors:{messages}")


def main():
    [parser, args] = set_args()
    config_file = args.repo + "/" + args.config_filename
    check_args(parser, config_file)
    [pid_file, content_paths] = u.read_config(config_file)
    full_paths = {}
    full_paths['pid_file'] = args.repo + "/" + pid_file
    full_paths['content_paths'] = list(map(lambda x: args.repo + "/" + x, content_paths))
    try:
        check_config_args(full_paths)
    except ValueError as e:
        print(e)
        sys.exit(1)
    
    
    

    # parse content paths to see what has changed to version different from what's listed in the pid json file. If file is not listed in the pid json file
    #[commit_id, git_hash, utc_datetime] = git_info(args)
    #id = gid.GenID().gen_default()
    #json_file = pjson.ProcessJson(args.repo, args.pid_file_path, args.file)
    #json_file.add_pid(id, commit_id, git_hash, utc_datetime)
   



if __name__ == "__main__":
    main()