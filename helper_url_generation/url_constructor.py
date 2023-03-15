import argparse
import os
from os.path import exists, basename, splitext
import re 
import json
import configparser
import frontmatter
import requests
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

def process_frontmatter_title(str):
    #remove leading and trailing whitespace
    str = str.strip()
    # converting the string to lower case
    str = str.lower()
    # finding all non-alphanumeric characters
    non_word = re.findall(r'\W',str)
    # removing the whitespace character from the ones that are found and
    # removing duplicates
    non_word_chars = list(set(filter(lambda r: not(r == " " or r == "-"), non_word)))
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
    title = md.metadata.get('title', None)
    if title:
        title = "blog/" + process_frontmatter_title(title)
    return title

def generate_non_blog_url(path, content_path = "content/"):
    url = None
    file_basename = basename(path)
    filename = splitext(file_basename)[0]
    if filename == "_index":
        url = path.split(file_basename)[0].split(content_path)[1]
    else:
        url = splitext(path)[0].split(content_path)[1]
    return url



def set_args():
    """CLI"""
    parser = argparse.ArgumentParser(
                    description="Generate urls")
    parser.add_argument('-r', '--repo', help='Path to repository containing the files', type=lambda s:check_path(parser,s, "dir"), required=True)
    parser.add_argument('-cf', '--config-filename',  help='Filename for config init', type=lambda s:check_path(parser,s, "file"), required=True)
    parser.add_argument('-chk', '--check-urls-only',  help='Runs a check on the pid file to make sure the urls resolve. Does not generate the urls', action='store_true')
    args = parser.parse_args()
    return args

def generate_urls(repo_path, domain, file):
    try:
        with open(file, "r+") as f:
            records = json.load(f)
            for record in records:
                page_url = None
                if "/blog/" in record['file']:
                    filepath = repo_path + "/" + record['file']
                    page_url = generate_blog_url(filepath)
                else:
                    page_url = generate_non_blog_url(record['file'])
                if page_url:
                    record['url'] = domain + "/" + page_url
                else:
                   record['url'] = page_url
            f.seek(0)
            f.truncate()
            json.dump(records, f)
    except Exception as e:
        raise (f"Error processing url generation: {e}")
    

def read_config(config_file_name):
    c = configparser.ConfigParser()
    try:
        c.read(config_file_name)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
    pid_file = c['DEFAULT']['pid_file']
    domain = c['DEFAULT']['domain']
    return [pid_file, domain]

def read_pid_file(file):
    records = None
    try:
        with open(file, "r") as f:
            records = json.load(f)
    except Exception as e:
        raise (f"ERROR: {e}")
    return records

def check_urls(pidfile):
    records = read_pid_file(pidfile)
    bad_url_status = {}
    for r in records:
        request = None
        if r['url']:
            try:
                request = requests.get(r['url'])
                if not(request.ok):
                    bad_url_status[r['file']] = {"url": r['url'], "status": request.status_code, "reason": request.reason}
            except Exception as e:
                raise (f"Error occurred on request: {e}")
    return bad_url_status
            
    
# this script can be run after the files are initialized
def main():
    args = set_args()
    [pid_file, domain] = read_config(args.config_filename)
    pid = args.repo + "/" + pid_file
    if not(args.check_urls_only):
        generate_urls(args.repo, domain, pid)
    bad_url_status = check_urls(pid)
    if bad_url_status:
        for file, info in bad_url_status.items():
            print(f"For {file}: {info}")
            sys.exit(1)


if __name__ == "__main__":
    main()