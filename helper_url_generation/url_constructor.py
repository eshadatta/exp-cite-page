import argparse
import os
from os.path import exists, basename, splitext
import re 
import json
import frontmatter
import requests
import sys
import yaml

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

def process_frontmatter_title(str):
    #remove leading and trailing whitespace
    str = str.strip()
    # converting the string to lower case
    str = str.lower()
    # allow tokens
    allowed_tokens = ["."," ","-","/"]
    # finding all non-alphanumeric characters
    non_word = re.findall(r'\W',str)
    # removing the whitespace and hypen character from the non-alphanumeric characters that are found and
    # removing duplicates
    non_word_chars = list(set(filter(lambda r: not(r in allowed_tokens), non_word)))
    # replacing the non-alphanumeric chars found in the list with ""
    for i in non_word_chars:
        str = str.replace(i, "")
    # replacing whitespace with hyphen according to the hugo construction of urls
    str = re.sub(r'\s', '-', str)
    #sometimes multiple hyphens occur if there is a hypen already
    str = re.sub(r'\-+', "-", str)
    return str

def read_markdown_file(file):
    try:
        markdown_file = frontmatter.load(file)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
    return markdown_file

def generate_blog_url(path):
    md = read_markdown_file(path)
    slug = md.metadata.get('slug', None)
    aliases = md.metadata.get('aliases', None)
    title = md.metadata.get('title', None)
    real_url = None
    if slug:
        real_url = "blog/" + slug
    elif aliases:
        real_url = aliases
    if not(real_url) and title:
        real_url = "blog/" + process_frontmatter_title(title)
    return real_url

def generate_non_blog_url(path, content_path = "content/"):
    url = None
    file_name_special_cases = ["index", "_index"]
    file_basename = basename(path)
    filename = splitext(file_basename)[0]
    if filename in file_name_special_cases:
        url = path.split(file_basename)[0].split(content_path)[1]
    else:
        url = splitext(path)[0].split(content_path)[1]
    return url



def set_args(argv):
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Generate urls")
    parser.add_argument('-r', '--repo', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-cf', '--config-filename',  help='Full path to the config file', type=lambda s:check_path(parser,s, "file"), required=True)
    args = parser.parse_args(argv)
    return args

def generate_urls(repo_path, domain, file):
    try:
        with open(file, "r+") as f:
            records = json.load(f)
            for record in records:
                if not(record['url']):
                    page_url = None
                    if "/blog/" in record['file']:
                        filepath = repo_path + "/" + record['file']
                        page_url = generate_blog_url(filepath)
                    else:
                        page_url = generate_non_blog_url(record['file'])
                    if page_url:
                        record['url'] = domain + "/" + page_url
            f.seek(0)
            f.truncate()
            json.dump(records, f)
    except Exception as e:
        raise (f"Error processing url generation: {e}")
    

def read_config(config_file_name):
    config = None
    try:
        with open(config_file_name, 'r') as y:
            config = yaml.safe_load(y)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
    pid_file = config['pid_file']
    domain = config['domain']
    return [pid_file, domain]

def read_pid_file(file):
    records = None
    try:
        with open(file, "r") as f:
            records = json.load(f)
    except Exception as e:
        raise (f"ERROR: {e}")
    return records
    
# this script can be run after the files are initialized
def main(argv=None):
    args = set_args(argv)
    print("Generating URLs")
    [pid_file, domain] = read_config(args.config_filename)
    pid = os.path.normpath(args.repo) + "/" + pid_file
    generate_urls(args.repo, domain, pid)
   
if __name__ == "__main__":
    main()