import pytest
import t
def test_t(capsys):
    with pytest.raises(SystemExit) as e:
        t.main([''])
    retv,_ = e.value.args
    out, err = capsys.readouterr()
    assert out == '\n'
    assert err == 'arg empty'