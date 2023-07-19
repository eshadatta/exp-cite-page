import init
import pytest
import re
import os
import configparser
from os.path import exists
from itertools import chain
import json

def fixture_dir_path():
    return {"dir_path": "tests/fixtures/tiny_static_site"}

def fixture_domain():
    return {'domain': 'https://test.org'}

def fixture_default_filenames():
    return {'default_pid_json_filename': 'pid.json','default_config_filename': 'static.ini'}

def fixture_dir_path():
    return {"dir_path": "tests/fixtures/tiny_static_site"}

def fixture_id():
    return [{"id": "uuid"}, {"id": "doi", "doi_prefix": "x.x.x"}]

def files():
    # returning an empty array to create valid args with and without specifying user files
    user_specified_files = {"-p": "record.json", "-cf": "config.ini"}
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
    config = configparser.ConfigParser()
    try:
        config.read(file)
    except Exception as e:
        raise NameError(e)
    return list(config['DEFAULT'].items())

def remove_files(files):
    for f in files:
        if exists(f):
            try:
                os.remove(f)
            except Exception as e:
                print(e)
def invalid_args():
    INVALID_ARGS = ['', ['t'], ['-a'], ['-x', 't'], ['-r', 'x']]
    invalid_args = {
        "empty_arg": {"arg": '', 'error': 'test'}
    }
    return invalid_args

def valid_args():
    valid_args_combo = []
    ids = fixture_id()
    script_files = files()
    for id in ids:
        args = {"-r": fixture_dir_path()["dir_path"], "-d": fixture_domain()["domain"], "-id": id['id']}
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

def get_data(info):
    repo_path = info['-r']
    necessary_files = {}
    necessary_files['pid_file'] = {"name": info.get("-p", fixture_default_filenames()['default_pid_json_filename'])}
    necessary_files['config_file'] = {"name": info.get("-cf", fixture_default_filenames()['default_config_filename'])}
    for v in necessary_files.values():
        v['full_path'] = f"{repo_path}/{v['name']}"
    return necessary_files

ITERATIONS = 2
ARGS = [['-r', 'tests/fixtures/tiny_static_site', '-d', 'x', '-id', 'uuid'],['-r', 'tests/fixtures/tiny_static_site', '-d', 'x', '-id', 'doi', '--doi-prefix', 'e']]
#files = ['tests/fixtures/tiny_static_site/pid.json', 'tests/fixtures/tiny_static_site/static.ini']

def remove(files):
    for f in files:
        if os.path.exists(f):
            os.remove(f)

@pytest.fixture(scope='class', autouse=True)
def setup_teardown(request):
    process_args = flatten_dict(request.param)
    print(f'{request.param}-SETUP')
    yield init.main(process_args)
    files = get_data(request.param)
    file_collection = [x['full_path'] for x in files.values()]
    print(f'{request.param}-TEARDOWN')
    remove(file_collection)

@pytest.mark.parametrize('setup_teardown', valid_args(), indirect=True)
class TestSomething:
    def test_something(self):
        print("test_something: ")

    def test_something_else(self):
        print("test_something_else: ")

