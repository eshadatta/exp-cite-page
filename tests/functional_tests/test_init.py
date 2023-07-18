import helpers.static_page_id as sp
import init
import pytest
import re
import os
import configparser
from os.path import exists
from itertools import chain
import json


#VALID_ARGS = [{"-r": "tests/fixtures/tiny_static_site", "-d": "https://test.org", "-id": "uuid"},{"-r": "tests/fixtures/tiny_static_site", "-d": "https://test.org", "-id": "doi", "--doi-prefix": "x.x.x"},{"-r": "tests/fixtures/tiny_static_site", "-d": "https://test.org", "-id": "uuid", "-cf": "config.ini", "-p": "record.json"},{"-r": "tests/fixtures/tiny_static_site", "-d": "https://test.org", "-id": "doi", "--doi-prefix": "x.x.x","-cf": "config.ini", "-p": "record.json"}]


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

@pytest.mark.parametrize('valid_args', valid_args())
def test_correct_args(valid_args, capsys):
    repo_path = valid_args['-r']
    necessary_files = {}
    necessary_files['pid_file'] = {"name": valid_args.get("-p", fixture_default_filenames()['default_pid_json_filename'])}
    necessary_files['config_file'] = {"name": valid_args.get("-cf", fixture_default_filenames()['default_config_filename'])}
    for v in necessary_files.values():
        v['full_path'] = f"{repo_path}/{v['name']}"
    id_type = valid_args['-id']
    doi_prefix = valid_args.get('--doi-prefix', None)
    process_args = flatten_dict(valid_args)
    init.main(process_args)
    _, err = capsys.readouterr()
    assert err == ''


    
