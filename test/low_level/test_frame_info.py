import inspect

from pyinstrument.low_level import stat_profile as stat_profile_c
from pyinstrument.low_level import stat_profile_python

import pytest

class AClass:
    def get_frame_info_for_a_method(self, getter_function):
        frame = inspect.currentframe()
        assert frame
        return getter_function(frame)

    def get_frame_info_with_cell_variable(self, getter_function):
        frame = inspect.currentframe()
        assert frame

        def an_inner_function():
            # reference self to make it a cell variable
            if self:
                pass

        return getter_function(frame)

    @classmethod
    def get_frame_info_for_a_class_method(cls, getter_function):
        frame = inspect.currentframe()
        assert frame
        return getter_function(frame)


def test_frame_info():
    frame = inspect.currentframe()

    assert frame
    assert stat_profile_c.get_frame_info(frame) == stat_profile_python.get_frame_info(frame)


def test_frame_info_hide_true():
    __tracebackhide__ = True

    frame = inspect.currentframe()

    assert frame
    assert stat_profile_c.get_frame_info(frame) == stat_profile_python.get_frame_info(frame)


def test_frame_info_hide_false():
    """to avoid calling FastToLocals on the c side,
    __tracebackhide__ = True
    and
    __tracebackhide__ = False
    are treated the same. All that matters is that the var is defined
    """
    __tracebackhide__ = False

    frame = inspect.currentframe()

    assert frame
    assert stat_profile_c.get_frame_info(frame) == stat_profile_python.get_frame_info(frame)


@pytest.mark.parametrize('test_function',
                         ['get_frame_info_for_a_method',
                          'get_frame_info_for_a_class_method',
                          'get_frame_info_with_cell_variable'])
def test_frame_info_with_classes(test_function):
    if 'class' in test_function:
        test_function = getattr(AClass, test_function)
    else:
        instance = AClass()
        test_function = getattr(instance, test_function)

    c_frame_info = test_function(stat_profile_c.get_frame_info)
    py_frame_info = test_function(stat_profile_python.get_frame_info)

    assert c_frame_info == py_frame_info
