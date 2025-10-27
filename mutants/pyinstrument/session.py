from __future__ import annotations

import json
import os
import sys
from collections import deque
from typing import Any

from pyinstrument.frame import Frame
from pyinstrument.frame_info import frame_info_get_identifier
from pyinstrument.frame_ops import FrameRecordType, build_frame_tree
from pyinstrument.typing import PathOrStr

# pyright: strict


ASSERTION_MESSAGE = (
    "Please raise an issue at https://github.com/joerick/pyinstrument/issues and "
    "let me know how you caused this error!"
)
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class Session:
    def xǁSessionǁ__init____mutmut_orig(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_1(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = None
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_2(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = None
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_3(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = None
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_4(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = None
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_5(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = None
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_6(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = None
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_7(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = None
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_8(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = None
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_9(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = None
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_10(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = None
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_11(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = None
        self._short_file_path_cache = {}
    def xǁSessionǁ__init____mutmut_12(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        min_interval: float,
        max_interval: float,
        sample_count: int,
        start_call_stack: list[str],
        target_description: str,
        cpu_time: float,
        sys_path: list[str],
        sys_prefixes: list[str],
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.min_interval = min_interval
        self.max_interval = max_interval
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.target_description = target_description
        self.cpu_time = cpu_time
        self.sys_path = sys_path
        self.sys_prefixes = sys_prefixes
        self._short_file_path_cache = None
    
    xǁSessionǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSessionǁ__init____mutmut_1': xǁSessionǁ__init____mutmut_1, 
        'xǁSessionǁ__init____mutmut_2': xǁSessionǁ__init____mutmut_2, 
        'xǁSessionǁ__init____mutmut_3': xǁSessionǁ__init____mutmut_3, 
        'xǁSessionǁ__init____mutmut_4': xǁSessionǁ__init____mutmut_4, 
        'xǁSessionǁ__init____mutmut_5': xǁSessionǁ__init____mutmut_5, 
        'xǁSessionǁ__init____mutmut_6': xǁSessionǁ__init____mutmut_6, 
        'xǁSessionǁ__init____mutmut_7': xǁSessionǁ__init____mutmut_7, 
        'xǁSessionǁ__init____mutmut_8': xǁSessionǁ__init____mutmut_8, 
        'xǁSessionǁ__init____mutmut_9': xǁSessionǁ__init____mutmut_9, 
        'xǁSessionǁ__init____mutmut_10': xǁSessionǁ__init____mutmut_10, 
        'xǁSessionǁ__init____mutmut_11': xǁSessionǁ__init____mutmut_11, 
        'xǁSessionǁ__init____mutmut_12': xǁSessionǁ__init____mutmut_12
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSessionǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁSessionǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁSessionǁ__init____mutmut_orig)
    xǁSessionǁ__init____mutmut_orig.__name__ = 'xǁSessionǁ__init__'

    @staticmethod
    def load(filename: PathOrStr) -> Session:
        """
        Load a previously saved session from disk.

        :param filename: The path to load from.
        :rtype: Session
        """
        with open(filename) as f:
            return Session.from_json(json.load(f))

    def xǁSessionǁsave__mutmut_orig(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(filename, "w") as f:
            json.dump(self.to_json(), f)

    def xǁSessionǁsave__mutmut_1(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(None, "w") as f:
            json.dump(self.to_json(), f)

    def xǁSessionǁsave__mutmut_2(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(filename, None) as f:
            json.dump(self.to_json(), f)

    def xǁSessionǁsave__mutmut_3(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open("w") as f:
            json.dump(self.to_json(), f)

    def xǁSessionǁsave__mutmut_4(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(filename, ) as f:
            json.dump(self.to_json(), f)

    def xǁSessionǁsave__mutmut_5(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(filename, "XXwXX") as f:
            json.dump(self.to_json(), f)

    def xǁSessionǁsave__mutmut_6(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(filename, "W") as f:
            json.dump(self.to_json(), f)

    def xǁSessionǁsave__mutmut_7(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(filename, "w") as f:
            json.dump(None, f)

    def xǁSessionǁsave__mutmut_8(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(filename, "w") as f:
            json.dump(self.to_json(), None)

    def xǁSessionǁsave__mutmut_9(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(filename, "w") as f:
            json.dump(f)

    def xǁSessionǁsave__mutmut_10(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
        with open(filename, "w") as f:
            json.dump(self.to_json(), )
    
    xǁSessionǁsave__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSessionǁsave__mutmut_1': xǁSessionǁsave__mutmut_1, 
        'xǁSessionǁsave__mutmut_2': xǁSessionǁsave__mutmut_2, 
        'xǁSessionǁsave__mutmut_3': xǁSessionǁsave__mutmut_3, 
        'xǁSessionǁsave__mutmut_4': xǁSessionǁsave__mutmut_4, 
        'xǁSessionǁsave__mutmut_5': xǁSessionǁsave__mutmut_5, 
        'xǁSessionǁsave__mutmut_6': xǁSessionǁsave__mutmut_6, 
        'xǁSessionǁsave__mutmut_7': xǁSessionǁsave__mutmut_7, 
        'xǁSessionǁsave__mutmut_8': xǁSessionǁsave__mutmut_8, 
        'xǁSessionǁsave__mutmut_9': xǁSessionǁsave__mutmut_9, 
        'xǁSessionǁsave__mutmut_10': xǁSessionǁsave__mutmut_10
    }
    
    def save(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSessionǁsave__mutmut_orig"), object.__getattribute__(self, "xǁSessionǁsave__mutmut_mutants"), args, kwargs, self)
        return result 
    
    save.__signature__ = _mutmut_signature(xǁSessionǁsave__mutmut_orig)
    xǁSessionǁsave__mutmut_orig.__name__ = 'xǁSessionǁsave'

    def xǁSessionǁto_json__mutmut_orig(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_1(self, include_frame_records: bool = False):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_2(self, include_frame_records: bool = True):
        result: dict[str, Any] = None

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_3(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "XXstart_timeXX": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_4(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "START_TIME": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_5(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "XXdurationXX": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_6(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "DURATION": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_7(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "XXmin_intervalXX": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_8(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "MIN_INTERVAL": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_9(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "XXmax_intervalXX": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_10(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "MAX_INTERVAL": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_11(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "XXsample_countXX": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_12(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "SAMPLE_COUNT": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_13(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "XXstart_call_stackXX": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_14(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "START_CALL_STACK": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_15(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "XXtarget_descriptionXX": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_16(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "TARGET_DESCRIPTION": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_17(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "XXcpu_timeXX": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_18(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "CPU_TIME": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_19(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "XXsys_pathXX": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_20(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "SYS_PATH": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_21(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "XXsys_prefixesXX": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_22(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "SYS_PREFIXES": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_23(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["frame_records"] = None

        return result

    def xǁSessionǁto_json__mutmut_24(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["XXframe_recordsXX"] = self.frame_records

        return result

    def xǁSessionǁto_json__mutmut_25(self, include_frame_records: bool = True):
        result: dict[str, Any] = {
            "start_time": self.start_time,
            "duration": self.duration,
            "min_interval": self.min_interval,
            "max_interval": self.max_interval,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "target_description": self.target_description,
            "cpu_time": self.cpu_time,
            "sys_path": self.sys_path,
            "sys_prefixes": self.sys_prefixes,
        }

        if include_frame_records:
            result["FRAME_RECORDS"] = self.frame_records

        return result
    
    xǁSessionǁto_json__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSessionǁto_json__mutmut_1': xǁSessionǁto_json__mutmut_1, 
        'xǁSessionǁto_json__mutmut_2': xǁSessionǁto_json__mutmut_2, 
        'xǁSessionǁto_json__mutmut_3': xǁSessionǁto_json__mutmut_3, 
        'xǁSessionǁto_json__mutmut_4': xǁSessionǁto_json__mutmut_4, 
        'xǁSessionǁto_json__mutmut_5': xǁSessionǁto_json__mutmut_5, 
        'xǁSessionǁto_json__mutmut_6': xǁSessionǁto_json__mutmut_6, 
        'xǁSessionǁto_json__mutmut_7': xǁSessionǁto_json__mutmut_7, 
        'xǁSessionǁto_json__mutmut_8': xǁSessionǁto_json__mutmut_8, 
        'xǁSessionǁto_json__mutmut_9': xǁSessionǁto_json__mutmut_9, 
        'xǁSessionǁto_json__mutmut_10': xǁSessionǁto_json__mutmut_10, 
        'xǁSessionǁto_json__mutmut_11': xǁSessionǁto_json__mutmut_11, 
        'xǁSessionǁto_json__mutmut_12': xǁSessionǁto_json__mutmut_12, 
        'xǁSessionǁto_json__mutmut_13': xǁSessionǁto_json__mutmut_13, 
        'xǁSessionǁto_json__mutmut_14': xǁSessionǁto_json__mutmut_14, 
        'xǁSessionǁto_json__mutmut_15': xǁSessionǁto_json__mutmut_15, 
        'xǁSessionǁto_json__mutmut_16': xǁSessionǁto_json__mutmut_16, 
        'xǁSessionǁto_json__mutmut_17': xǁSessionǁto_json__mutmut_17, 
        'xǁSessionǁto_json__mutmut_18': xǁSessionǁto_json__mutmut_18, 
        'xǁSessionǁto_json__mutmut_19': xǁSessionǁto_json__mutmut_19, 
        'xǁSessionǁto_json__mutmut_20': xǁSessionǁto_json__mutmut_20, 
        'xǁSessionǁto_json__mutmut_21': xǁSessionǁto_json__mutmut_21, 
        'xǁSessionǁto_json__mutmut_22': xǁSessionǁto_json__mutmut_22, 
        'xǁSessionǁto_json__mutmut_23': xǁSessionǁto_json__mutmut_23, 
        'xǁSessionǁto_json__mutmut_24': xǁSessionǁto_json__mutmut_24, 
        'xǁSessionǁto_json__mutmut_25': xǁSessionǁto_json__mutmut_25
    }
    
    def to_json(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSessionǁto_json__mutmut_orig"), object.__getattribute__(self, "xǁSessionǁto_json__mutmut_mutants"), args, kwargs, self)
        return result 
    
    to_json.__signature__ = _mutmut_signature(xǁSessionǁto_json__mutmut_orig)
    xǁSessionǁto_json__mutmut_orig.__name__ = 'xǁSessionǁto_json'

    @staticmethod
    def from_json(json_dict: dict[str, Any]):
        return Session(
            frame_records=json_dict["frame_records"],
            start_time=json_dict["start_time"],
            min_interval=json_dict.get("min_interval", 0.001),
            max_interval=json_dict.get("max_interval", 0.001),
            duration=json_dict["duration"],
            sample_count=json_dict["sample_count"],
            start_call_stack=json_dict["start_call_stack"],
            target_description=json_dict["target_description"],
            cpu_time=json_dict["cpu_time"] or 0,
            sys_path=json_dict.get("sys_path", sys.path),
            sys_prefixes=json_dict.get("sys_prefixes", Session.current_sys_prefixes()),
        )

    @staticmethod
    def combine(session1: Session, session2: Session) -> Session:
        """
        Combines two :class:`Session` objects.

        Sessions that are joined in this way probably shouldn't be interpreted
        as timelines, because the samples are simply concatenated. But
        aggregate views (the default) of this data will work.

        :rtype: Session
        """
        if session1.start_time > session2.start_time:
            # swap them around so that session1 is the first one
            session1, session2 = session2, session1

        return Session(
            frame_records=session1.frame_records + session2.frame_records,
            start_time=session1.start_time,
            min_interval=min(session1.min_interval, session2.min_interval),
            max_interval=max(session1.max_interval, session2.max_interval),
            duration=session1.duration + session2.duration,
            sample_count=session1.sample_count + session2.sample_count,
            start_call_stack=session1.start_call_stack,
            target_description=session1.target_description,
            cpu_time=session1.cpu_time + session2.cpu_time,
            sys_path=(
                session1.sys_path + [p for p in session2.sys_path if p not in session1.sys_path]
            ),
            sys_prefixes=list(set([*session1.sys_prefixes, *session2.sys_prefixes])),
        )

    @staticmethod
    def current_sys_prefixes() -> list[str]:
        return [sys.prefix, sys.base_prefix, sys.exec_prefix, sys.base_exec_prefix]

    def xǁSessionǁroot_frame__mutmut_orig(self, trim_stem: bool = True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = build_frame_tree(self.frame_records, context=self)

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame

    def xǁSessionǁroot_frame__mutmut_1(self, trim_stem: bool = False) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = build_frame_tree(self.frame_records, context=self)

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame

    def xǁSessionǁroot_frame__mutmut_2(self, trim_stem: bool = True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = None

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame

    def xǁSessionǁroot_frame__mutmut_3(self, trim_stem: bool = True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = build_frame_tree(None, context=self)

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame

    def xǁSessionǁroot_frame__mutmut_4(self, trim_stem: bool = True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = build_frame_tree(self.frame_records, context=None)

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame

    def xǁSessionǁroot_frame__mutmut_5(self, trim_stem: bool = True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = build_frame_tree(context=self)

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame

    def xǁSessionǁroot_frame__mutmut_6(self, trim_stem: bool = True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = build_frame_tree(self.frame_records, )

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame

    def xǁSessionǁroot_frame__mutmut_7(self, trim_stem: bool = True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = build_frame_tree(self.frame_records, context=self)

        if root_frame is not None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame

    def xǁSessionǁroot_frame__mutmut_8(self, trim_stem: bool = True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = build_frame_tree(self.frame_records, context=self)

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = None

        return root_frame

    def xǁSessionǁroot_frame__mutmut_9(self, trim_stem: bool = True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be rendered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = build_frame_tree(self.frame_records, context=self)

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(None)

        return root_frame
    
    xǁSessionǁroot_frame__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSessionǁroot_frame__mutmut_1': xǁSessionǁroot_frame__mutmut_1, 
        'xǁSessionǁroot_frame__mutmut_2': xǁSessionǁroot_frame__mutmut_2, 
        'xǁSessionǁroot_frame__mutmut_3': xǁSessionǁroot_frame__mutmut_3, 
        'xǁSessionǁroot_frame__mutmut_4': xǁSessionǁroot_frame__mutmut_4, 
        'xǁSessionǁroot_frame__mutmut_5': xǁSessionǁroot_frame__mutmut_5, 
        'xǁSessionǁroot_frame__mutmut_6': xǁSessionǁroot_frame__mutmut_6, 
        'xǁSessionǁroot_frame__mutmut_7': xǁSessionǁroot_frame__mutmut_7, 
        'xǁSessionǁroot_frame__mutmut_8': xǁSessionǁroot_frame__mutmut_8, 
        'xǁSessionǁroot_frame__mutmut_9': xǁSessionǁroot_frame__mutmut_9
    }
    
    def root_frame(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSessionǁroot_frame__mutmut_orig"), object.__getattribute__(self, "xǁSessionǁroot_frame__mutmut_mutants"), args, kwargs, self)
        return result 
    
    root_frame.__signature__ = _mutmut_signature(xǁSessionǁroot_frame__mutmut_orig)
    xǁSessionǁroot_frame__mutmut_orig.__name__ = 'xǁSessionǁroot_frame'

    def xǁSessionǁ_trim_stem__mutmut_orig(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_1(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = None

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_2(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(None)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_3(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(None) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_4(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() == frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_5(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 or len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_6(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time != 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_7(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 1 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_8(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) != 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_9(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 2:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_10(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 and frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_11(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) != 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_12(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 1 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_13(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[1].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_14(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier == start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_15(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                return

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_16(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = None

        frame.remove_from_parent()
        return frame

    def xǁSessionǁ_trim_stem__mutmut_17(self, frame: Frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(frame_info_get_identifier(info) for info in self.start_call_stack)

        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.total_self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[1]

        frame.remove_from_parent()
        return frame
    
    xǁSessionǁ_trim_stem__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSessionǁ_trim_stem__mutmut_1': xǁSessionǁ_trim_stem__mutmut_1, 
        'xǁSessionǁ_trim_stem__mutmut_2': xǁSessionǁ_trim_stem__mutmut_2, 
        'xǁSessionǁ_trim_stem__mutmut_3': xǁSessionǁ_trim_stem__mutmut_3, 
        'xǁSessionǁ_trim_stem__mutmut_4': xǁSessionǁ_trim_stem__mutmut_4, 
        'xǁSessionǁ_trim_stem__mutmut_5': xǁSessionǁ_trim_stem__mutmut_5, 
        'xǁSessionǁ_trim_stem__mutmut_6': xǁSessionǁ_trim_stem__mutmut_6, 
        'xǁSessionǁ_trim_stem__mutmut_7': xǁSessionǁ_trim_stem__mutmut_7, 
        'xǁSessionǁ_trim_stem__mutmut_8': xǁSessionǁ_trim_stem__mutmut_8, 
        'xǁSessionǁ_trim_stem__mutmut_9': xǁSessionǁ_trim_stem__mutmut_9, 
        'xǁSessionǁ_trim_stem__mutmut_10': xǁSessionǁ_trim_stem__mutmut_10, 
        'xǁSessionǁ_trim_stem__mutmut_11': xǁSessionǁ_trim_stem__mutmut_11, 
        'xǁSessionǁ_trim_stem__mutmut_12': xǁSessionǁ_trim_stem__mutmut_12, 
        'xǁSessionǁ_trim_stem__mutmut_13': xǁSessionǁ_trim_stem__mutmut_13, 
        'xǁSessionǁ_trim_stem__mutmut_14': xǁSessionǁ_trim_stem__mutmut_14, 
        'xǁSessionǁ_trim_stem__mutmut_15': xǁSessionǁ_trim_stem__mutmut_15, 
        'xǁSessionǁ_trim_stem__mutmut_16': xǁSessionǁ_trim_stem__mutmut_16, 
        'xǁSessionǁ_trim_stem__mutmut_17': xǁSessionǁ_trim_stem__mutmut_17
    }
    
    def _trim_stem(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSessionǁ_trim_stem__mutmut_orig"), object.__getattribute__(self, "xǁSessionǁ_trim_stem__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _trim_stem.__signature__ = _mutmut_signature(xǁSessionǁ_trim_stem__mutmut_orig)
    xǁSessionǁ_trim_stem__mutmut_orig.__name__ = 'xǁSessionǁ_trim_stem'

    _short_file_path_cache: dict[str, str]

    def xǁSessionǁshorten_path__mutmut_orig(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_1(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path not in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_2(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = None
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_3(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) >= 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_4(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 2:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_5(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = None
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_6(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(None, sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_7(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, None)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_8(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_9(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, )
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_10(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    break

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_11(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if not result and (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_12(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_13(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) <= len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_14(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = None

        self._short_file_path_cache[path] = result

        return result

    def xǁSessionǁshorten_path__mutmut_15(self, path: str) -> str:
        """
        Shorten a path to a more readable form, relative to sys_path. Used by
        Frame.short_file_path.
        """
        if path in self._short_file_path_cache:
            return self._short_file_path_cache[path]

        result = path
        # if os.sep doesn't appear, probably not a file path at all, more
        # likely <built-in> or similar
        if len(path.split(os.sep)) > 1:
            for sys_path_entry in self.sys_path:
                # On Windows, if path and sys_path_entry are on
                # different drives, relpath will result in exception,
                # because it cannot compute a relpath in this case.
                # The root cause is that on Windows, there is no root
                # dir like '/' on Linux.
                try:
                    candidate = os.path.relpath(path, sys_path_entry)
                except ValueError:
                    continue

                if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                    result = candidate

        self._short_file_path_cache[path] = None

        return result
    
    xǁSessionǁshorten_path__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁSessionǁshorten_path__mutmut_1': xǁSessionǁshorten_path__mutmut_1, 
        'xǁSessionǁshorten_path__mutmut_2': xǁSessionǁshorten_path__mutmut_2, 
        'xǁSessionǁshorten_path__mutmut_3': xǁSessionǁshorten_path__mutmut_3, 
        'xǁSessionǁshorten_path__mutmut_4': xǁSessionǁshorten_path__mutmut_4, 
        'xǁSessionǁshorten_path__mutmut_5': xǁSessionǁshorten_path__mutmut_5, 
        'xǁSessionǁshorten_path__mutmut_6': xǁSessionǁshorten_path__mutmut_6, 
        'xǁSessionǁshorten_path__mutmut_7': xǁSessionǁshorten_path__mutmut_7, 
        'xǁSessionǁshorten_path__mutmut_8': xǁSessionǁshorten_path__mutmut_8, 
        'xǁSessionǁshorten_path__mutmut_9': xǁSessionǁshorten_path__mutmut_9, 
        'xǁSessionǁshorten_path__mutmut_10': xǁSessionǁshorten_path__mutmut_10, 
        'xǁSessionǁshorten_path__mutmut_11': xǁSessionǁshorten_path__mutmut_11, 
        'xǁSessionǁshorten_path__mutmut_12': xǁSessionǁshorten_path__mutmut_12, 
        'xǁSessionǁshorten_path__mutmut_13': xǁSessionǁshorten_path__mutmut_13, 
        'xǁSessionǁshorten_path__mutmut_14': xǁSessionǁshorten_path__mutmut_14, 
        'xǁSessionǁshorten_path__mutmut_15': xǁSessionǁshorten_path__mutmut_15
    }
    
    def shorten_path(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁSessionǁshorten_path__mutmut_orig"), object.__getattribute__(self, "xǁSessionǁshorten_path__mutmut_mutants"), args, kwargs, self)
        return result 
    
    shorten_path.__signature__ = _mutmut_signature(xǁSessionǁshorten_path__mutmut_orig)
    xǁSessionǁshorten_path__mutmut_orig.__name__ = 'xǁSessionǁshorten_path'
