from pyinstrument import processors
from pyinstrument.frame import Frame
from pytest import approx

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

    frame = processors.remove_importlib(frame)

    assert frame.self_time == approx(0.2)  # the root gets the self_time from the importlib
    assert frame.time() == approx(0.5)
    assert len(frame.children) == 3
    assert frame.children[0].file_path == 'sympy/polys/polyfuncs.py'
    assert frame.children[1].file_path == 'sympy/polys/partfrac.py'
    assert frame.children[2].file_path == 'sympy/polys/numberfields.py'

