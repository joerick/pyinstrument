import os
from pyinstrument.session import Session

def test_shorten_path_equal_depth_prefers_first():
    s = Session(
        frame_records=[],
        start_time=0.0,
        duration=0.0,
        min_interval=0.0,
        max_interval=0.0,
        sample_count=0,
        start_call_stack=[],
        target_description="test",
        cpu_time=0.0,
        sys_path=[],
        sys_prefixes=[],
    )

    path1 = os.path.join("src", "module1", "file.py")
    path2 = os.path.join("src", "module2", "file.py")

    s._short_file_path_cache.clear()

    result1 = s.shorten_path(path1)
    result2 = s.shorten_path(path2)

    assert result1 == s.shorten_path(path1)
    assert result2.endswith("file.py")
