import git
from git import Repo
from datetime import datetime
import os 

class GitInfo:
    def __init__(self, path):
        self.path = path
        try:
            self.repo = Repo(self.path)
        except:
            raise ValueError(f"{self.path} must be a git repository")
        else:
            self.git = self.repo.git
            self.active_branch = self.repo.active_branch
    def tracked(self, file):
        tracked = None if not(git.ls_files(file)) else True
        return tracked
    def get_file_commit_id(self, file, branch):
        file_commit_id = None
        git = self.git
        file = self.path + file
        is_tracked = self.tracked(file)
        if is_tracked:
            # most recent commit id for the branch in question
            branch_commit_id = git.rev_list(branch, n=1)
            # file's most recent commit id
            file_commit_id = git.rev_list("-n 1", branch_commit_id, file)
            # getting hash of file contents
            git_hash = git.hash_object(file)
        else:
            raise ValueError(f"{file} must be tracked in git repository: {self.path}")
        return [file_commit_id, git_hash]

    def commit_date(self, commit):
        iso_format = self.git.show("-s","--format=%cI",commit)
        dt = datetime.fromisoformat(iso_format)
        timestamp = int(round(dt.timestamp()))
        utc_datetime = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return utc_datetime



        

 