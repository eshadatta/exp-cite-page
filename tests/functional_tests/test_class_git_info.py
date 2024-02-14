import pytest
from unittest.mock import patch, MagicMock
from helpers.git_info import GitInfo
import re

def get_default_values():
    return {"test_file_commit": {'param_value': 'b4e2f2162510fc04962b7c78c157a8d771ff5750', 'git_value': '2023-10-12T18:21:14+00:00', 'expected_output': '2023-10-12 18:21:14'}}

def mock_gitinfo(method_name=None):
    class MockGit(object):
        def ls_files(self, x):
            state = True if method_name != MockGit.ls_files.__name__ else False
            return state
        def rev_list(self, a, n, c=None):
            return True
        def status(self,a, b):
            state = '' if method_name != MockGit.status.__name__ else 'string'
            return state
        def diff(self,a):
            state = '' if method_name != MockGit.diff.__name__ else 'string'
            return state
        def add(self,a):
            state = True if method_name != MockGit.add.__name__ else False
            return state
        def commit(self,a, b, c):
            state = True if method_name != MockGit.commit.__name__ else False
            print("here: ", state)
            return state
        def restore(self,a):
            return True
        def hash_object(self,a):
            return True
        def show(self,a, b, c):
            return get_default_values()['test_file_commit']['git_value']
        
    def __init__(self, x):
        self.path = x
        self.git = MockGit()
        self.repo = True
        self.active_branch = True
    with patch.object(GitInfo, '__init__', __init__):
        s = GitInfo('a')
        return s
    
@pytest.fixture
def valid_mock_gitinfo():
    mg = mock_gitinfo()
    return mg

# Testing true cases
def test_tracked(valid_mock_gitinfo):
    mock_gitinfo = valid_mock_gitinfo
    assert mock_gitinfo.tracked('x') is True

def test_commit_date(valid_mock_gitinfo):
    default_values = get_default_values()
    mock_gitinfo = valid_mock_gitinfo
    test_file_commit = default_values['test_file_commit']
    assert mock_gitinfo.commit_date(test_file_commit) == test_file_commit['expected_output']

def test_check_file_status(valid_mock_gitinfo):
    mock_gitinfo = valid_mock_gitinfo
    assert mock_gitinfo.check_file_status('x') is True

def test_valid_methods_without_exception(valid_mock_gitinfo):
    mock_gitinfo = valid_mock_gitinfo
    methods = ['git_add_file', 'git_commit_file']
    for m in methods:
        a = getattr(mock_gitinfo, m)
        assert a('x') is None

def test_method_list_types(valid_mock_gitinfo):
    mock_gitinfo = valid_mock_gitinfo
    methods = ['git_commit_id','get_file_commit_info']
    for m in methods:
        print(m)
        a = getattr(mock_gitinfo, m)
        result = a('a', 'b')
        assert isinstance(result, list)

def test_check_git_info(valid_mock_gitinfo):
    mock_gitinfo = valid_mock_gitinfo
    result = mock_gitinfo.check_git_info('a','b')
    assert isinstance(result, list)
    assert len(result) == 3
    assert isinstance(result[2], list)
    assert len(result[2]) == 0

def test_not_tracked():
    mg = mock_gitinfo(method_name='ls_files')
    assert mg.tracked('x') is None

def test_not_committed():
    mg_status_check = mock_gitinfo(method_name='status')
    mg_file_diff_check = mock_gitinfo(method_name='diff')
    assert mg_status_check.check_file_status('x') is False
    assert mg_file_diff_check.check_file_status('x') is False

def test_err_check_git_info():
    mg_not_tracked = mock_gitinfo(method_name='ls_files')
    result1 = mg_not_tracked.check_git_info('a','b')
    assert len(result1[2]) == 1
    mg_not_committed = mock_gitinfo(method_name='status')
    result2 = mg_not_committed.check_git_info('a','b')
    assert len(result2[2]) == 1



    







