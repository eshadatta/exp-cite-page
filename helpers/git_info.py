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
        tracked = None if not(self.git.ls_files(file)) else True
        return tracked

    def branch_commit_id(self, branch, n=1):
        # most recent commit id for the branch in question
        return self.git.rev_list(branch, n=1)

    def file_commit_id(self, branch_commit_id, file, n="1"):
        # most recent commit id for the file in question
        n = f"-n {n}"
        return self.git.rev_list(n, branch_commit_id, file)

    # check if this is the latest commit
    def check_file_status(self, file):
        committed = False
        status = self.git.diff(file)
        if len(status) == 0:
            committed = True
        return committed

    def git_add_file(self, file):
        try:
            self.git.add(file)
        except Exception as e:
            raise(f"ERROR: {e}")
         

    def git_commit_file(self, file, comment = None):
        if not(comment):
            comment = "Initializing file for permanent ID versioning"
        try:
            self.git.commit("-m", comment, file)
        except Exception as e:
            raise(f"ERROR: {e}")

    def git_commit_id(self, branch, file):
        # most recent commit id for the branch in question
        branch_commit_id = self.branch_commit_id(branch)
        # file's most recent commit id
        file_commit_id = self.file_commit_id(branch_commit_id, file)
        # getting hash of file contents
        git_hash = self.git.hash_object(file)
        return [file_commit_id, git_hash]

    def get_file_commit_info(self, file, branch):
        file_commit_id = None
        git_hash = None
        file = self.path + file
        is_tracked = self.tracked(file)
        if is_tracked:
            [file_commit_id, git_hash]  = self.git_commit_id(branch, file)
        else:
            raise ValueError(f"{file} must be tracked in git repository: {self.path}")
        return [file_commit_id, git_hash]


    def commit_date(self, commit):
        iso_format = self.git.show("-s","--format=%cI",commit)
        dt = datetime.fromisoformat(iso_format)
        timestamp = int(round(dt.timestamp()))
        utc_datetime = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return utc_datetime



        

 