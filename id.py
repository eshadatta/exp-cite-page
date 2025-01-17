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
import helpers.initialize_files as init_file


def check_path(parser, p, type='dir'):
    path_types = ["file", "dir"]
    if type not in path_types:
        raise parser.error(f"type: {type} must be one of these: {path_types}")
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    elif type == "dir" and not(os.path.isdir(p)):
        parser.error(f"{p} needs to be a directory")
    return os.path.normpath(p)

def set_args(argv):
    """CLI"""
    s = sp.static_page_id()
    default_config_filename = s.default_config_filename
    parser = argparse.ArgumentParser(
                    description="Generate a permanent ID for a specific file")
    parser.add_argument('-r', '--repo', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-c', '--content', required=True, type=str, nargs='+', help="Examples: -c filepath1 filepath2; relative to the repository root")
    parser.add_argument('-cf', '--config-filename', nargs='?', type=str, default = default_config_filename, help='Filename for config init, has a default filename if none is specified')
    parser.add_argument('-b', '--batch-process', help='initialize static pages; batch process. This only adds the x-version tag to pages in a specified path', action='store_true')
    parser.add_argument('-d', '--dry-run', help='Dry run to generate a permanent ID of a specified file or files', action='store_true')
    args = parser.parse_args(argv)
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
                doi = {"doi": {"submitted": None, "registered": None, "value": None}}
                file_info[filename] = {"file_commit_id": file_commit_id, "file_hash": git_hash, "utc_commit_date": utc_datetime, "current_id": current_id, "version": v["version"], "url": v["url"], "file": filename, "title": v['title'], "authors": v['author_info']}
                file_info[filename].update(doi)
            else:
                err_msg[f] = err
            
        if err_msg:
            print("ERRORS found in files to be processed:")
            for k, v in err_msg.items():
                print(f"For file {k}: {v}")
            raise AssertionError("Script will stop processing until errors are addressed")
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

def commit_pid(repo, file, processed_files):
    g = gi.GitInfo(repo)
    g.git_commit_file(file, comment=f"Updating file with IDs for {processed_files}")

def main(argv = None):
    [parser, args] = set_args(argv)
    config_file = args.repo + "/" + args.config_filename
    # verifying config args in ini file are ok
    [pid_file, id_type, production_domain, doi_prefix] = u.read_config(config_file)
    full_paths = {}
    full_paths['pid_file'] = args.repo + "/" + pid_file
    full_paths['content_paths'] = list(map(lambda x: args.repo + "/" + x, args.content))
    msg = [p for p in full_paths['content_paths'] if not(exists(p))]
    if msg:
        raise ValueError(f"Paths provided: {msg} do not exist. Cannot process further")
    print("Generating PID(s)")
    try:
        if args.dry_run:
            print("RUNNING DRY RUN:")
        check_args(parser, config_file, args.dry_run)
        check_config_args(full_paths, args.dry_run)
        #gather files to be processed
        content_paths = full_paths['content_paths']
        file_list = u.get_file_list(content_paths, args.dry_run)
        file_info = None
        if args.batch_process:
            print("RUNNING IN BATCH MODE")
            if args.dry_run:
                print("Initializing files and committing them")
            else:
                file_info = init_file.InitializeFiles(args.repo, file_list, full_paths['pid_file']).process_files()
        else:
            [gen_pids, unprocessed_files] = u.check_file_versions(args.repo, full_paths['pid_file'], file_list, args.dry_run)
            if not(gen_pids) and not(args.dry_run):
                print(f"There are no files to be processed in the given content paths: {args.content}")
            else:
                file_info = git_info(args, gen_pids, args.dry_run)
        if not(args.dry_run) and file_info:
            updated_files, rest_files = cleanup.cleanup(full_paths['pid_file'], file_info)
            if updated_files:
                info = pjson.ProcessJson(args.repo, full_paths['pid_file'], production_domain, doi_prefix)
                info.write_file_info(updated_files, rest_files)
                print(f"Files in {args.content} have been processed and written to {full_paths['pid_file']}")
            else:
                print(f"No updated files in {args.content}. Nothing was processed")
        elif args.dry_run:
            print("Generates a ProcessJSON object which contains path and domain information")
            print("Updates any PID information in the pid file, if the file already exists in the pid file or inserts PID information if the file is new")
    except Exception as e:
        print(e)
        sys.exit(1)
if __name__ == "__main__":
    main()
