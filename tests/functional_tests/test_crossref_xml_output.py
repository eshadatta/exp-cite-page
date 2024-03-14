from run_all import init, gen_pid
import pytest
import re
import json
import helpers.git_info as g
import tests.functional_tests.fixtures as f
import helpers.utilities as u
from click.testing import CliRunner
from git import Repo
import os
from xmldiff import main
from lxml import etree

def delete_nodes(nodes):
    for n in nodes:
        n.getparent().remove(n)

def collect_nodes(tree):
    # elements expected to have different values
    # timestamp and posted date
    expected_nodes_xpath = ['./x:head/x:timestamp', './x:body//x:posted_date']
    ns = {'x': 'http://www.crossref.org/schema/5.3.0'}
    gather_nodes = []
    for n in expected_nodes_xpath:
        el = tree.xpath(n, namespaces = ns)
        gather_nodes = gather_nodes + el
    return gather_nodes

def compare_xml_outputs(submission, fixture):
    submission_temp_xml = 'temp_submission.xml'
    fixture_temp_xml = 'temp_fixture.xml'
    submission_tree = etree.parse(submission)
    fixture_tree = etree.parse(fixture)
    fixture_collect_nodes = collect_nodes(fixture_tree)
    submission_collect_nodes = collect_nodes(submission_tree)
    # alter submission tree
    delete_nodes(submission_collect_nodes)
    submission_tree.write(submission_temp_xml, pretty_print=True, xml_declaration=True,   encoding="utf-8")
    #alter fixture tree
    delete_nodes(fixture_collect_nodes)
    fixture_tree.write(fixture_temp_xml, pretty_print=True, xml_declaration=True,   encoding="utf-8")
    return [submission_temp_xml, fixture_temp_xml]

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
    except Exception:
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

def test_valid_args(monkeypatch):
    test_info = get_valid_gen_pid_args()
    s = test_info['info']
    dir_path = f.fixture_dir_path()["dir_path"]
    pid_file = dir_path+"/"+f.fixture_default_filenames()['default_pid_json_filename']
    content_files = s['args']['-c']
    expected_output = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/fixture_two_files_output.xml"
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
    assert result.exit_code == 0
    submission_file = None
    submission_file_match = re.search("tests.*?\\d{14}_submission.xml", result.output, re.MULTILINE)
    assert submission_file_match
    submission_file = submission_file_match.group() 
    assert os.path.exists(submission_file)
    tmp_submission, tmp_fixture = compare_xml_outputs(submission_file, expected_output)
    d = main.diff_files(tmp_submission, tmp_fixture)
    assert len(d) == 0
    remove_extraneous_files = [tmp_submission, tmp_fixture, submission_file]
    teardown_files(dir_path, content_files, remove_extraneous_files)

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