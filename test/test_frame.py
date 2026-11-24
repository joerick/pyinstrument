from typing import Sequence

from pyinstrument.frame import Frame, FrameContext


class _TestContext:
    """Minimal FrameContext implementation for is_application_code tests."""

    def __init__(self, sys_prefixes: Sequence[str]):
        self._sys_prefixes = list(sys_prefixes)

    def shorten_path(self, path: str) -> str:
        return path

    @property
    def sys_prefixes(self) -> Sequence[str]:
        return self._sys_prefixes


def _make_frame(file_path: str, sys_prefixes: Sequence[str]) -> Frame:
    context: FrameContext = _TestContext(sys_prefixes)
    return Frame(f"work\x00{file_path}\x001", context=context)


class TestIsApplicationCode:
    def test_file_inside_prefix_is_library(self):
        frame = _make_frame("/tmp/env/lib/python3.12/site-packages/foo.py", ["/tmp/env"])
        assert frame.is_application_code is False

    def test_file_outside_prefix_is_application(self):
        frame = _make_frame("/home/user/project/main.py", ["/tmp/env"])
        assert frame.is_application_code is True

    def test_sibling_directory_is_application(self):
        # Regression: a path that shares a textual prefix with a sys_prefix
        # entry but sits in a sibling directory must not be classified as
        # library code. "/tmp/env-project/main.py" starts with "/tmp/env"
        # character-by-character, but it is not inside "/tmp/env".
        frame = _make_frame("/tmp/env-project/main.py", ["/tmp/env"])
        assert frame.is_application_code is True

    def test_sibling_directory_with_matching_name_prefix(self):
        frame = _make_frame("/opt/venvs/envprod/app/x.py", ["/opt/venvs/env"])
        assert frame.is_application_code is True

    def test_trailing_slash_prefix_inside(self):
        frame = _make_frame("/tmp/env/lib/foo.py", ["/tmp/env/"])
        assert frame.is_application_code is False

    def test_trailing_slash_prefix_sibling(self):
        frame = _make_frame("/tmp/env-project/main.py", ["/tmp/env/"])
        assert frame.is_application_code is True

    def test_path_exactly_equal_to_prefix(self):
        frame = _make_frame("/tmp/env", ["/tmp/env"])
        assert frame.is_application_code is False

    def test_windows_separators_inside_prefix(self):
        frame = _make_frame("C:\\env\\Lib\\foo.py", ["C:\\env"])
        assert frame.is_application_code is False

    def test_windows_separators_sibling(self):
        # Windows-shaped paths come up for profiles saved on Windows and
        # rendered elsewhere.
        frame = _make_frame("C:\\env-project\\main.py", ["C:\\env"])
        assert frame.is_application_code is True

    def test_cross_platform_separator_after_prefix(self):
        # A Windows-style separator appearing after a POSIX-style prefix is
        # still a path boundary, so the file should be treated as library.
        frame = _make_frame("/tmp/env\\lib\\foo.py", ["/tmp/env"])
        assert frame.is_application_code is False
