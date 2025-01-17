import configparser
import os
import configparser
from os.path import exists
from itertools import chain
import pytest
import init
import frontmatter
import helpers.static_page_id as sp
import helpers.utilities as u
import json
import shutil

def fixture_dir_path():
    return {"dir_path": "tests/fixtures/tiny_static_site"}

def fixture_domain():
    return {'domain': 'https://test.org'}

def fixture_default_filenames():
    return {'default_pid_json_filename': 'pid.json','default_config_filename': 'config.yml'}

def fixture_dir_path():
    return {"dir_path": "tests/fixtures/tiny_static_site"}

def fixture_id():
    return [{"id": "doi", "doi_prefix": "10.5555"}]

def fixture_content_path():
    return "content/blog/"

def init_files():
    # returning an empty array to create valid args with and without specifying user files
    user_specified_files = {"-p": "record.json", "-cf": "config.yml"}
    return [{}, user_specified_files]

def flatten_dict(d, expected_length = 3, key = '-c'):
    data = [[k, v] for k, v in d.items()]
    data = list(chain(*data))
    args = list(filter(lambda x: x, data))
    if key in d.keys() and isinstance(d[key], list):
        for i in range(0, len(d[key])):
            file = d[key][i]
            index = i + expected_length
            limit = len(data) -1
            if index > limit:
                args.append(file)
            else:
                args[index] = file
    return args

def remove_files(files):
    for f in files:
        if exists(f):
            try:
                os.remove(f)
            except Exception as e:
                print(e)


def read_config_parser(file):
    config = configparser.ConfigParser()
    try:
        config.read(file)
    except Exception as e:
        raise NameError(e)
    return list(config['DEFAULT'].items())

def files():
    return ["tests/fixtures/tiny_static_site/content/blog/2022/2022-09-16-2022-board-election.md", "tests/fixtures/tiny_static_site/content/blog/2023/2023-04-01-renewed-persistence.md"]

def valid_init_args(content=None):
    ids = fixture_id()[0]
    args = {"-r": fixture_dir_path()['dir_path'], "-d": fixture_domain()["domain"], "--doi-prefix": ids['doi_prefix']}
    if content:
        args.update({"-c": content})
    process_args = flatten_dict(args)
    return process_args

def valid_gen_pid_args(dry_run=True, st="crossref", batch=False):
    st_types = ["custom", "crossref"]
    if st in st_types:
        submission_info = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/fixture_submission_info.yml"
        args = {"-r": fixture_dir_path()['dir_path'], "-st": st}
        if st == "crossref":
            args.update({"--info": submission_info})
        process_args = flatten_dict(args)
        if batch:
            process_args.append("--batch")
        if dry_run:
            process_args.append("-dry")
    else:
        raise ValueError(f"Invalid value. It needs to be one of these: {st_types}")
    return process_args

