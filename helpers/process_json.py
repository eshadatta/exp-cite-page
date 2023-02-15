import json
import os 
from os.path import exists
from pathlib import Path
class ProcessJson:
    def __init__(self, repo, pid_file):
        self.repo = repo
        self.pid_file = pid_file
        self.pid_entry = {"file_commit_id": None, "current_id": None, "file": None, "file_hash": None, "utc_commit_date": None}

    def write_pid(self, contents):
        try:
            with open(self.pid_file, "w") as outfile:
                json.dump(contents, outfile)
        except Exception as e:
                raise IOError(f"Error writing to file: {e}")

    def check_pre_existing_commits(self, json_file_contents, pid_file_contents):
        pid_file_commit_id = pid_file_contents['file_commit_id']
        pre_existing_files = [x['file'] for x in json_file_contents if x['file_commit_id'] == pid_file_commit_id]
        return pre_existing_files

    def add_pid(self, pid_file_contents):
        for k, v in self.pid_entry.items():
            pid_file_contents[k] = pid_file_contents.get(k, v)

        id = {"file_commit_id": pid_file_contents["file_commit_id"], "current_id": pid_file_contents["current_id"], "file": pid_file_contents["file"], "file_hash": pid_file_contents["file_hash"], "utc_commit_date": pid_file_contents["utc_commit_date"]}
        if (exists(self.pid_file)):
            if not(os.path.isfile(self.pid_file)):
                raise ValueError(f"{self.pid_file} must be a json file")
            else:
                # handle file processing
                contents = None
                file_size = os.path.getsize(self.pid_file)
                if file_size > 0:
                    try:
                        with open(self.pid_file, "r") as outfile:
                            contents = json.load(outfile)
                    except Exception as e:
                        raise IOError(f"Error reading file: {e}")
                    check_pre_existing_file = self.check_pre_existing_commits(contents, id)
                    if not(check_pre_existing_file):
                        contents.append(id)
                    else:
                        print(f"INFO: Not adding {check_pre_existing_file}. This file at this commit already exists in {self.pid_file}")
                elif file_size == 0:
                    contents = [id]
        else:
            raise ValueError(f"PID File: {self.pid_file} must exist")
        return contents

    def initialize_pid_file(self, pid_file_contents):
        for f in pid_file_contents:
            content = self.add_pid(f)
            self.write_pid(content)

      