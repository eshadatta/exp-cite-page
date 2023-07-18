import helpers.static_page_id as sp
import init
import pytest
import re
import os
import configparser
from os.path import exists
from itertools import chain
import json

# convert dictionary into a flattened list
def flatten_dict(d):
    data = [[k, v] for k, v in d.items()]
    data = list(chain(*data))
    return data

def fixtures():
    return {"dir_path": "tests/fixtures/tiny_static_site", 'default_pid_json_filename': 'pid.json','default_config_filename': 'static.ini'}

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

def parse_correct_args():
    required_args, id_args = correct_args()
    full_args = []
    for a in id_args:
        id_type = a['-id']
        doi_prefix = a.get('--doi-prefix', None)
        args = [[k, v] for k, v in a.items()]
        arg_list = list(chain(*args))
        full_args.append(required_args + arg_list)
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
    required_args, id_args, _ = correct_args()
    # flattening this to a list
    rargs = flatten_dict(required_args)
    dfnames = get_default_filenames()
    for a in id_args:
        for f in dfnames:
            if exists(f):
                os.remove(f) 
        id_type = a['-id']
        doi_prefix = a.get('--doi-prefix', None)
        args_list = flatten_dict(a)
        full_args = rargs + args_list
        init.main(full_args)
        _, err = capsys.readouterr()
        assert err == ''
        for f in dfnames:
            assert exists(f)
        json_file = list(filter(re.compile(".*json").match, dfnames))[0]
        ini_file = list(filter(re.compile(".*ini").match, dfnames))[0]
        with open(json_file, 'r') as fp:
            d = json.load(fp)
        assert len(d) == 0
        ini_contents = read_config_parser(ini_file)
        check_defaults = {"pid_file": fixtures()['default_pid_json_filename'], "domain": required_args['-d'], "id_type": id_type}
        if doi_prefix:
            check_defaults["doi_prefix"] = doi_prefix
        for c in ini_contents:
            key = c[0]
            assert check_defaults[key] == c[1]

def test_init_configured_filenames(capsys):
    #with pytest.raises(SystemExit) as e:
    pid_file_name = 'record.json'
    config_file_name = 'config.ini'
    required_args, id_args, files = correct_args(pid_file_name = pid_file_name, config_file_name = config_file_name)
    # flattening this to a list
    rargs = flatten_dict(required_args)
    file_args = flatten_dict(files)
    for a in id_args:
        for f in list(files.values()):
            if exists(f):
                os.remove(f) 
        id_type = a['-id']
        doi_prefix = a.get('--doi-prefix', None)
        arg_list = flatten_dict(a)
        full_args = rargs + file_args + arg_list
        init.main(full_args)
        _, err = capsys.readouterr()
        assert err == ''
        for f in list(files.values()):
            full_path = f"{required_args['-r']}/{f}"
            assert exists(full_path)
        json_file = f"{required_args['-r']}/{files['-p']}"
        ini_file = f"{required_args['-r']}/{files['-cf']}"
        with open(json_file, 'r') as fp:
            d = json.load(fp)
        assert len(d) == 0
        ini_contents = read_config_parser(ini_file)
        check_defaults_config_file = {"pid_file": pid_file_name, "domain": required_args['-d'], "id_type": id_type}
        if doi_prefix:
            check_defaults_config_file["doi_prefix"] = doi_prefix
        for c in ini_contents:
            key = c[0]
            assert check_defaults_config_file[key] == c[1]

        


