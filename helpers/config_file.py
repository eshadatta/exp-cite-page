import configparser
import os
from os.path import exists
from pathlib import Path
import configparser
import ast

class ConfigFile:
    def __init__(self, content_path, pid_file, config_file_name = "static_pid_gen.ini"):
         self.c = configparser.ConfigParser()
         self.c['REPO'] = {"repo_path": "."}
         self.content_path = content_path
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
        paths = self.content_path
        for p in paths:
            if not(exists(p)):
                raise ValueError(f"content path: {p} must exist")

    def create_config(self):
        self.chk_content_paths()
        self.create_pid_file()
        self.c['DEFAULT'] = {'content_path': self.content_path, 'pid_file': self.pid_file}
        try:
            with open(self.config_file_name, "w") as cf:
                self.c.write(cf)
        except Exception as e:
            raise(f"ERROR: Could not create config file: {e}")

