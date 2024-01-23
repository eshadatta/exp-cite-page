import helpers.static_page_id as sp
from run_all import init
from click.testing import CliRunner
import pytest
import re
import os
import configparser
from os.path import exists
from itertools import chain
import json
import yaml 

def fixture_dir_path():
    return {"dir_path": "tests/fixtures/tiny_static_site"}

def fixture_domain():
    return {'domain': 'https://test.org'}

def fixture_default_filenames():
    return {'default_pid_json_filename': 'pid.json','default_config_filename': 'config.yml'}

def fixture_dir_path():
    return {"dir_path": "tests/fixtures/tiny_static_site"}

def fixture_id():
    return [{"id": "doi", "doi_prefix": "x.x.x"}]

def files():
    # returning an empty array to create valid args with and without specifying user files
    user_specified_files = {"-p": "record.json", "-cf": "test.yml", "-c": "content"}
    return [{}, user_specified_files]

def fixtures():
    path = fixture_dir_path().copy()
    filenames = fixture_default_filenames().copy()
    path.update(filenames)
    return path

# convert dictionary into a flattened list
def flatten_dict(d):
    data = [[k, v] for k, v in d.items()]
    data = list(chain(*data))
    return data

def read_config_parser(file):
    data = None
    try:
        with open(file, 'r') as y:
            data = yaml.safe_load(y)
    except Exception as e:
            raise ValueError(f"ERROR: {e}")
    return data

def remove_files(files):
    for f in files:
        if exists(f):
            try:
                os.remove(f)
            except Exception as e:
                print(e)

def valid_args():
    valid_args_combo = []
    ids = fixture_id()
    script_files = files()
    for id in ids:
        args = {"-r": fixture_dir_path()["dir_path"], "-d": fixture_domain()["domain"]}
        if 'doi_prefix' in id:
            args['--doi-prefix'] = id['doi_prefix']
        for f in script_files:
            if len(f) != 0:
                # could be optimized
                # python dictionary behavior is difficult here
                s = args.copy()
                s.update(f)
                valid_args_combo.append(s)
        valid_args_combo.append(args)
    return valid_args_combo

def test_default_filename():
    s = sp.static_page_id()
    fix = fixture_default_filenames()
    for k, v in fix.items():
        assert getattr(s,k) == v

def remove_files(valid_args):
    files = data(valid_args)
    for f in files.values():
        if exists(f['full_path']):
            os.remove(f['full_path'])

def data(valid_args):
    repo_path = valid_args['-r']
    necessary_files = {}
    necessary_files['pid_file'] = {"name": valid_args.get("-p", fixture_default_filenames()['default_pid_json_filename'])}
    necessary_files['config_file'] = {"name": valid_args.get("-cf", fixture_default_filenames()['default_config_filename'])}
    for v in necessary_files.values():
        v['full_path'] = f"{repo_path}/{v['name']}"
    return necessary_files
    
class InitTest:
    def __init__(self, args):
        default_id = 'doi'
        default_content = ['.']
        self.args = args
        self.files = data(self.args)
        self.domain = args['-d']
        self.content_path = args.get('-id', default_content)
        self.id_type = args.get('-id', default_id)
        self.doi_prefix = args.get('--doi-prefix', None)

    def check_files(self):
        all_files = [x['full_path'] for x in self.files.values()]
        return all_files

    def check_pid_file_contents(self):
        pid_file = self.files['pid_file']['full_path']
        file_length = 1
        try:
            with open(pid_file, 'r') as fp:
                d = json.load(fp)
                file_length = len(d)
        except Exception as e:
            print(e)
        return file_length

    def check_config_contents(self):
        ini_contents = read_config_parser(self.files['config_file']['full_path'])
        check_defaults = {"pid_file": self.files['pid_file']['name'], "domain": self.domain, "id_type": self.id_type}
        if self.doi_prefix:
            check_defaults["doi_prefix"] = self.doi_prefix
        return [check_defaults, ini_contents]

@pytest.mark.parametrize('v_args', valid_args())
class TestInit: 
    @pytest.fixture(scope='function', autouse=True)
    def setup_and_teardown(self, v_args):
        print("setup")
        process_args = flatten_dict(v_args)
        print(process_args)
        runner = CliRunner()
        runner.invoke(init, process_args)
        yield
        remove_files(v_args)

    def test_all(self, v_args):
        json_file_should_be_empty = 0
        test_init = InitTest(v_args)
        files = test_init.check_files()
        for f in files:
            assert exists(f)
        json_file_should_be_empty == test_init.check_pid_file_contents()
        defaults, ini_contents = test_init.check_config_contents()
        for k, v in defaults.items():
            assert v == ini_contents[k]

def invalid_args():
    invalid_args = {
        "empty_args": [''],
        "unnamed_arg": ['t'],
        "incorrect_flag": ['-a'],
        "incorrect_flag_with_value": ['-x', 't'],
        "correct_flag_with_non_existent_dir": ['-r', 'x'],
        "incomplete_args": ['-r', '.'],
        "required_arg_without_value1": ['-r', '.', '-d'],
        "incomplete_args2": ['-r', '.', '-d', 'a'],
        "required_arg_without_value2": ['-r', '.', '-d', 'a', '--id-type'],
        "required_arg_without_req_subcommand": ['-r', '.', '-d', 'a', '--id-type', 'doi']
    }
    return invalid_args


def test_invalid_args():
    args = invalid_args()
    for k, v in args.items():
        print("Testing: ", k)
        print("args: ", v)
        runner = CliRunner()
        result = runner.invoke(init, v)
        assert result.exit_code != 0

