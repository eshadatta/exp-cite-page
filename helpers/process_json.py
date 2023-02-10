import json
import os 
from os.path import exists
from pathlib import Path
class ProcessJson:
    def __init__(self, repo, pid_file):
        self.repo = repo
        self.pid_file = self.repo + pid_file
        self.pid_entry = {"file_commit_id": None, "current_id": None, "file": None, "file_hash": None, "utc_commit_date": None}
    def create_pid_file(self):
        if not(exists(self.pid_file)):
            try:
                Path(self.pid_file).touch()
            except Exception as e:
                raise ValueError(f"ERROR: {e}")
        else:
            print(f"{self.pid_file} already exists")
            
    def write_pid(self, contents):
        try:
            with open(self.pid_file, "w") as outfile:
                contents.append(id)
                json.dump(contents, outfile)
        except Exception as e:
                raise IOError(f"Error writing to file: {e}")

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
                    contents.append(id)
                elif file_size == 0:
                    contents = [id]
        else:
            raise ValueError(f"PID File: {self.pid_file} must exist")
        self.write_pid(contents)
      