import sys
from test.util import calculate_frame_tree_times

from pytest import approx

from pyinstrument import processors
from pyinstrument.frame import SELF_TIME_FRAME_IDENTIFIER, Frame

ALL_PROCESSORS = [
    processors.aggregate_repeated_calls,
    processors.group_library_frames_processor,
    processors.merge_consecutive_self_time,
    processors.remove_importlib,
    processors.remove_tracebackhide,
    processors.remove_unnecessary_self_time_nodes,
    processors.remove_irrelevant_nodes,
]


def self_time_frame(time):
    return Frame(SELF_TIME_FRAME_IDENTIFIER, time=time)


def test_frame_passthrough_none():
    for processor in ALL_PROCESSORS:
        assert processor(None, options={}) is None


def test_remove_importlib():
    frame = Frame(
        identifier_or_frame_info="<module>\x00sympy/__init__.py\x0012",
        children=[
            Frame(
                identifier_or_frame_info="_handle_fromlist\x00../<frozen importlib._bootstrap>\x00997",
                children=[
                    self_time_frame(0.15),
                    Frame(
                        identifier_or_frame_info="_find_and_load\x00../<frozen importlib._bootstrap>\x00997",
                        children=[
                            self_time_frame(0.05),
                            Frame(
                                identifier_or_frame_info="<module>\x00sympy/polys/polyfuncs.py\x001",
                                children=[self_time_frame(0.05)],
                            ),
                            Frame(
                                identifier_or_frame_info="<module>\x00sympy/polys/partfrac.py\x001",
                                children=[self_time_frame(0.2)],
                            ),
                        ],
                    ),
                    Frame(
                        identifier_or_frame_info="<module>\x00sympy/polys/numberfields.py\x001",
                        children=[self_time_frame(0.05)],
                    ),
                ],
            )
        ],
    )

    calculate_frame_tree_times(frame)
    frame.self_check()

    assert frame.total_self_time == 0.0
    assert frame.time == approx(0.5)

    frame = processors.remove_importlib(frame, options={})
    assert frame
    frame.self_check()

    assert frame.total_self_time == approx(0.2)  # the root gets the self_time from the importlib
    assert frame.time == approx(0.5)
    assert len(frame.children) == 5
    assert frame.children[0].identifier == SELF_TIME_FRAME_IDENTIFIER
    assert frame.children[0].time == 0.15
    assert frame.children[1].identifier == SELF_TIME_FRAME_IDENTIFIER
    assert frame.children[1].time == 0.05

    assert frame.children[2].file_path == "sympy/polys/polyfuncs.py"
    assert frame.children[3].file_path == "sympy/polys/partfrac.py"
    assert frame.children[4].file_path == "sympy/polys/numberfields.py"


def test_remove_hidden():
    frame = Frame(
        identifier_or_frame_info="<module>\x00sympy/__init__.py\x0012\x01h0",
        children=[
            Frame(
                identifier_or_frame_info="_handle_fromlist\x00../foo.py\x00997\x01h1",
                children=[
                    self_time_frame(0.15),
                    Frame(
                        identifier_or_frame_info="_find_and_load\x00../foo.py\x00997\x01h1",
                        children=[
                            self_time_frame(0.05),
                            Frame(
                                identifier_or_frame_info="<module>\x00sympy/polys/polyfuncs.py\x001\x01h0",
                                children=[self_time_frame(0.05)],
                            ),
                            Frame(
                                identifier_or_frame_info="<module>\x00sympy/polys/partfrac.py\x001\x01h0",
                                children=[self_time_frame(0.2)],
                            ),
                        ],
                    ),
                    Frame(
                        identifier_or_frame_info="<module>\x00sympy/polys/numberfields.py\x001\x01h0",
                        children=[self_time_frame(0.05)],
                    ),
                ],
            )
        ],
    )

    calculate_frame_tree_times(frame)
    frame.self_check()

    assert frame.total_self_time == 0.0
    assert frame.time == approx(0.5)

    frame = processors.remove_tracebackhide(frame, options={})
    assert frame
    frame.self_check()

    assert frame.total_self_time == approx(0.2)  # the root gets the self_time from the importlib
    assert frame.time == approx(0.5)
    assert len(frame.children) == 5
    assert frame.children[0].identifier == SELF_TIME_FRAME_IDENTIFIER
    assert frame.children[0].time == 0.15
    assert frame.children[1].identifier == SELF_TIME_FRAME_IDENTIFIER
    assert frame.children[1].time == 0.05


