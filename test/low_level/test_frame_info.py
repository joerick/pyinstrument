import inspect

import pytest

from pyinstrument.low_level import stat_profile as stat_profile_c
from pyinstrument.low_level import stat_profile_python


class AClass:
    def get_frame_info_for_a_method(self, getter_function, del_local):
        if del_local:
            del self
        frame = inspect.currentframe()
        assert frame
        return getter_function(frame)

    def get_frame_info_with_cell_variable(self, getter_function, del_local):
        def an_inner_function():
            # reference self to make it a cell variable
            if self:
                pass

        if del_local:
            del self
        frame = inspect.currentframe()
        assert frame

        return getter_function(frame)

    @classmethod
    def get_frame_info_for_a_class_method(cls, getter_function, del_local):
        if del_local:
            del cls
        frame = inspect.currentframe()
        assert frame
        return getter_function(frame)

    @classmethod
    def get_frame_info_for_a_class_method_where_cls_is_reassigned(cls, getter_function, del_local):
        cls = 1
        if del_local:
            del cls
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


instance = AClass()


@pytest.mark.parametrize(
    "test_function",
    [
        instance.get_frame_info_for_a_method,
        AClass.get_frame_info_for_a_class_method,
        instance.get_frame_info_with_cell_variable,
        AClass.get_frame_info_for_a_class_method_where_cls_is_reassigned,
    ],
)
@pytest.mark.parametrize("del_local", [True, False])
def test_frame_info_with_classes(test_function, del_local):
    c_frame_info = test_function(stat_profile_c.get_frame_info, del_local=del_local)
    py_frame_info = test_function(stat_profile_python.get_frame_info, del_local=del_local)

    assert c_frame_info == py_frame_info
