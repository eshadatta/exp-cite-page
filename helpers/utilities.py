import ast
import configparser
import os
from os.path import exists, isfile, isdir

def check_path(path, type=None):
    status = True
    msg = None
    print("PATH: ", path)
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