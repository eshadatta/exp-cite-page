import json
import tests.functional_tests.fixtures as f
import helpers.utilities as u
from git import Repo
import add_doi
import pytest
import os
import helpers.git_info as g

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

def content_file(files):
        s = f.TestScenarios()
        for i in files:
            md = u.read_markdown_file(i)
            md.metadata[s.version_tag] = s.initial_version
            s.write_content_file(i, md)

def mock_add_dois():
    dir_path = "tests/fixtures/tiny_static_site"
    mock_pid_file = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/fixture_multiple_dois.json"
    mock_pid_content = check_output(mock_pid_file)
    values = {}
    for i in mock_pid_content:
        f = dir_path + '/' + i['file']
        values[f] = i['doi']['value']
    mock_content_files = list(values.keys())
    content_file(mock_content_files)
    add_doi_args = ['-r', dir_path, '-f', mock_pid_file]
    add_doi.main(add_doi_args)
    return values

def test_valid_args():
    check_values = mock_add_dois()
    for file, fixture_value in check_values.items():
        md = u.read_markdown_file(file)
        assert 'DOI' in md.metadata.keys()
        assert md.metadata['DOI'] == fixture_value

"""Restoring fixtures to their original state"""
@pytest.fixture(scope="session", autouse=True)
def restore(request):
    def git_restore():
        cwd = os.getcwd()
        repo = is_repo(cwd)
        if repo:
            fixtures_path = f.fixture_dir_path()['dir_path'] + "/" + f.fixture_content_path()
            print(fixtures_path)
            g.GitInfo(cwd).restore(fixtures_path)
    request.addfinalizer(git_restore)