import helpers.static_page_id as sp
import init
import pytest
import re
from os.path import exists
def fixtures():
    return {"dir_path": "tests/fixtures/tiny_static_site", 'default_pid_json_filename': 'pid.json','default_config_filename': 'static.ini'}

def correct_args():
    repo_dir_path = fixtures()
    id = [["-id", "doi", "--doi-prefix", "x.x.x"], ["-id", "uuid"]]
    
def test_default_filename():
        s = sp.static_page_id()
        fix = fixtures()
        default_attributes = re.compile("default_")
        for k, v in fix.items():
             if default_attributes.match(k):
                  assert getattr(s,k) == v 

# suite of correct args
def test_init_default_filename(capsys):
    fixture_pid = f"{fixtures()['dir_path']}/{fixtures()['default_pid_json_filename']}"
    fixture_config = f"{fixtures()['dir_path']}/{fixtures()['default_config_filename']}"
    #with pytest.raises(SystemExit) as e:
    init.main(["-r", "tests/fixtures/tiny_static_site", "-id", "uuid", "-d", "x"])
    _, err = capsys.readouterr()
    assert err == ''
    assert exists(fixture_pid)
    assert exists(fixture_config)

