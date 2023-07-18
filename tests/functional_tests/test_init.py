import helpers.static_page_id as sp
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

def fixture_default_filenames():
    return {'default_pid_json_filename': 'pid.json','default_config_filename': 'static.ini'}

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

def correct_args(pid_file_name = None, config_file_name = None):
    required_args = {"-r": fixtures()['dir_path'], "-d": "https://test.org"}
    id = [{'-id': 'doi', '--doi-prefix': 'x.x.x'}, {'-id': 'uuid'}]
    files = {}
    if pid_file_name:
        files['-p'] = pid_file_name
    if config_file_name:
        files['-cf'] = config_file_name
    return required_args, id, files

def get_default_filenames():
    fix = list(fixtures().keys())
    # get values for all default file names
    default_file_names = list(map(lambda x: fixtures()["dir_path"] + "/" + fixtures()[x], filter(lambda x: not(x == "dir_path"), fix)))
    return default_file_names

def parse_correct_args(pid_file_name = None, config_file_name = None):
    required_args, id_args, files = correct_args(pid_file_name, config_file_name)
    required_args.update(files)
    full_args = id_args.copy()
    [a.update(required_args) for a in full_args]
    return full_args

def read_config_parser(file):
    config = configparser.ConfigParser()
    try:
        config.read(file)
    except Exception as e:
        raise NameError(e)
    return list(config['DEFAULT'].items())
def test_default_filename():
    s = sp.static_page_id()
    fix = fixtures()
    default_attributes = re.compile("default_")
    for k, v in fix.items():
        if default_attributes.match(k):
            assert getattr(s,k) == v 

# suite of correct args
# should not error out
def test_init_default_filenames(capsys):
    #with pytest.raises(SystemExit) as e:
    full_args = parse_correct_args()
    repo_path = full_args[0]['-r']
    dfnames = list(map(lambda x: f"{repo_path}/{x}", list(fixture_default_filenames().values())))
    for a in full_args:
        # take this out to its own method
        for f in dfnames:
            if exists(f):
                os.remove(f) 
        id_type = a['-id']
        doi_prefix = a.get('--doi-prefix', None)
        args_list = flatten_dict(a)
        init.main(args_list)
        _, err = capsys.readouterr()
        assert err == ''
        for f in dfnames:
            assert exists(f)
        json_file = repo_path + "/" + fixture_default_filenames()['default_pid_json_filename']
        ini_file = repo_path + "/" + fixture_default_filenames()['default_config_filename']
        with open(json_file, 'r') as fp:
            d = json.load(fp)
        assert len(d) == 0
        ini_contents = read_config_parser(ini_file)
        check_defaults = {"pid_file": fixtures()['default_pid_json_filename'], "domain": a['-d'], "id_type": id_type}
        if doi_prefix:
            check_defaults["doi_prefix"] = doi_prefix
        for c in ini_contents:
            key = c[0]
            assert check_defaults[key] == c[1]

def test_init_configured_filenames(capsys):
    #with pytest.raises(SystemExit) as e:
    pid_file_name = 'record.json'
    config_file_name = 'config.ini'
    full_args = parse_correct_args(pid_file_name = pid_file_name, config_file_name = config_file_name)
    files = [pid_file_name, config_file_name]
    repo_path = full_args[0]['-r']
    file_names = list(map(lambda x: f"{repo_path}/{x}", files))
    for a in full_args:
        for f in file_names:
            if exists(f):
                os.remove(f) 
        id_type = a['-id']
        doi_prefix = a.get('--doi-prefix', None)
        arg_list = flatten_dict(a)
        init.main(arg_list)
        _, err = capsys.readouterr()
        assert err == ''
        for f in file_names:
            assert exists(f)
        json_file = file_names[0]
        ini_file = file_names[1]
        with open(json_file, 'r') as fp:
            d = json.load(fp)
        assert len(d) == 0
        ini_contents = read_config_parser(ini_file)
        check_defaults_config_file = {"pid_file": pid_file_name, "domain": a['-d'], "id_type": id_type}
        if doi_prefix:
            check_defaults_config_file["doi_prefix"] = doi_prefix
        for c in ini_contents:
            key = c[0]
            assert check_defaults_config_file[key] == c[1]

        


