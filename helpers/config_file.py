import configparser
import os
from os.path import exists, relpath, join
from pathlib import Path
from . import utilities as u
import sys
import json
import warnings
import yaml

class ConfigFile:
    def __init__(self, repo_path, pid_file, config_file_name, content_paths = None):
        self.c = configparser.ConfigParser()
        self.repo_path = repo_path
        #self.relative_content_paths = content_path
        self.relative_pid_file = pid_file
        if content_paths:
            self.content_paths = list(map(lambda p: self.repo_path + "/" + p, content_paths))
        config_file_name =  join(self.repo_path, config_file_name)
        pid_file = join(self.repo_path, pid_file)
        self.pid_file = pid_file
        self.config_file_name = config_file_name

    def file_existence(self, file):
        file_exists = False
        if (exists(file) and os.path.isfile(file)):
            print(f"{file} already exists and will not be overwritten")
            file_exists = True
        return file_exists
    
    def create_pid_file(self):
        pid_file = self.pid_file
        new_file = False
        if not(self.file_existence(pid_file)):
            try:
                d = {}
                with open(pid_file, 'w') as outfile:
                    json.dump(d, outfile)
            except Exception as e:
                raise ValueError(f"ERROR: {e}")
            else:
                new_file = True
                print(f"Pid tracking file: {pid_file} created")
        else:
            warnings.warn(f"{pid_file} already exists and will not be overwritten")
        return new_file

    def create_config_yaml(self, args):
        if not(self.file_existence(self.config_file_name)):
            # removing conf file from args when creating yml file
            yaml_dict = args.copy()
            yaml_dict.pop('conf_file', None)
            yaml_dict.pop('repo', None)
            try:
                with open(self.config_file_name, 'w') as c:
                    yaml.safe_dump(yaml_dict, c)
            except Exception as e:
                print(e)
            else:
                print(f"Config file created: {self.config_file_name}")
        else:
            warnings.warn(f"{self.config_file_name} already exists and will not be overwritten")

    def chk_content_paths(self):
        script_name = relpath(__file__)
        method_name = self.chk_content_paths.__name__
        msg = list(map(u.check_path, self.content_path))
        # removing all ok messages, i.e. None
        messages = list(filter(lambda x: x, msg))
        if messages:
            raise ValueError(f"From {script_name}.{method_name}: Cannot continue processing. See errors:{messages}")

    def create_config(self, id_type, domain, doi_prefix):
        self.c['DEFAULT'] = {'pid_file': self.relative_pid_file, "domain": domain, 'id_type': id_type}
        if doi_prefix:
            self.c['DEFAULT'].update({"doi_prefix": doi_prefix})
        try:
            with open(self.config_file_name, "w") as cf:
                self.c.write(cf)
        except Exception as e:
            raise(f"ERROR: Could not create config file: {e}")
        else:
            print(f"Config file: {self.config_file_name} created")

    def get_file_list(self):
        try:
            file_list = u.get_file_list(self.content_path)
        except ValueError as e:
            print(e)
            sys.exit(1)
        return file_list