def test_merge_consecutive_self_time():
    frame = Frame(
        identifier_or_frame_info="<module>\x00cibuildwheel/__init__.py\x0012",
        children=[
            Frame(
                identifier_or_frame_info="strip_newlines\x00cibuildwheel/utils.py\x00997",
                children=[self_time_frame(0.1)],
            ),
            self_time_frame(0.2),
            self_time_frame(0.1),
            Frame(
                identifier_or_frame_info="calculate_metrics\x00cibuildwheel/utils.py\x007",
                children=[self_time_frame(0.1)],
            ),
            self_time_frame(0.05),
        ],
    )

    calculate_frame_tree_times(frame)
    frame.self_check()

    assert frame.time == approx(0.55)

    frame = processors.merge_consecutive_self_time(frame, options={})
    assert frame
    frame.self_check()

    assert frame.time == approx(0.55)
    assert len(frame.children) == 4
    assert frame.children[0].total_self_time == approx(0.1)
    assert frame.children[1].identifier == SELF_TIME_FRAME_IDENTIFIER
    assert frame.children[1].time == approx(0.3)
    assert frame.children[2].time == approx(0.1)
    assert frame.children[3].time == approx(0.05)
    assert frame.children[3].identifier == SELF_TIME_FRAME_IDENTIFIER


def test_aggregate_repeated_calls():
    frame = Frame(
        identifier_or_frame_info="<module>\x00cibuildwheel/__init__.py\x0012",
        children=[
            Frame(
                identifier_or_frame_info="strip_newlines\x00cibuildwheel/utils.py\x00997",
                children=[
                    self_time_frame(0.1),
                    Frame(
                        identifier_or_frame_info="scan_string\x00cibuildwheel/utils.py\x0054",
                        children=[self_time_frame(0.2)],
                    ),
                ],
            ),
            self_time_frame(0.1),
            Frame(
                identifier_or_frame_info="strip_newlines\x00cibuildwheel/utils.py\x00997",
                children=[self_time_frame(0.05)],
            ),
            self_time_frame(0.2),
            Frame(
                identifier_or_frame_info="calculate_metrics\x00cibuildwheel/utils.py\x007",
                children=[self_time_frame(0.1)],
            ),
            self_time_frame(0.05),
        ],
    )

    calculate_frame_tree_times(frame)
    frame.self_check()

    assert frame.time == approx(0.8)

    frame = processors.aggregate_repeated_calls(frame, options={})

    assert frame
    frame.self_check()
    assert frame.time == approx(0.8)
    # children should be sorted by time
    assert len(frame.children) == 3
    assert frame.children[0].function == "strip_newlines"
    assert frame.children[0].time == approx(0.35)
    assert frame.children[0].children[0].function == "scan_string"
    assert frame.children[1].identifier == SELF_TIME_FRAME_IDENTIFIER
    assert frame.children[1].time == approx(0.35)
    assert frame.children[2].function == "calculate_metrics"


