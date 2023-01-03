import json
import os 
from os.path import exists

class ProcessJson:
    def __init__(self, repo, file):
        self.repo = repo
        self.path = os.path.normpath(self.repo)
        self.file = self.path + "/" + file


    def add_pid(self, pid, commit_id, utc_datetime):
        id = {"git_commit_id": commit_id, "current_id": pid, "file": self.file, "utc_commit_date": utc_datetime}
        if (exists(self.file)):
            if not(os.path.isfile(self.file)):
                raise ValueError(f"{self.file} must be a json file")
            else:
                # handle file processing
                contents = None
                try:
                    with open(self.file, "r") as outfile:
                        contents = json.load(outfile)
                except Exception as e:
                    raise IOError(f"Error reading file: {e}")
                try:
                    with open(self.file, "w") as outfile:
                        contents.append(id)
                        json.dump(contents, outfile)
                except Exception as e:
                    raise IOError(f"Error writing to file: {e}")
        elif not(exists(self.file)):
            try:
                with open(self.file, "w") as outfile:
                    json.dump([id], outfile)
            except Exception as e:
                raise IOError(f"Error writing to file: {e}")