import json
import os 
from os.path import exists

class ProcessJson:
    def __init__(self, repo, pid_file, tracked_file):
        self.repo = repo
        self.pid_file = self.repo + pid_file
        self.tracked_file = tracked_file

    def add_pid(self, pid, commit_id, utc_datetime):
        id = {"git_commit_id": commit_id, "current_id": pid, "file": self.tracked_file, "utc_commit_date": utc_datetime}
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