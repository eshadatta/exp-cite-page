from run_all import init
from helper_url_generation import url_constructor
import tests.functional_tests.fixtures as f
import json
import helpers.utilities as u
from click.testing import CliRunner
import id
import os
import pytest
import helpers.git_info as g
from git import Repo
content_path = ["content/blog", "content/report/_index.md","content/report/rules.md"]
files = ["content/blog/2022/2022-09-16-2022-board-election.md", "content/blog/2023/2023-03-23-cite-data-now.md", "content/report/_index.md", "content/report/rules.md"]
ids = f.fixture_id()[0]
args = {"-r": f.fixture_dir_path()['dir_path'], "-d": f.fixture_domain()["domain"], "--doi-prefix": ids['doi_prefix']}
url_constructor_args = ['-r', '/Users/eshadatta/test-website-workflow', '-cf', '/Users/eshadatta/test-website-workflow/config.yml']
url_gen_output = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/url_gen.json"

def is_repo(path):
    repo = None
    try:
        repo = Repo(path)
    except Exception:
        pass
    return repo

def valid_init_args(content=None):
    process_args = f.flatten_dict(args)
    if isinstance(content, list):
        for i in range(0, len(content) * 2):
            if (i % 2) == 0:
                content.insert(i, "-c")
        process_args = process_args + content

    return process_args

def check_output(output):
    contents = None
    try:
        with open(output, 'r') as f:
            contents = json.load(f)
    except Exception as e:
        print(e)
    return contents

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

def setup_files():
    process_args = valid_init_args(content = content_path)
    runner = CliRunner()
    runner.invoke(init, process_args)
    content_file(args['-r'], files)

def teardown_files(dir_path, content_files):
    content_file(dir_path, content_files, "restore")
    default_files = list(f.fixture_default_filenames().values())
    default_config_files = list(map(lambda x: dir_path+"/"+x, default_files))
    f.remove_files(default_config_files)

def test(monkeypatch):
    setup_files()
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
    id_args = ["-r", args['-r'], '-c'] + files
    id.main(id_args)
    url_gen_args = ["-r", args['-r'], "-cf", args['-r']+'/'+f.fixture_default_filenames()['default_config_filename']]
    pid_file = args['-r']+'/'+f.fixture_default_filenames()['default_pid_json_filename']
    url_constructor.main(url_gen_args)
    pid_output = check_output(pid_file)
    expected_output = check_output(url_gen_output)
    sorted_pid_output = sorted(pid_output, key = lambda d: d['file'])
    sorted_expected_output = sorted(expected_output, key = lambda d: d['file'])
    assert sorted_pid_output == sorted_expected_output
    teardown_files(args['-r'], files)

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