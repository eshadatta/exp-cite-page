import json
import os 
from os.path import exists
from pathlib import Path
class ProcessJson:
    def __init__(self, repo, pid_file, doi_prefix, domain):
        self.repo = repo
        self.pid_file = pid_file
        self.file_url_domain = domain
        self.doi_prefix = doi_prefix
        self.pid_entry = {"file_commit_id": None, "current_id": None, "file": None, "file_hash": None, "utc_commit_date": None, "version": None, "doi_prefix": doi_prefix, "production_domain": domain,"url": None}

    def write_pid(self, contents):
        try:
            with open(self.pid_file, "w") as outfile:
                json.dump(contents, outfile)
        except Exception as e:
                raise IOError(f"Error writing to file: {e}")

    def check_pre_existing_filehash(self, json_file_contents, pid_file_contents):
        pid_file_hash = pid_file_contents['file_hash']
        pre_existing_files = [x['file'] for x in json_file_contents if x['file_hash'] == pid_file_hash]
        return pre_existing_files

    def add_pid(self, pid_file_contents):
        for k, v in self.pid_entry.items():
            pid_file_contents[k] = pid_file_contents.get(k, v)

        id = {"file_commit_id": pid_file_contents["file_commit_id"], "current_id": pid_file_contents["current_id"], "file": pid_file_contents["file"], "file_hash": pid_file_contents["file_hash"], "utc_commit_date": pid_file_contents["utc_commit_date"], "version": pid_file_contents["version"], "doi_prefix": self.doi_prefix, "production_domain": self.file_url_domain,"url": pid_file_contents["url"]}
        # handle file processing
        contents = []
        file_size = os.path.getsize(self.pid_file)
        if file_size > 0:
            try:
                with open(self.pid_file, "r") as outfile:
                    contents = json.load(outfile)
                    contents.append(id)
            except Exception as e:
                    raise IOError(f"Error reading file: {e}")
        elif file_size == 0:
            contents = [id]
        return contents

    def initialize_pid_file(self, pid_file_contents):
        if (exists(self.pid_file)):
            if not(os.path.isfile(self.pid_file)):
                raise ValueError(f"{self.pid_file} must be a json file")
        else:
            raise ValueError(f"PID File: {self.pid_file} must exist")
        for f in pid_file_contents:
            content = self.add_pid(f)
            self.write_pid(content)

    def write_file_info(self, updated_pid_file_contents, rest_pid_contents):
        keys = list(self.pid_entry.keys())
        for f, info in updated_pid_file_contents.items():
            for k in keys:
                # adding the rest of the information that's the same for all files
                if not(k in info):
                    info[k] = self.pid_entry[k]
            rest_pid_contents.append(info)
        self.write_pid(rest_pid_contents)



      