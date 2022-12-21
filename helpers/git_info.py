import git
from git import Repo

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

    def get_file_commit_id(self, file, branch):
        file_commit_id = None
        git = self.git
        tracked = None if not(git.ls_files(file)) else True
        if tracked:
            # most recent commit id for the branch in question
            branch_commit_id = git.rev_list(branch, n=1)
            # file's most recent commit id
            file_commit_id = git.rev_list("-n 1", branch_commit_id, file)
        return file_commit_id
        

 