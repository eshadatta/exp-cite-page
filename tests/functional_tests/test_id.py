import init
import id
import pytest
import re
import os
import configparser
from os.path import exists
from itertools import chain
import json
import tests.functional_tests.fixtures as f
import git
from git import Repo
import sys
import random
import os.path
import helpers.git_info as gi
from unittest.mock import patch
import id
def gen_args():
    id_args = f.fixture_id()[1]
    content_path = f.fixture_content_path()+'2022/2022-09-16-2022-board-election.md'
    args = {'-r': f.fixture_dir_path()['dir_path'], '-c': content_path}
    return args
"""
def roll_dice():
    return random.randint(1,3)

def test_roll(monkeypatch):
    def mockrandom(a,b):
        return 3
    
    monkeypatch.setattr(random, "randint", mockrandom)

    x = roll_dice()
    assert x == 3

"""

def twotest_id(monkeypatch):
    args = f.flatten_dict(gen_args())
    files = f.fixture_files()[0]
    def mock_git_return(a,b, c=None):
        return a + b
    monkeypatch.setattr(id, "git_info", mock_git_return("1", "2", None))
    #monkeypatch.setattr(id, "git_info", lambda: "s")
    x = id.main(args)
    #assert x == "s"
    print("HERE: ", x)

# need to run a more comprehensive unittest on git_info to make sure it's returning what is expected. Probably need to mock the git info and uuid class for that

# this runs a functional test to make sure that id.py runs as expected
# I don't really like magical programming but both mock and monkeypatch have it, monkeypatch is a little more explicit in its patching

#I was having trouble with monkeypatching here
@patch("id.git_info")
def test_id(mock_git):
    args = f.flatten_dict(gen_args())
    mock_git.return_value = f.fixture_git_response()
    id.main(args)
    # open json file
    #check against expected value
    # assert that it's all good
'''
def division():
    nb = random.randrange(0, 2)
    return 100 / nb    # this is on purpose ;-)
 
def function_to_be_tested():
    result = division()
    return f"This is the result :{result}"
 
def test_function_to_be_tested_returns_str(monkeypatch):
    def mockreturn():
        return 50.0
    monkeypatch.setattr(sys.modules[__name__],division, mockreturn)    
    assert isinstance(function_to_be_tested(), str)
def test(monkeypatch):
    print(sys.modules[__name__])
'''