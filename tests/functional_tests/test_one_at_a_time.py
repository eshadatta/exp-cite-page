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

""" def test_default_filename():
    s = sp.static_page_id()
    fix = fixture_default_filenames()
    for k, v in fix.items():
        assert getattr(s,k) == v  """

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
    

""" @pytest.fixture
def check_files():
    def _chk_files(args):
        files = data(args)
        all_files = [x['full_path'] for x in files.values()]
        for f in all_files:
            assert exists(f)
    yield _chk_files """

def check_files(files):
    all_files = [x['full_path'] for x in files.values()]
    for f in all_files:
        assert exists(f)

def check_pid_file_contents(files):
    pid_file = files['pid_file']['full_path']
    with open(pid_file, 'r') as fp:
        d = json.load(fp)
        assert len(d) == 0

def check_config_contents(doi_prefix, id_type, domain, files):
    ini_contents = read_config_parser(files['config_file']['full_path'])
    check_defaults = {"pid_file": files['pid_file']['name'], "domain": domain, "id_type": id_type}
    if doi_prefix:
        check_defaults["doi_prefix"] = doi_prefix
    for c in ini_contents:
        key = c[0]
        assert check_defaults[key] == c[1]

@pytest.mark.parametrize('v_args', valid_args())
class TestInit: 
    @pytest.fixture(scope='function', autouse=True)
    def setup_and_teardown(self, v_args):
        print("setup")
        process_args = flatten_dict(v_args)
        init.main(process_args)
        yield
        remove_files(v_args)

    #def test_all(self, capsys, check_files, v_args):
        #check_files(v_args)

    def test_all(self, v_args):
        id_type = v_args['-id']
        domain = v_args['-d']
        doi_prefix = v_args.get('--doi-prefix', None)
        files = data(v_args)
        check_files(files)
        check_pid_file_contents(files)
        check_config_contents(doi_prefix, id_type, domain, files)
        
""" 
    def test_check_files(self, valid_args):
        print("HERE2: ", valid_args)
        _, files = self.data(valid_args)
        for f in files.values():
            assert exists(f['full_path'])
        self.remove_files(valid_args)
        
    def test_check_pid_file_contents(self, valid_args):
        print("HERE3: ", valid_args)
        _, files = self.data(valid_args)
        pid_file = files['pid_file']['full_path']
        with open(pid_file, 'r') as fp:
            d = json.load(fp)
            assert len(d) == 0
        self.remove_files(valid_args)
    
     """