class TestScenarios():
    def __init__(self):
        ids = fixture_id()[0]
        args = {"-r": fixture_dir_path()['dir_path'], "-d": fixture_domain()["domain"], "-id": ids['id'], "--doi-prefix": ids['doi_prefix']}
        default_files = list(fixture_default_filenames().values())
        self.dir_path = fixture_dir_path()["dir_path"]
        self.static_page = sp.static_page_id()
        self.version_tag = self.static_page.init_version_tag
        self.initial_version = self.static_page.init_version
        self.default_config_files = list(map(lambda x: self.dir_path+"/"+x, default_files))
        self.init_process_args = flatten_dict(args)
        self.content_path = fixture_content_path()
        self.relevant_keys = ['file_commit_id', 'file_hash', 'utc_commit_date', 'current_id', 'file', 'version']

    def write_content_file(self, file_path, markdown):
        try:
            with open(file_path, 'w') as m:
                m.write(frontmatter.dumps(markdown, handler=markdown.handler))
        except Exception as e:
            raise(f"ERROR: {e}")
        
    def content_file(self, file, action="initialize"):
        md = u.read_markdown_file(file)
        if action == "restore":
            md.metadata.pop(self.version_tag, None)
        elif action == "initialize":
            md.metadata[self.version_tag] = self.initial_version
        self.write_content_file(file, md)

    def get_mock_json_values(self, output):
        expected_values = {}
        for i in output:
            expected_values[i['file']] = {}
            for k in self.relevant_keys:
                expected_values[i['file']][k] = i[k]
        return expected_values
        
    def get_mock_values(self, file):
        contents = None
        try:
            with open(file, 'r') as f:
                contents = json.load(f)
        except Exception as e:
            print(e)
        return contents

    def generate_fixture_info(self, name, content_path, expected_output, additional_data = None):
        info = {}
        expected_json = self.get_mock_values(expected_output)
        expected_json_values = self.get_mock_json_values(expected_json)
        info = {"name": name, "args": {"-r": self.dir_path, "-c": content_path}, "expected_output": expected_output,"expected_content_values": expected_json_values}
        if additional_data:
            info.update(additional_data)
        return info
    
    def scenario_single_non_existing_file(self, st=None):
        st_types = [None, "crossref", "custom"]
        info = None
        if st in st_types:
            if st == "crossref":
                expected_output = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/one_value.json"
            else:
                expected_output = "tests/fixtures/tiny_static_site/expected_values_json/non_existing_files/one_value.json"
        name = "scenario_single_non_existing_file"
        if st:
                name = st + "_" + name
        content_path = 'content/blog/2022/2022-09-16-2022-board-election.md' 
        info = self.generate_fixture_info(name, content_path, expected_output)
        return info
    
    def scenario_multiple_non_existing_files(self, st=None):
        st_types = [None, "crossref", "custom"]
        info = None
        if st in st_types:
            if st == "custom":
                expected_output = "tests/fixtures/tiny_static_site/custom_submission/multiple_values.json"
            elif st == "crossref":
                expected_output = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/multiple_values.json"
            else:
                expected_output = "tests/fixtures/tiny_static_site/expected_values_json/non_existing_files/multiple_values.json"
            name = "scenario_multiple_non_existing_files"
            if st:
                name = st + "_" + name
            content_path = [i.split(self.dir_path+"/")[1] for i in files()]
            info = self.generate_fixture_info(name, content_path, expected_output)
        return info
    
    def scenario_batch(self, st=None):
        st_types = [None, "crossref", "custom"]
        info = None
        if st in st_types:
            if st == "custom":
                expected_output = "tests/fixtures/tiny_static_site/custom_submission/batch.json"
            elif st == "crossref":
                expected_output = "tests/fixtures/tiny_static_site/crossref_submission_fixtures/batch.json"
            else:
                expected_output = "tests/fixtures/tiny_static_site/expected_values_json/non_existing_files/batch.json"
        name = "scenario_batch"
        if st:
            name = st + "_" + name
        content_path = self.content_path
        info = self.generate_fixture_info(name, content_path, expected_output)
        info['args'].update({"-b": None})
        return info
    
    # need to reimplement
    """ def scenario_existing_single_file(self):
        name = "scenario_existing_single_file"
        expected_output = "tests/fixtures/tiny_static_site/expected_values_json/existing_files/one_value.json"
        preset_file = "tests/fixtures/tiny_static_site/expected_values_json/non_existing_files/one_value.json"
        file = files()[0]
        content_path = file.split(self.dir_path+"/")[1]
        preset_file_info = {"preset_file": preset_file}
        info = self.generate_fixture_info(name, content_path, expected_output, preset_file_info)
        return info
    
    def scenario_mixed(self):
        name = "scenario_mixed"
        expected_output = "tests/fixtures/tiny_static_site/expected_values_json/mixed/two_values.json"
        preset_file = "tests/fixtures/tiny_static_site/expected_values_json/non_existing_files/another_test_one_value.json"
        content_path = self.content_path
        additional_data = {"preset_file": preset_file, "files": {"non_existing": "content/blog/2022/2022-09-16-2022-board-election.md", "existing": "content/blog/2023/2023-05-02-2023-public-data-file-now-available-with-new-and-improved-retrieval-options.md"}}
        info = self.generate_fixture_info(name, content_path, expected_output, additional_data)
        return info  """







