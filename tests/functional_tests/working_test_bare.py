import pytest
import init
import os

ITERATIONS = 2
ARGS = [['-r', 'tests/fixtures/tiny_static_site', '-d', 'x', '-id', 'uuid'],['-r', 'tests/fixtures/tiny_static_site', '-d', 'x', '-id', 'doi', '--doi-prefix', 'e']]
files = ['tests/fixtures/tiny_static_site/pid.json', 'tests/fixtures/tiny_static_site/static.ini']

def remove(files=files):
    for f in files:
        if os.path.exists(f):
            os.remove(f)

@pytest.fixture(scope='class', autouse=True)
def setup_teardown(request):
    print(f'{request.param}-SETUP')
    yield init.main(request.param)
    print(f'{request.param}-TEARDOWN')
    remove()

@pytest.mark.parametrize('setup_teardown', ARGS, indirect=True)
class TestSomething:
    def test_something(self):
        print("test_something: ")

    def test_something_else(self):
        print("test_something_else: ")

