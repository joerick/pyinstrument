import inspect

from pyinstrument.low_level import stat_profile as stat_profile_c
from pyinstrument.low_level import stat_profile_python


class AClass:
    def get_frame_identfier_for_a_method(self, getter_function):
        frame = inspect.currentframe()
        assert frame
        return getter_function(frame)

    @classmethod
    def get_frame_identfier_for_a_class_method(cls, getter_function):
        frame = inspect.currentframe()
        assert frame
        return getter_function(frame)


def test_frame_identifier():
    frame = inspect.currentframe()

    assert frame
    assert stat_profile_c.get_frame_identifier(frame) == stat_profile_python.get_frame_identifier(
        frame
    )


def test_frame_identifier_for_method():
    instance = AClass()
    assert instance.get_frame_identfier_for_a_method(
        stat_profile_c.get_frame_identifier
    ) == instance.get_frame_identfier_for_a_method(stat_profile_python.get_frame_identifier)
