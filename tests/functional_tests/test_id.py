import init
import id
import pytest
import re
import os
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

def get_mock_git_info(d):
    return [d['file_commit_id'], d['file_hash'], []]

# mocking methods used in both these classes
# generate combos of valid args and do the test like the commented out test id function
def get_all_scenarios():
    pass

@patch('helpers.git_info.GitInfo', autospec=True)
@patch('helpers.generate_id.GenID', autospec=True)
def test_id(mock_id, mock_git):
    test_scenarios = f.TestScenarios()
    scenario_info = test_scenarios.scenario_single_non_existing_file()
    #scenario_info = test_scenarios.scenario_multiple_non_existing_file()
    [file_commit_id, file_hash, err] = get_mock_git_info(scenario_info['expected_content_values'])

    args = f.flatten_dict(scenario_info['args'])
    m = mock_git.return_value
    m.path = "test"
    m.active_branch = "branch"
    m.check_git_info.return_value = [file_commit_id, file_hash, err]
    m.commit_date.return_value = scenario_info['expected_content_values']['utc_commit_date']
    m_id = mock_id.return_value
    m_id.gen_default.return_value = scenario_info['expected_content_values']['current_id']
    id.main(args)
    pid_output = check_output("tests/fixtures/tiny_static_site/pid.json")
    expected_output = check_output(scenario_info['expected_output'])
    assert pid_output == expected_output

    
# need to run a more comprehensive unittest on git_info to make sure it's returning what is expected. Probably need to mock the git info and uuid class for that

# this runs a functional test to make sure that id.py runs as expected
# I don't really like magical programming but both mock and monkeypatch have it, monkeypatch is a little more explicit in its patching

#I was having trouble with monkeypatching here
""" @patch("id.git_info")
def test_id(mock_git):
    args = f.flatten_dict(gen_args())
    mock_git.return_value = f.fixture_git_response()
    id.main(args)
    pid_output = check_output("tests/fixtures/tiny_static_site/pid.json")
    expected_output = check_output("tests/fixtures/tiny_static_site/expected_values_json/one_value.json")
    assert pid_output == expected_output """
    # open json file
    #check against expected value
    # assert that it's all good
