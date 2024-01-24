from run_all import init, gen_pid
import id
import pytest
import re
import shutil
import configparser
from os.path import exists
from itertools import chain
import json
import helpers.git_info as g
import tests.functional_tests.fixtures as f
import id
import helpers.utilities as u
from click.testing import CliRunner
from git import Repo
import os
import re

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
    args = [{}, {'batch': True}, {'st': "custom"}, {'st': "custom", 'batch': True}]
    info = []
    ts = f.TestScenarios()
    for a in args:
        process = {}
        if 'batch' in a.keys():
            if 'st' in a.keys() and a['st'] == "custom":
                process['info'] = ts.scenario_batch(st="custom")
            else:
                process['info'] = ts.scenario_batch(st="crossref")
        elif 'st' in a.keys() and a['st'] == "custom":
            process['info'] = ts.scenario_multiple_non_existing_files(st="custom")
        else:
            process['info'] = ts.scenario_multiple_non_existing_files(st="crossref")
        process['test_args'] = f.valid_gen_pid_args(**a)
        info.append(process)
    return info

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
def scenario_name(scenario):
    return scenario['info']['name']

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
        default_config_files.append(other_files)
    f.remove_files(default_config_files)

@pytest.mark.parametrize('scenario', get_valid_gen_pid_args(), ids=scenario_name)
def test_valid_args(monkeypatch, scenario):
    s = scenario['info']
    processing_type = 'batch' if ('batch' in s['name']) else None
    dir_path = f.fixture_dir_path()["dir_path"]
    pid_file = dir_path+"/"+f.fixture_default_filenames()['default_pid_json_filename']
    if not('mixed' in s['name'] or 'batch' in s['name']):
        content_files = s['args']['-c']
    elif 'batch' in s['name']:
        content_files = list(s['expected_content_values'].keys())
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
    setup_files(dir_path, content_files, processing_type)
    runner = CliRunner()
    result = runner.invoke(gen_pid, scenario['test_args'])
    assert result.exit_code == 0
    submission_file = None
    if 'crossref' in scenario['test_args']:
        submission_file_match = re.search("tests.*?xml", result.output, re.MULTILINE)
        submission_file = submission_file_match.group() 
        assert os.path.exists(submission_file)
    pid_output = check_output(pid_file)
    expected_output = check_output(s['expected_output'])
    sorted_pid_output = sorted(pid_output, key = lambda d: d['file'])
    sorted_expected_output = sorted(expected_output, key = lambda d: d['file'])
    assert sorted_pid_output == sorted_expected_output
    teardown_files(dir_path, content_files, submission_file)

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