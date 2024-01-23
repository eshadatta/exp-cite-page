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
import check_doi_urls

def is_repo(path):
    repo = None
    try:
        repo = Repo(path)
    except:
        pass
    return repo

def check_output(output):
    contents = None
    try:
        with open(output, 'r') as f:
            contents = json.load(f)
    except Exception as e:
        print(e)
    return contents

def teardown_files(dir_path):
    default_files = list(f.fixture_default_filenames().values())
    default_config_files = list(map(lambda x: dir_path+"/"+x, default_files))
    f.remove_files(default_config_files)

def mock_check_doi_urls(requests_mock, repo_path, pid_file):
    check_doi_args = ['-r', repo_path, '-p', pid_file]
    test_doi_prefix = f.fixture_id()[0]['doi_prefix']
    # the breakup of the strings is to accurately represent
    # the regular expression with the variable interpolation. 
    # Otherwise, the regular expression ends up with incorrectly compiling the {10} signifier 

    match_str = f'http.*?doi.org/{test_doi_prefix}'
    # mock doi url check
    matcher = re.compile(match_str + r'\/[a-z0-9]{10}$')
    # get location from pid_file
    pid_output = check_output(pid_file)
    location = pid_output[0]['url']
    requests_mock.get(matcher, headers={'location':location}, status_code = 302)
    url_status = check_doi_urls.main(check_doi_args)
    return url_status

def test_valid_args(monkeypatch, requests_mock):
    dir_path = "tests/fixtures/tiny_static_site"
    mock_pid_file = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/fixture_one_file_pid.json"
    expected_output_file = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/one_value.json"
    expected_output = check_output(expected_output_file)
    url_status = mock_check_doi_urls(requests_mock, dir_path, mock_pid_file)
    mock_pid_output = check_output(mock_pid_file)
    assert url_status == {}
    assert mock_pid_output == expected_output
    teardown_files(dir_path) 

"""Restoring fixtures to their original state"""
@pytest.fixture(scope="session", autouse=True)
def restore(request):
    def git_restore():
        cwd = os.getcwd()
        repo = is_repo(cwd)
        if repo:
            g.GitInfo(cwd).restore("tests/fixtures/tiny_static_site/crossref_submission_fixtures/fixture_one_file_pid.json")
    request.addfinalizer(git_restore)