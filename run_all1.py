import yaml
import sys
import re
import os
from os.path import exists
import argparse
import helpers.static_page_id as sp
from datetime import datetime
import helpers.git_info as g
import helpers.config_file as cf
import helpers.utilities as u
import warnings
import id
import helper_url_generation.url_constructor as uc
from submit_files import create_xml_files, submit_files
import check_doi_urls
import add_doi
import time

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

def set_args(argv):
    s = sp.static_page_id()
    default_config_filename = s.default_config_filename
    default_pid_filename = s.default_pid_json_filename
    default_id_types = s.default_id_types
    submission_types = ["crossref", "custom"]
    parser = argparse.ArgumentParser(description='Generates and parses YAML file with all values needed for scripts. Runs all necessary scripts')
    parser.add_argument("-cf", "--conf-file",  help="Name of config yml file. This file will be saved to the root of the repository", default="config.yml")
    parser.add_argument('-r', '--repo', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-st', '--st-type', help='Type of submission protocol', choices=submission_types, default="crossref")
    parser.add_argument('--info', help='Submission information, for crossref, please enter path to the submittor information yml file', default="submission_info.yml")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-i', '--init', action='store_true',help="Create pid and config files")
    group.add_argument('-b', '--batch', action='store_true', help='initialize static pages; batch process. This adds the x-version tag to pages in a specified path and commits them to the specified repository')
    init_subcommand, _ = parser.parse_known_args(argv)
    init_parser = argparse.ArgumentParser(
        description="Generate a permanent ID for a static site generator", parents=[parser], add_help=False)
    if init_subcommand.init:
        init_parser.add_argument('-p', '--pid-file', default=default_pid_filename, type=str, help="Json file that keeps track of the files, stored relative to the root of the repository")
        init_parser.add_argument('-d', '--domain', help='Production domain of the content, for example: https://www.crossref.org/', required=True)
        init_parser.add_argument('-c', '--content', type=str, required=True, nargs='+', help="Examples: -c filepath1 filepath2; relative to the repository root")
        init_parser.add_argument('-id', '--id-type', default="doi")
        init_parser.add_argument('--doi-prefix', required=True, help="Add doi prefix string to this argument, example: --doi-prefix 'x.xxx'")
    
    args = init_parser.parse_args(argv)
    return args

def create_yaml(args, config_file):
    # creating a dictionary out of args object
    orig_yaml_dict = vars(args)
    yaml_dict = orig_yaml_dict.copy()
    # remove keys not to be tracked in conf file
    #remove_keys = ['batch_process', 'localhost_check']
    remove_keys = ['batch', 'conf_file', 'init', 'st_type', 'info']
    for r in remove_keys:
        yaml_dict.pop(r)
    try:
        with open(config_file, 'w') as c:
            yaml.safe_dump(yaml_dict, c)
    except Exception as e:
        raise(e)
    else:
        print(f"Config file created: {config_file}")

def process_config_pid_files(full_config_filename, args):
    c = cf.ConfigFile(args.repo, args.pid_file, args.conf_file)
    files = []
    if not(exists(full_config_filename)):
        create_yaml(args, full_config_filename)
        files.append(full_config_filename)
    else:
        warnings.warn(f"{full_config_filename} exists and will not be overwritten")
    
def main(argv = None):
    args = set_args(argv)
    print(args)
    config_file = os.path.join(args.repo, args.conf_file)
    if args.init:
        content_paths = list(map(lambda x: os.path.join(args.repo, os.path.normpath(x)), args.content))
        msg = [p for p in content_paths if not(exists(p))]
        if msg:
            raise ValueError(f"Paths provided: {msg} do not exist. Cannot process further")
        process_config_pid_files(config_file, args)
        print(f"Init SUCCESS")
    elif not(exists(config_file)):
        raise ValueError(f"{config_file} must exist for future processing. Please re-initialize script")
    else:
        config = u.read_all_config(config_file)
        pid_file = os.path.join(config['repo'], config['pid_file'])
        if not(exists(pid_file)):
            raise ValueError(f"{pid_file} must exist for future processing. Please re-initialize script")
        # run id.py
        content_args = ['--content']
        for i in config['content']:
            content_args.append(i)
        id_args = content_args + ['--repo', config['repo'], '--config-filename', args.conf_file]
        if args.batch:
            id_args.append('-b')
        id.main(id_args)
        if args.st_type == "crossref":
            url_gen = ['--repo', config['repo'], '--config-filename', config_file]
            uc.main(url_gen)
            submission_info = args.info
            default_xml_filename = datetime.now().strftime("%Y%m%d%H%M%S") + "_submission.xml"
            try:
                with open(submission_info, 'r') as y:
                    data = yaml.safe_load(y)
            except Exception as e:
                raise ValueError(f"ERROR: {e}")
            xml_file = os.path.join(config['repo'],os.path.normpath(data['submission_path']), default_xml_filename)
            xml_file = '/Users/eshadatta/tiny_static_site/xml_submission/20230920155006_submission.xml'
            xml_args = ['-p', pid_file, '-b', data['batch_id'], '-dn', data['depositor'][0]['name'],'-de', data['depositor'][1]['email'], '-re', data['registrant'], '-f', xml_file]
            create_xml_files.main(xml_args)
            username, password, deposit_endpoint = os.environ['username'], os.environ['password'], os.environ['test_deposit']
            submit_args = ['-f', xml_file, '-pid', pid_file, '-u', username, '-p', password, '-e', deposit_endpoint]
            submit_files.main(submit_args)
            check_doi_args = ['--repo', config['repo'], '-p', pid_file]
            time.sleep(300)
            k = check_doi_urls.main(check_doi_args)
            if k: 
                print(k)
            add_doi_args = ['--repo', config['repo'], '-f', pid_file]
            add_doi.main(add_doi_args)
            
   

if __name__ == '__main__':
    main()
