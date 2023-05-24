import ast
import configparser
import os
from os.path import exists, isfile
import frontmatter
from frontmatter.default_handlers import YAMLHandler, JSONHandler, TOMLHandler
from pathlib import Path
from itertools import chain
from . import static_page_id as s
import json
import sys 

sp = s.static_page_id()
base_version = sp.init_version
version_tag = sp.init_version_tag

def get_major_version(version):
    return int(version.split(".")[0])

def check_path(path, type=None):
    msg = None
    if not(exists(path)):
        msg = f"ERROR: {path} must exist"
    else:
        if (type == "file") and not(isfile(path)):
            msg = f"{path} must be a file"
    return msg

# move this to config file class
def read_config(config_file_name):
    c = configparser.ConfigParser()
    try:
        c.read(config_file_name)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
     #when read, the list gets read as a string of a list - converting to a list
    content_path = ast.literal_eval(c['DEFAULT']['content_path'])
    pid_file = c['DEFAULT']['pid_file']
    doi_prefix = c['DEFAULT']['doi_prefix']
    domain = c['DEFAULT']['domain']
    return [pid_file, content_path, doi_prefix, domain]

def read_markdown_file(file):
    try:
        markdown_file = frontmatter.load(file)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
    return markdown_file

def get_file_list(content_path):
    file_list = []
    not_found = []
    for p in content_path:
        f = []
        if os.path.isdir(p):
            # instead of hardcoding the md, use the asterisk and check if it's a file
            for i in Path(p).rglob('*.md'):
                f.append(str(os.path.abspath(i)))
        elif os.path.isfile(p):
            f.append(p)
        if not(f):
            not_found.append(p)
        else:
            file_list.append(f)
    if not_found:
        raise ValueError(f"ERROR: Stopping processing. No files found for {not_found}")
    files = list(chain(*file_list))
    return files

def get_files_pid(pid_file):
    file_version_info = {}
    try:
        with open(pid_file, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print("ERROR: ", e)
        sys.exit(1)

    for d in data:
        file_version_info[d['file']] = {"version": d['version'], "url": d['url']}
    return file_version_info
    
def check_file_versions(repo_path, pid_file, file_list):
    #get a list of all files and their versions from the pid file
    initialized_files =  get_files_pid(pid_file)
    generate_dois = {}
    uninitialized_files = []
    for f in file_list:
        md = read_markdown_file(f)
        base_major_version = get_major_version(base_version)
        # is the file initialized or does it have the tag
        if (version_tag in md.metadata):
            version = md.metadata[version_tag]
            major_version = get_major_version(version)
            relative_path = f.split(repo_path+"/")[1]
            # does the file being processed exist in the pid file
            if relative_path in initialized_files.keys():
                # is the version greater than the default version
                if major_version > base_major_version:
                    # get the existing version in the pid file
                    previous_major_file_version = get_major_version(initialized_files[relative_path]["version"])
                    # only checks if it is greater. There should eventually be some handling if for some reason the file has been deprecated or is lower than the previous version
                    if major_version > previous_major_file_version:
                        generate_dois[f] = {"version": version, "url": initialized_files[relative_path]["url"]}
            else:
                uninitialized_files.append({f: f"WARNING: Does not exist in {pid_file}. Version in file: {md.metadata[version_tag]}. File will still be processed"})
                generate_dois[f] = {"version": md.metadata[version_tag], "url": None}
 
        else:
            uninitialized_files.append({f: f"INFO: Does not contain the tag: {version_tag}. File is not initialized and will not be processed"})
    # add file version to this
    return [generate_dois, uninitialized_files]


