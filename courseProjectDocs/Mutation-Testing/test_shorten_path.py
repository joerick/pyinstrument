from pyinstrument.session import Session

def test_shorten_path_returns_string_when_sys_path_empty():
    s = Session.__new__(Session)
    s._short_file_path_cache = {}
    s.sys_path = []

    fake_path = "not/a/real/path.py"

    result = s.shorten_path(fake_path)

    assert result == fake_path, "expected original path"