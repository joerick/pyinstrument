from pyinstrument import processors
from pyinstrument.frame import Frame, SelfTimeFrame
from pytest import approx

all_processors = [
    processors.aggregate_repeated_calls,
    processors.group_library_frames_processor,
    processors.merge_consecutive_self_time,
    processors.remove_importlib,
    processors.remove_unnecessary_self_time_nodes,
    processors.remove_irrelevant_nodes,
]

def test_remove_importlib():
    frame = Frame(
        identifier='<module>\x00sympy/__init__.py\x0012',
        children=[
            Frame(
                identifier='_handle_fromlist\x00../<frozen importlib._bootstrap>\x00997',
                self_time=0.1,
                children=[
                    Frame(
                        identifier='_find_and_load\x00../<frozen importlib._bootstrap>\x00997',
                        self_time=0.1,
                        children=[
                            Frame(
                                identifier='<module>\x00sympy/polys/polyfuncs.py\x001',
                                self_time=0.05,
                            ),
                            Frame(
                                identifier='<module>\x00sympy/polys/partfrac.py\x001',
                                self_time=0.2,
                            )
                        ]
                    ),
                    Frame(
                        identifier='<module>\x00sympy/polys/numberfields.py\x001',
                        self_time=0.05,
                    )
                ]
            )
        ]
    )

    assert frame.self_time == 0.0
    assert frame.time() == approx(0.5)

    frame = processors.remove_importlib(frame, options={})

    assert frame.self_time == approx(0.2)  # the root gets the self_time from the importlib
    assert frame.time() == approx(0.5)
    assert len(frame.children) == 3
    assert frame.children[0].file_path == 'sympy/polys/polyfuncs.py'
    assert frame.children[1].file_path == 'sympy/polys/partfrac.py'
    assert frame.children[2].file_path == 'sympy/polys/numberfields.py'


def test_frame_passthrough_none():
    for processor in all_processors:
        assert processor(None, options={}) is None


def test_merge_consecutive_self_time():
    frame = Frame(
        identifier='<module>\x00cibuildwheel/__init__.py\x0012',
        children=[
            Frame(
                identifier='strip_newlines\x00cibuildwheel/utils.py\x00997',
                self_time=0.1),
            SelfTimeFrame(
                self_time=0.2,
            ),
            SelfTimeFrame(
                self_time=0.1,
            ),
            Frame(
                identifier='calculate_metrics\x00cibuildwheel/utils.py\x007',
                self_time=0.1),
            SelfTimeFrame(
                self_time=0.05,
            ),
        ]
    )

    assert frame.time() == approx(0.55)

    frame = processors.merge_consecutive_self_time(frame, options={})

    assert frame.time() == approx(0.55)
    assert len(frame.children) == 4
    assert frame.children[0].self_time == approx(0.1)
    assert frame.children[1].self_time == approx(0.3)
    assert isinstance(frame.children[1], SelfTimeFrame)
    assert frame.children[2].self_time == approx(0.1)
    assert frame.children[3].self_time == approx(0.05)
    assert isinstance(frame.children[3], SelfTimeFrame)
