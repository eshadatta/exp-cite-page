import json
import os 
from os.path import exists
from pathlib import Path
class ProcessJson:
    def __init__(self, repo, pid_file, tracked_file):
        self.repo = repo
        self.pid_file = self.repo + pid_file
        self.tracked_file = tracked_file

    def create_pid_file(self):
        if not(exists(self.pid_file)):
            try:
                Path(self.pid_file).touch()
            except Exception as e:
                raise ValueError(f"ERROR: {e}")
        else:
            print(f"{self.pid_file} already exists")

    def add_pid(self, pid, commit_id, git_hash, utc_datetime):
        id = {"git_commit_id": commit_id, "current_id": pid, "file": self.tracked_file, "file_hash": git_hash, "utc_commit_date": utc_datetime}
        if (exists(self.pid_file)):
            if not(os.path.isfile(self.pid_file)):
                raise ValueError(f"{self.pid_file} must be a json file")
            else:
                # handle file processing
                contents = None
                try:
                    with open(self.pid_file, "r") as outfile:
                        contents = json.load(outfile)
                except Exception as e:
                    raise IOError(f"Error reading file: {e}")
                try:
                    with open(self.pid_file, "w") as outfile:
                        contents.append(id)
                        json.dump(contents, outfile)
                except Exception as e:
                    raise IOError(f"Error writing to file: {e}")
        elif not(exists(self.pid_file)):
            try:
                with open(self.pid_file, "w") as outfile:
                    json.dump([id], outfile)
            except Exception as e:
                raise IOError(f"Error writing to file: {e}")