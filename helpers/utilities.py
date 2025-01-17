import ast
import yaml
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

def dry_run_info(method_name, docstring):
    step = f"At {method_name}: {docstring}"
    print(step)


def get_major_version(version):
    return int(version.split(".")[0])

def check_path(path, type=None):
    msg = None
    if not(exists(path)):
        msg = f"ERROR: {path} must exist"
    else:
        if (type == "file") and not(isfile(path)):
            msg = f"ERROR: {path} must be a file"
    return msg

def read_config(config_file_name):
    msg = check_path(config_file_name)
    config = None
    if msg:
        raise RuntimeError(f"{config_file_name} must exist")
    try:
        with open(config_file_name, 'r') as y:
            config = yaml.safe_load(y)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
    
    doi_prefix = None
    keys = list(config.keys())
    id_type = config['id_type']
    pid_file = config['pid_file']
    if ('doi_prefix' in keys):
        doi_prefix = config['doi_prefix']
    domain = config['domain']
    return [pid_file, id_type, domain, doi_prefix]

def read_all_config(config_file_name):
    msg = check_path(config_file_name)
    config = None
    if msg:
        raise RuntimeError(f"{config_file_name} must exist")
    try:
        with open(config_file_name, 'r') as y:
            config = yaml.safe_load(y)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
    
    return config

# move this to config file class
def read_config2(config_file_name):
    msg = check_path(config_file_name)
    if msg:
        raise RuntimeError(f"{config_file_name} must exist")
    c = configparser.ConfigParser()
    try:
        c.read(config_file_name)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
     #when read, the list gets read as a string of a list - converting to a list
    doi_prefix = None
    keys = list(c['DEFAULT'].keys())
    id_type = c['DEFAULT']['id_type']
    pid_file = c['DEFAULT']['pid_file']
    if ('doi_prefix' in keys):
        doi_prefix = c['DEFAULT']['doi_prefix']
    domain = c['DEFAULT']['domain']
    return [pid_file, id_type, doi_prefix, domain]

def read_markdown_file(file):
    markdown_file = None
    try:
        markdown_file = frontmatter.load(file)
    except Exception as e:
        print(f"ERROR: {e}")
    return markdown_file

def get_file_list(content_path, dry_run):
    '''Gets file list from paths'''
    files = None
    if dry_run:
        dry_run_info(get_file_list.__name__, get_file_list.__doc__)
    else:
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
    if data:
        for d in data:
            file_version_info[d['file']] = {"version": d['version'], "url": d['url']}
    return file_version_info

def get_md_info(file, md, key):
    info = md.metadata.get(key, None)
    if not(info):
        raise ValueError(f"{file} must contain {key}")
    return info

def get_md_title(file, md, key='title'):
    ''' Gets title in frontmatter '''
    title = get_md_info(file, md, key)
    return title

def split_authors(author):
    info = {}
    split_name = author.split(" ")
    info['given_name'] = split_name[0]
    info['surname'] = split_name[-1]
    return info

def get_md_authors(file, md, key='authors'):
    ''' Gets author in frontmatter '''
    author_info = []
    existing_key = None
    if 'authors' in md.metadata.keys():
        existing_key = 'authors'
    elif 'author' in md.metadata.keys():
        existing_key = 'author'
    authors = get_md_info(file, md, existing_key)
    if isinstance(authors, str):
        authors = [authors]
    if authors:
        for i, v in enumerate(authors):
            sequence = "first" if i == 0 else "additional"
            split_author_name = split_authors(v)
            author_info.append({'name': v, 'sequence': sequence, "given_name": split_author_name['given_name'], "surname": split_author_name['surname']}) 
    return author_info

def check_file_versions(repo_path, pid_file, file_list, dry_run):
    '''gets a list of all files from given content paths and their versions from the pid file (if they exist) and generates a list of files to be pid-ized'''
    generate_dois = {}
    uninitialized_files = []
    if dry_run:
        dry_run_info(check_file_versions.__name__, check_file_versions.__doc__)
    else:
        initialized_files =  get_files_pid(pid_file)
        for f in file_list:
            md = read_markdown_file(f)
            if not md:
                print(f"WARNING: Not processing: {f}. There was an error or there is no markdown present")
                pass
            else:
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
                                title = get_md_title(f, md)
                                authors = get_md_authors(f, md)
                                generate_dois[f] = {"version": version, "url": initialized_files[relative_path]["url"], "title": title, "author_info": authors}
                            else:
                                print(f"For {f}: Version {major_version} can not be less than the previous version: {previous_major_file_version}. File will not be processed")
                    else:
                        # if file does not already exist in the pid file, it will be added to the list for id generation
                        title = get_md_title(f, md)
                        authors = get_md_authors(f, md)
                        generate_dois[f] = {"version": md.metadata[version_tag], "url": None, "title": md.metadata['title'], "author_info": authors}
                else:
                    uninitialized_files.append(f)
        # add file version to this
    return [generate_dois, uninitialized_files]


