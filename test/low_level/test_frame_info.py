import inspect
import sys

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


class OuterClass:
    class InnerClass(AClass):
        pass


def frame_with_no_locals():
    return inspect.currentframe()


def test_frame_info():
    frame = inspect.currentframe()

    assert frame
    assert stat_profile_c.get_frame_info(frame) == stat_profile_python.get_frame_info(frame)


def test_frame_info_with_no_locals():
    frame = frame_with_no_locals()

    assert frame
    assert frame.f_code.co_varnames == ()
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
nested_instance = OuterClass.InnerClass()


@pytest.mark.parametrize(
    "test_function",
    [
        instance.get_frame_info_for_a_method,
        nested_instance.get_frame_info_for_a_method,
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


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires code.co_qualname")
@pytest.mark.parametrize(
    "getter", [stat_profile_c.get_frame_info, stat_profile_python.get_frame_info]
)
@pytest.mark.parametrize("del_local", [True, False])
@pytest.mark.parametrize(
    "method",
    [
        nested_instance.get_frame_info_for_a_method,
        OuterClass.InnerClass.get_frame_info_for_a_class_method,
        nested_instance.get_frame_info_with_cell_variable,
        OuterClass.InnerClass.get_frame_info_for_a_class_method_where_cls_is_reassigned,
    ],
)
def test_inherited_method_uses_defining_class(getter, del_local, method):
    info = method(getter, del_local)
    assert "\x01cAClass\x01" in info


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires code.co_qualname")
@pytest.mark.parametrize(
    "getter", [stat_profile_c.get_frame_info, stat_profile_python.get_frame_info]
)
def test_qualified_class_names(getter):
    class Outer:
        class Inner甲:
            @staticmethod
            def method():
                return inspect.currentframe()

    class Child(Outer.Inner甲):
        pass

    frame = Child.method()
    assert frame
    assert "\x01ctest_qualified_class_names.<locals>.Outer.Inner甲\x01" in getter(frame)


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires code.co_qualname")
@pytest.mark.parametrize(
    "getter", [stat_profile_c.get_frame_info, stat_profile_python.get_frame_info]
)
def test_nested_function_has_no_class_name(getter):
    def inner(self):
        return inspect.currentframe()

    frame = inner(instance)
    assert frame
    assert "\x01c" not in getter(frame)


@pytest.mark.parametrize(
    "getter", [stat_profile_c.get_frame_info, stat_profile_python.get_frame_info]
)
def test_class_body_has_no_class_name(getter):
    class Outer:
        class Inner:
            frame = inspect.currentframe()

    assert Outer.Inner.frame
    assert "\x01c" not in getter(Outer.Inner.frame)


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires code.co_qualname")
@pytest.mark.parametrize(
    "getter", [stat_profile_c.get_frame_info, stat_profile_python.get_frame_info]
)
def test_metaclass_method_uses_defining_class(getter):
    class Meta(type):
        def method(cls):
            return inspect.currentframe()

    class Target(metaclass=Meta):
        pass

    frame = Target.method()
    assert frame
    assert "\x01ctest_metaclass_method_uses_defining_class.<locals>.Meta\x01" in getter(frame)


@pytest.mark.skipif(sys.version_info < (3, 11), reason="requires code.co_qualname")
@pytest.mark.parametrize(
    "getter", [stat_profile_c.get_frame_info, stat_profile_python.get_frame_info]
)
def test_function_inside_method_has_no_class_name(getter):
    class Example:
        def method(self):
            def inner():
                if self:
                    return inspect.currentframe()

            return inner()

    frame = Example().method()
    assert frame
    assert "\x01c" not in getter(frame)
