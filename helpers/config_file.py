import configparser
import os
from os.path import exists, relpath
from pathlib import Path
from . import utilities as u
import sys

class ConfigFile:
    def __init__(self, repo_path, content_path, pid_file, config_file_name):
        self.c = configparser.ConfigParser()
        self.repo_path = repo_path
        self.relative_content_paths = content_path
        self.relative_pid_file = pid_file
        content_paths = list(map(lambda p: self.repo_path + "/" + p, content_path))
        config_file_name =  self.repo_path + "/" + config_file_name
        pid_file = self.repo_path + "/" + pid_file
        self.content_path = content_paths
        self.pid_file = pid_file
        self.config_file_name = config_file_name

    def create_pid_file(self):
        pid_file = self.pid_file
        if not(exists(pid_file)):
                try:
                    Path(pid_file).touch()
                except Exception as e:
                    raise ValueError(f"ERROR: {e}")
        elif (exists(pid_file) and os.path.isfile(pid_file)):
            print(f"{pid_file} already exists")
        else:
            raise ValueError(f"ERROR: please send a path with a filename and not path: {pid_file}")

    def chk_content_paths(self):
        script_name = relpath(__file__)
        method_name = self.chk_content_paths.__name__
        msg = list(map(u.check_path, self.content_path))
        # removing all ok messages, i.e. None
        messages = list(filter(lambda x: x, msg))
        if messages:
            raise ValueError(f"From {script_name}.{method_name}: Cannot continue processing. See errors:{messages}")

    def create_config(self, doi_prefix, domain):
        try:
            self.chk_content_paths()
        except ValueError as e:
            print(e)
            sys.exit(1)
        self.create_pid_file()
        self.c['DEFAULT'] = {'content_path': self.relative_content_paths, 'pid_file': self.relative_pid_file, "doi_prefix": doi_prefix, "domain": domain}
        try:
            with open(self.config_file_name, "w") as cf:
                self.c.write(cf)
        except Exception as e:
            raise(f"ERROR: Could not create config file: {e}")
        print(f"Config file: {self.config_file_name} created")

    def get_file_list(self):
        try:
            file_list = u.get_file_list(self.content_path)
        except ValueError as e:
            print(e)
            sys.exit(1)
        return file_list



