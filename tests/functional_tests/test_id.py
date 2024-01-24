from run_all import init
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


def setup_files(dir_path, content_files, processing_type=None):
    if not(processing_type):
        content_file(dir_path, content_files, "initialize")
    process_args = f.valid_init_args()
    runner = CliRunner()
    runner.invoke(init, process_args)
    
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
        
def scenario_name(scenario):
    return scenario['name']

def check_scenario_settings(scenario):
    existing_file = None
    processing_type = 'batch' if ('batch' in scenario['name']) else None
    dir_path = f.fixture_dir_path()["dir_path"]
    # this needs to be optimized
    if not('mixed' in scenario['name'] or 'batch' in scenario['name']):
        content_files = scenario['args']['-c']
    elif 'batch' in scenario['name']:
        content_files = list(scenario['expected_content_values'].keys())
    else:
        content_files = list(scenario['files'].values())
    pid_file = dir_path+"/"+f.fixture_default_filenames()['default_pid_json_filename']
    setup_files(dir_path, content_files, processing_type)
    if '_mixed' in scenario['name']:
        existing_file = scenario['files']['existing']
    if 'scenario_existing' in scenario['name'] or '_mixed' in scenario['name']:
        increment_file = existing_file if existing_file else content_files
        preset_file = scenario['preset_file']
        prepare_existing_pid_file(preset_file, pid_file)
        content_file(dir_path, increment_file, "increment")
    return [dir_path, pid_file, content_files]
# for batch scenario we are not initializing the files. The id script will do that
@pytest.mark.parametrize('scenario', get_all_scenarios(scenario_type='scenario_'), ids=scenario_name)
def test_id_valid_args(monkeypatch, scenario):
    dir_path, pid_file, content_files = check_scenario_settings(scenario)
    args = f.flatten_dict(scenario['args'])
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
            return 12345
    
    def mock_git(a):
        return MockGit(a)
    
    def mock_gen_id():
        return MockID()

        
    monkeypatch.setattr('helpers.git_info.GitInfo', mock_git)
    monkeypatch.setattr('helpers.generate_id.GenID', mock_gen_id)
    id.main(args)
    pid_output = check_output(pid_file)
    expected_output = check_output(scenario['expected_output'])
    sorted_pid_output = sorted(pid_output, key = lambda d: d['file'])
    sorted_expected_output = sorted(expected_output, key = lambda d: d['file'])
    assert sorted_pid_output == sorted_expected_output
    teardown_files(dir_path, content_files)

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

