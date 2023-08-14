import init
import id
import pytest
import re
import shutil
import configparser
from os.path import exists
from itertools import chain
import json
import tests.functional_tests.fixtures as f
import git
from git import Repo
import sys
import random
import os.path
import helpers.git_info as gi
import helpers.generate_id as gid
from unittest.mock import patch
import id
import helpers.utilities as u


def gen_args():
    content_path = f.fixture_content_path()+'2022/2022-09-16-2022-board-election.md'
    args = {'-r': f.fixture_dir_path()['dir_path'], '-c': 'content/blog'}
    return args

def valid_args():
    {}

def check_output(output):
    contents = None
    try:
        with open(output, 'r') as f:
            contents = json.load(f)
    except Exception as e:
        print(e)
    return contents

def fixture_gi():
    return {"path": "test", "active_branch": "t", "check_git_info": ["fc","gh",""], "commit_date": "2023-07-25 17:02:32"}

def get_mock_git_info(d = None):
    x = [1,2,[]]
    if d:
        x = [d['file_commit_id'], d['file_hash'], []]
    return x

# mocking methods used in both these classes
# generate combos of valid args and do the test like the commented out test id function
def get_all_scenarios(scenario_type):
    test_scenarios = f.TestScenarios()
    regex = re.compile(rf'^{scenario_type}')
    scenario_methods = list(filter(regex.match, dir(test_scenarios)))
    scenarios = []
    for i in scenario_methods:
        m = getattr(test_scenarios, i)
        scenarios.append(m())
    return scenarios

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


def setup_files(dir_path, content_files):
    content_file(dir_path, content_files, "initialize")
    process_args = f.valid_init_args()
    init.main(process_args)

def teardown_files(dir_path, content_files):
    content_file(dir_path, content_files, "restore")
    default_files = list(f.fixture_default_filenames().values())
    default_config_files = list(map(lambda x: dir_path+"/"+x, default_files))
    f.remove_files(default_config_files)

def prepare_existing_pid_file(src, dst):
    try:
        shutil.copyfile(src, dst)
    except Exception as e:
        print(e)

@pytest.mark.parametrize('scenario1', get_all_scenarios(scenario_type='mixed_'))
def test_me(monkeypatch, scenario1):
    print("scenario: ", scenario1)
    dir_path = f.fixture_dir_path()["dir_path"]
    content_files = list(scenario1['files'].values())
    existing_file = scenario1['files']['existing']
    pid_file = dir_path+"/"+f.fixture_default_filenames()['default_pid_json_filename']
    setup_files(dir_path, content_files)
    preset_file = scenario1['preset_file']
    prepare_existing_pid_file(preset_file, pid_file)
    content_file(dir_path, existing_file, "increment")
    args = f.flatten_dict(scenario1['args'])
    def mock_git_info(a, b, c):
        file_info = scenario1['expected_values']
        return file_info
    monkeypatch.setattr('id.git_info', mock_git_info)
    id.main(args)
    pid_output = check_output(pid_file)
    expected_output = check_output(scenario1['expected_output'])
    assert pid_output == expected_output
    teardown_files(dir_path, content_files)

# you are getting file info from the script. Look that up to get the uuid and the file hash
@pytest.mark.parametrize('scenario', get_all_scenarios(scenario_type='scenario_'))
@patch('helpers.git_info.GitInfo', autospec=True)
@patch('helpers.generate_id.GenID', autospec=True)
class TestID:
    @pytest.fixture(scope='function', autouse=True)
    def setup_andteardown(self, scenario):
        dir_path = f.fixture_dir_path()["dir_path"]
        content_files = scenario['args']['-c']
        pid_file = dir_path+"/"+f.fixture_default_filenames()['default_pid_json_filename']
        setup_files(dir_path, content_files)
        if (re.search("scenario_existing", scenario['name'])):
            preset_file = scenario['preset_file']
            prepare_existing_pid_file(preset_file, pid_file)
            content_file(dir_path, content_files, "increment")
        yield
        teardown_files(dir_path, content_files)

    # mocking git info methods
    def test_id(self, mock_id, mock_git, scenario):
        print(f"For {scenario['name']}: {scenario}")
        [file_commit_id, file_hash, err] = get_mock_git_info(scenario['expected_content_values'])
        args = f.flatten_dict(scenario['args'])
        m = mock_git.return_value
        m.path = "test"
        m.active_branch = "branch"
        m.check_git_info.return_value = [file_commit_id, file_hash, err]
        m.commit_date.return_value = scenario['expected_content_values']['utc_commit_date']
        m_id = mock_id.return_value
        m_id.gen_default.return_value = scenario['expected_content_values']['current_id']
        pid_file = f.fixture_dir_path()["dir_path"]+"/"+f.fixture_default_filenames()['default_pid_json_filename']
        id.main(args)
        pid_output = check_output(pid_file)
        expected_output = check_output(scenario['expected_output'])
        assert pid_output == expected_output

    
