from run_all import init, gen_pid
import pytest
import re
from os.path import exists
import json
import helpers.git_info as g
import tests.functional_tests.fixtures as f
import helpers.utilities as u
from click.testing import CliRunner
from git import Repo
import os
import re
from xmldiff import main
from lxml import etree
from submit_files import submit_files

def check_output(output):
    contents = None
    try:
        with open(output, 'r') as f:
            contents = json.load(f)
    except Exception as e:
        print(e)
    return contents

def is_repo(path):
    repo = None
    try:
        repo = Repo(path)
    except:
        pass
    return repo

def get_valid_gen_pid_args():
    process = {}
    ts = f.TestScenarios()
    process['info'] = ts.scenario_multiple_non_existing_files(st="crossref")
    process['args'] = f.valid_gen_pid_args()
    return process

def content_file(dir_path, file, action="initialize"):
        s = f.TestScenarios()
        # converting files to a list if incoming file is a string
        c = [file] if not(isinstance(file, list)) else file
        # adding directory path to the relative path
        c = list(map(lambda x: f"{dir_path}/{x}", c))
        for i in c:
            md = u.read_markdown_file(i)
            # removing x-version
            if action == "restore":
                md.metadata.pop(s.version_tag, None)
            # adding x-version
            elif action == "initialize":
                md.metadata[s.version_tag] = s.initial_version
            elif action == "increment":
                prev_version = md.metadata[s.version_tag]
                mv = int(prev_version.split(".")[0]) + 1
                updated_version = f"{str(mv)}.0.0"
                md.metadata[s.version_tag] = updated_version
            s.write_content_file(i, md)

def setup_files(dir_path, content_files,processing_type=None):
    if not(processing_type):
        content_file(dir_path, content_files,"initialize")
    process_args = f.valid_init_args(content = f.fixture_content_path())
    runner = CliRunner()
    runner.invoke(init, process_args)
    
def teardown_files(dir_path, content_files, other_files = None):
    content_file(dir_path, content_files, "restore")
    default_files = list(f.fixture_default_filenames().values())
    default_config_files = list(map(lambda x: dir_path+"/"+x, default_files))
    if other_files:
        default_config_files = default_config_files + other_files
    f.remove_files(default_config_files)

def run_script(monkeypatch):
    test_info = get_valid_gen_pid_args()
    s = test_info['info']
    dir_path = f.fixture_dir_path()["dir_path"]
    content_files = s['args']['-c']
    class MockGit(object):
        def __init__(self, a):
            self.a = a
            self.active_branch = True
        def check_file_status(self, a):
            return True
        def tracked(self, a):
            return True
        def batch_check_git_info(self, a):
            return [1, 2]
        def check_git_info(self, a, b):
            return [1, 2,3]
        def commit_date(self, a):
            return "2023-12-20 19:30:13"
        def git_commit_id(self, a, b):
            return self.batch_check_git_info(a)
        
    class MockID(object):
        def __init__(self):
            pass
        def gen_default(self, len=None):
            return "hvvgkns9ta"
    
    def mock_git(a):
        return MockGit(a)
    
    def mock_gen_id():
        return MockID()

        
    monkeypatch.setattr('helpers.git_info.GitInfo', mock_git)
    monkeypatch.setattr('helpers.generate_id.GenID', mock_gen_id)
    setup_files(dir_path, content_files)
    runner = CliRunner()
    result = runner.invoke(gen_pid, test_info['args'])
    submission_file = None
    submission_file_match = re.search("tests.*?\\d{14}_submission.xml", result.output, re.MULTILINE)
    submission_file = submission_file_match.group()
    return [dir_path, content_files, [submission_file]]
    
def mock_submit_file_args(requests_mock, pid_file, submission_file):
    username = "username"
    password = "password"
    deposit_endpoint = "mock://dummy-endpoint"
    submit_files_arg = ['-f', submission_file, '-pid', pid_file, '-u', username, '-p', password, '-e', deposit_endpoint]
    requests_mock.post(deposit_endpoint, text = "success", status_code = 200)
    submit_files.main(submit_files_arg)

def test_valid_args(monkeypatch, requests_mock):
    dir_path, content_files, [submission_file] = run_script(monkeypatch)
    expected_output_file = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/fixture_doi_deposit.json"
    pid_file = dir_path + '/' + f.fixture_default_filenames()['default_pid_json_filename']
    expected_output = check_output(expected_output_file)
    mock_submit_file_args(requests_mock, pid_file, [submission_file][0])
    pid_output = check_output(pid_file)
    sorted_pid_output = sorted(pid_output, key = lambda d: d['file'])
    sorted_expected_output = sorted(expected_output, key = lambda d: d['file'])
    assert sorted_pid_output == sorted_expected_output
    teardown_files(dir_path, content_files, [submission_file]) 

"""Restoring fixtures to their original state"""
@pytest.fixture(scope="session", autouse=True)
def restore(request):
    def git_restore():
        cwd = os.getcwd()
        repo = is_repo(cwd)
        if repo:
            fixtures_path = f.fixture_dir_path()['dir_path'] + "/" + f.fixture_content_path()
            g.GitInfo(cwd).restore(fixtures_path)
    request.addfinalizer(git_restore)