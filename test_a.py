import git
from git import Repo
from unittest.mock import patch
from helpers import git_info

def x():
    e = git_info.GitInfo(".")
    [s,x] = e.git_commit_id("t", "f")
    return [s,x]


class MockGitInfo:
    def __init__(self, path):
        self.git = True
        self.active_branch = "test"
    def tracked(self, file):
        return True
    def check_file_status(self, file):
        return True
    def git_commit_id(branch, file):
        pass

class MockGit:
    def __init__(self, path):
        self.git = True
        self.active_branch = "test"
    

""" @patch('helpers.git_info.GitInfo', MockGitInfo)
def test():
    b = x()
    print(b) """

@patch("helpers.git_info.GitInfo", autospec=True)
def test_stash_pull(mock_repo):
    def a(b,s):
        return [1,2]
    m = mock_repo.return_value
    m.git = True
    m.active_branch = "test"
    m.tracked = True
    m.git_commit_id.side_effect = a
    [e,s] = x()
    print([e,s])