def test_remove_irrelevant_nodes():
    frame = Frame(
        identifier_or_frame_info="<module>\x00cibuildwheel/__init__.py\x0012",
        children=[
            Frame(
                identifier_or_frame_info="strip_newlines\x00cibuildwheel/utils.py\x00997",
                children=[
                    Frame(
                        identifier_or_frame_info="scan_string\x00cibuildwheel/utils.py\x0054",
                        children=[self_time_frame(10)],
                    ),
                ],
            ),
            self_time_frame(0.5),
            Frame(
                identifier_or_frame_info="strip_newlines\x00cibuildwheel/utils.py\x00997",
                children=[self_time_frame(0.5)],
            ),
            Frame(
                identifier_or_frame_info="calculate_metrics\x00cibuildwheel/utils.py\x007",
                children=[self_time_frame(0.01)],
            ),
        ],
    )

    calculate_frame_tree_times(frame)
    frame.self_check()

    assert frame.time == approx(11.01)

    frame = processors.remove_irrelevant_nodes(frame, options={})

    assert frame
    frame.self_check()
    assert frame.time == approx(11.01)
    # check the calculate metrics function was deleted
    assert len(frame.children) == 3
    assert "calculate_metrics" not in [f.function for f in frame.children]


def test_remove_unnecessary_self_time_nodes():
    frame = Frame(
        identifier_or_frame_info="<module>\x00cibuildwheel/__init__.py\x0012",
        children=[
            Frame(
                identifier_or_frame_info="strip_newlines\x00cibuildwheel/utils.py\x00997",
                children=[
                    self_time_frame(0.2),
                ],
            ),
            self_time_frame(0.5),
            Frame(
                identifier_or_frame_info="strip_newlines\x00cibuildwheel/utils.py\x00997",
                children=[self_time_frame(0.5)],
            ),
            Frame(
                identifier_or_frame_info="calculate_metrics\x00cibuildwheel/utils.py\x007",
                children=[self_time_frame(0.1)],
            ),
        ],
    )
    calculate_frame_tree_times(frame)
    frame.self_check()

    assert frame.time == approx(1.3)

    frame = processors.remove_unnecessary_self_time_nodes(frame, options={})

    assert frame
    frame.self_check()
    assert frame.time == approx(1.3)
    assert len(frame.children) == 4
    # check the self time node was deleted
    strip_newlines_frame = frame.children[0]
    assert strip_newlines_frame.function == "strip_newlines"
    assert len(strip_newlines_frame.children) == 0
    # check the time was absorbed into the parent
    assert strip_newlines_frame.absorbed_time == 0.2
    assert strip_newlines_frame.time == 0.2


def test_group_library_frames_processor():
    frame = Frame(
        identifier_or_frame_info="<module>\x00cibuildwheel/__init__.py\x0012",
        children=[
            Frame(
                identifier_or_frame_info="library_function\x00env/lib/python3.6/django/__init__.py\x00997",
                children=[
                    Frame(
                        identifier_or_frame_info="library_inner\x00env/lib/python3.6/django/http.py\x0054",
                        children=[
                            Frame(
                                identifier_or_frame_info="library_callback\x00env/lib/python3.6/django/views.py\x0054",
                                children=[
                                    Frame(
                                        identifier_or_frame_info="<module>\x00cibuildwheel/views.py\x0012",
                                        children=[self_time_frame(0.3)],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            self_time_frame(0.5),
            Frame(
                identifier_or_frame_info="strip_newlines\x00cibuildwheel/utils.py\x00997",
                children=[self_time_frame(0.5)],
            ),
            Frame(
                identifier_or_frame_info="calculate_metrics\x00cibuildwheel/utils.py\x007",
                children=[self_time_frame(0.1)],
            ),
        ],
    )
    calculate_frame_tree_times(frame)
    frame.self_check()

    assert frame.time == approx(1.4)

    frame = processors.group_library_frames_processor(frame, options={})

    assert frame
    frame.self_check()
    assert frame.time == approx(1.4)
    group_root = frame.children[0]

    group = group_root.group
    assert group
    assert group.root == group_root

    for frame in group.frames:
        assert frame.group == group

    assert group_root in group.frames
    assert group_root.children[0] in group.frames
    assert group_root.children[0].children[0] in group.frames
    assert group_root.children[0].children[0] in group.exit_frames
    assert group_root.children[0].children[0].children[0] not in group.frames

    old_sys_path = sys.path[:]
    sys.path.append("env/lib/python3.6")
    assert group.libraries == ["django"]
    sys.path[:] = old_sys_path
