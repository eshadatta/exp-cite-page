import os
from os.path import exists
import argparse
import frontmatter
import json
from git import Repo
import warnings

def read_markdown_file(file):
    try:
        markdown_file = frontmatter.load(file)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
    return markdown_file

def commit_file(repo_path, file):
    repo = Repo(repo_path)
    git = repo.git
    file = os.path.normpath(repo_path) + "/" + file
    comment = "Adding doi"
    try:
        git.commit("-m", comment, file)
    except Exception as e:
        raise(f"ERROR: {e}")
    else:
        print(file, " committed")

def write_content_file(file_path, markdown):
    try:
        with open(file_path, 'w') as m:
            m.write(frontmatter.dumps(markdown, handler=markdown.handler))
    except Exception as e:
        raise(f"ERROR: {e}")
    else:
        print("Added DOI: ", file_path)

def check_path(parser, p, type=None):
    if not(exists(p)):
        parser.error(f"{p} needs to exist")
    elif type == "file" and not(os.path.isfile(p)):
        parser.error(f"{p} needs to be a file")
    return os.path.normpath(p)


def set_args(argv):
    parser = argparse.ArgumentParser(
                    description="Add DOIs to markdown files")
    parser.add_argument('-f', '--pid-file', help='Path and name of pid file', type=lambda p:check_path(parser,p, 'file'), required=True)
    parser.add_argument('-r', '--repo', help='Path of repository containing static pages', type=lambda p:check_path(parser,p), required=True)
    args = parser.parse_args(argv)
    return args

def get_registered_pids(file):
    ids = None
    try:
        with open(file, 'r') as f:
            ids = json.load(f)
    except Exception as e:
        print(e)
    
    registered_ids = list(filter(lambda x: x['doi']['registered'], ids))
    return registered_ids

def add_dois(dir, submitted_dois):
    for d in submitted_dois:
        file = dir + "/" + d['file']
        md = read_markdown_file(file)
        doi_value = md.metadata.get('DOI', None)
        # if there is no doi value
        if not(doi_value):
            md.metadata['DOI'] = d['doi']['value']
            write_content_file(file, md)

def main(argv=None):
    args = set_args(argv)
    dirname = os.path.normpath(args.repo)
    d = get_registered_pids(args.pid_file)
    if d:
        add_dois(dirname, d)
    else:
        warnings.warn("No dois were registered. Unable to update site with DOIs")


if __name__ == "__main__":
    main()