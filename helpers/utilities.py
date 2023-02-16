import ast
import configparser
import os
from os.path import exists, isfile
import frontmatter
from frontmatter.default_handlers import YAMLHandler, JSONHandler, TOMLHandler
from pathlib import Path

def check_path(path, type=None):
    msg = None
    if not(exists(path)):
        msg = f"ERROR: {path} must exist"
    else:
        if (type == "file") and not(isfile(path)):
            msg = f"{path} must be a file"
    return msg

def read_config(config_file_name):
    c = configparser.ConfigParser()
    try:
        c.read(config_file_name)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
     #when read, the list gets read as a string of a list - converting to a list
    content_path = ast.literal_eval(c['DEFAULT']['content_path'])
    pid_file = c['DEFAULT']['pid_file']
    return [pid_file, content_path]

def read_markdown_file(file):
    try:
        markdown_file = frontmatter.load(file)
    except Exception as e:
        raise ValueError(f"ERROR: {e}")
    return markdown_file

def get_file_list(content_path):
        file_list = []
        for p in content_path:
            if os.path.isdir(p):
                for i in Path(p).rglob('*.md'):
                    file_list.append(str(os.path.abspath(i)))
            elif os.path.isfile(p):
                file_list.append(p)
        return file_list