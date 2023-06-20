import git
import json
import hashlib
import uuid
import argparse
import os
import json
from os.path import exists, basename
from git import Repo
import helpers.git_info as gi
import helpers.generate_id as gid
import helpers.process_json as pjson
import helpers.utilities as u
import sys
import helpers.static_page_id as sp
import helpers.cleanup as cleanup


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
    s = sp.static_page_id()
    default_config_filename = s.default_config_filename
    parser = argparse.ArgumentParser(
                    description="Generate a permanent ID for a specific file")
    parser.add_argument('-r', '--repo', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-c', '--content', required=True, type=str, nargs='+', help="Examples: -c filepath1 filepath2; relative to the repository root", default=".")
    parser.add_argument('-cf', '--config-filename', nargs='?', type=str, default = default_config_filename, help='Filename for config init, has a default filename if none is specified')
    parser.add_argument('-d', '--dry-run', help='Dry run to generate a permanent ID of a specified file or files', action='store_true')
    args = parser.parse_args()
    return parser, args

def check_args(parser, file, dry_run):
    '''Checks if config file has been created'''
    if dry_run:
        u.dry_run_info(check_args.__name__, check_args.__doc__)
    else:
        if not(exists(file) and os.path.isfile(file)):
            parser.error(f"{file} needs to exist and/or be a file. Please run the following command to initialize the id generator: python init.py -r repo-path -d domain")

def git_info(args, files, dry_run):
    '''Generate PID and git information for file to be saved in pid file'''
    file_info = {}
    if dry_run:
        u.dry_run_info(git_info.__name__, git_info.__doc__)
    else:
        g = gi.GitInfo(args.repo)
        branch = g.active_branch
        err_msg = {}
        for f, v in files.items():
            [file_commit_id, git_hash, err] = g.check_git_info(f, branch)
            if file_commit_id and git_hash:
                utc_datetime = g.commit_date(file_commit_id)
                filename = f.split(args.repo+"/")[1]
                current_id = gid.GenID().gen_default(len=10) 
                file_info[filename] = {"file_commit_id": file_commit_id, "file_hash": git_hash, "utc_commit_date": utc_datetime, "current_id": current_id, "version": v["version"], "url": v["url"], "file": filename}
            else:
                err_msg[f] = err
            
        if err_msg:
            print("ERRORS found in files to be processed:")
            for k, v in err_msg.items():
                print(f"For file {k}: {v}")
            raise AssertionError(f"Script will stop processing until errors are addressed")
    return file_info

def check_config_args(config_args, dry_run, arg_type=None):
    '''Checks if config values exist'''
    script_name = basename(__file__)
    method_name = check_config_args.__name__
    if dry_run:
        u.dry_run_info(method_name, check_config_args.__doc__)
    all_messages = []
    for k, v in config_args.items():
        if k == "pid_file":
            all_messages.append(u.check_path(v, "file"))
    
    # removing all ok messages, i.e. None
    messages = list(filter(lambda x: x, all_messages))
    if messages:
        raise ValueError(f"From {script_name}.{method_name}: Cannot continue processing. See errors:{messages}")

def main():
    [parser, args] = set_args()
    config_file = args.repo + "/" + args.config_filename
    print(args)
    [pid_file, id_type, doi_prefix, production_domain] = u.read_config(config_file)
    full_paths = {}
    full_paths['pid_file'] = args.repo + "/" + pid_file
    full_paths['content_paths'] = list(map(lambda x: args.repo + "/" + x, args.content))
    msg = [p for p in full_paths['content_paths'] if not(exists(p))]
    if msg:
        raise ValueError(f"Paths provided: {msg} do not exist. Cannot process further")
    # verifying config args in ini file are ok
    try:
        if args.dry_run:
            print("RUNNING DRY RUN:")
        check_args(parser, config_file, args.dry_run)
        check_config_args(full_paths, args.dry_run)
        #gather files to be processed
        content_paths = full_paths['content_paths']
        file_list = u.get_file_list(content_paths, args.dry_run)
        [gen_pids, unprocessed_files] = u.check_file_versions(args.repo, full_paths['pid_file'], file_list, args.dry_run)
        fi = git_info(args, gen_pids, args.dry_run)
        if not(args.dry_run):
            updated_files, rest_files = cleanup.cleanup(full_paths['pid_file'], fi)
            info = pjson.ProcessJson(args.repo, full_paths['pid_file'], production_domain, doi_prefix)
            info.write_file_info(updated_files, rest_files)
            print(unprocessed_files)
        elif args.dry_run:
            print("Generates a ProcessJSON object which contains path and domain information")
            print("Updates any PID information in the pid file, if the file already exists in the pid file or inserts PID information if the file is new")

    except Exception as e:
        print(e)
        sys.exit(1)
if __name__ == "__main__":
    main()
