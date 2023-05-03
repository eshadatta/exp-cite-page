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
    default_filename = s.default_config_filename
    parser = argparse.ArgumentParser(
                    description="Generate a permanent ID for a specific file")
    parser.add_argument('-r', '--repo', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-cf', '--config-filename', nargs='?', type=str, default = default_filename, help='Filename for config init, has a default filename if none is specified')
    parser.add_argument('-d', '--dry-run', help='Dry run to generate a permanent ID of a specified file or files', action='store_true')
    args = parser.parse_args()
    return parser, args

def check_args(parser, file):
    if not(exists(file) and os.path.isfile(file)):
         parser.error(f"{file} needs to exist and/or be a file. Please run the following command to initialize the id generator: python init.py  -c [content-paths] -p pid-file-name.json -r repo-path")

def git_info(args, info, files):
    g = gi.GitInfo(args.repo)
    base_version = sp.static_page_id().init_version
    branch = g.active_branch
    file_info = {}
    err_msg = {}
    for f, v in files.items():
        [file_commit_id, git_hash, err] = g.check_git_info(f, branch)
        if file_commit_id and git_hash:
            utc_datetime = g.commit_date(file_commit_id)
            filename = f.split(args.repo+"/")[1]
            if v['version'] == base_version:
                current_id = None
            else:
                current_id = gid.GenID().gen_default() 
            file_info[filename] = {"file_commit_id": file_commit_id, "file_hash": git_hash, "utc_commit_date": utc_datetime, "current_id": current_id, "version": v["version"], "url": v["url"], "file": filename}
        else:
            err_msg[f] = err
        
    if err_msg:
        print("ERRORS found in files to be processed:")
        for k, v in err_msg.items():
            print(f"For file {k}: {v}")
        raise AssertionError(f"Script will stop processing until errors are addressed")
    return file_info

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
    
    # removing all ok messages, i.e. None
    messages = list(filter(lambda x: x, all_messages))
    if messages:
        raise ValueError(f"From {script_name}.{method_name}: Cannot continue processing. See errors:{messages}")


def main():

    [parser, args] = set_args()

    config_file = args.repo + "/" + args.config_filename
    check_args(parser, config_file)
    [pid_file, content_paths, doi_prefix, production_domain] = u.read_config(config_file)
    full_paths = {}
    full_paths['pid_file'] = args.repo + "/" + pid_file
    full_paths['content_paths'] = list(map(lambda x: args.repo + "/" + x, content_paths))

    # verifying config args in ini file are ok
    try:
        check_config_args(full_paths)
         #gather files to be processed
        content_paths = full_paths['content_paths']
        file_list = u.get_file_list(content_paths)
        [gen_dois, unprocessed_files] = u.check_file_versions(args.repo, full_paths['pid_file'], file_list)
        print("UP: ", unprocessed_files)
        info = pjson.ProcessJson(args.repo, full_paths['pid_file'], doi_prefix, production_domain)
        fi = git_info(args, info.pid_entry, gen_dois)
        updated_files, rest_files = cleanup.cleanup(full_paths['pid_file'], fi)
        info.write_file_info(updated_files, rest_files)
    except Exception as e:
        print(e)
        sys.exit(1)

    #print("INFO FOR FILES TO BE PROCESSED: ", fi)
    #print(f"Files will not be processed from UNPROCESSED FILES: {unprocessed_files}")
'''
  for all files in content paths, 
  read frontmatter - DONE
  if x-version:
    process if x-version is > initialized - DONE

  processing x-version:
    if major version greater than base:
        check pid json file
            if in json file and current major version is greater than major version in json file: - DONE
                generate id. - DONE
                -Store other ids, in previous id and with git info related with it - NEED TO DO
        generated urls - DONEs
        if not in pid: - OUTPUTTING THIS INFO
'''
if __name__ == "__main__":
    main()