import configparser
import os
import configparser
from os.path import exists
from itertools import chain

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

def fixture_content_path():
    return "content/blog/"

def fixture_files():
    files = ['2022/2022-09-16-2022-board-election.md']
    return files

def fixture_git_response():
    return {'content/blog/2022/2022-09-22-crossref-role-integrity-scholarly-record.md': {'file_commit_id': '8a45235c90adc33c60167661050b877a9f7fa4af', 'file_hash': 'e854b9426e59005a40c493ca40628fa1d15239a8', 'utc_commit_date': '2023-07-24 14:43:05', 'current_id': 'JvdtZ5EPCH', 'version': '0.0.0', 'url': None, 'file': 'content/blog/2022/2022-09-22-crossref-role-integrity-scholarly-record.md'}}

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


