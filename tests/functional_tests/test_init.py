import helpers.static_page_id as sp
import init
import pytest
import re
from os.path import exists
from itertools import chain
def fixtures():
    return {"dir_path": "tests/fixtures/tiny_static_site", 'default_pid_json_filename': 'pid.json','default_config_filename': 'static.ini'}

def correct_args():
    required_args = ["-r", fixtures()['dir_path'], "-d", "https://test.org"]
    id = [{'-id': 'doi', '--doi-prefix': 'x.x.x'}, {'-id': 'uuid'}]
    return required_args, id

def get_default_filenames():
    fix = list(fixtures().keys())
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
    get_full_args = parse_correct_args()
    for a in get_full_args:
        init.main(a)
        _, err = capsys.readouterr()
        assert err == ''
    #for f in default_file_names:
        #assert exists(f)

# check if default files exist
def test_file_existence():
    for f in get_default_filenames():
        assert exists(f)

# check expected contents of files

