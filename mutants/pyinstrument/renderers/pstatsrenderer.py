from __future__ import annotations

import marshal
from typing import Any, Dict, Tuple

from pyinstrument import processors
from pyinstrument.frame import Frame
from pyinstrument.renderers.base import FrameRenderer, ProcessorList
from pyinstrument.session import Session

# pyright: strict

FrameKey = Tuple[str, int, str]
CallerValue = Tuple[float, int, float, float]
FrameValue = Tuple[float, int, float, float, Dict[FrameKey, CallerValue]]
StatsDict = Dict[FrameKey, FrameValue]
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


class PstatsRenderer(FrameRenderer):
    """
    Outputs a marshaled dict, containing processed frames in pstat format,
    suitable for processing by gprof2dot and snakeviz.
    """

    output_file_extension = "pstats"
    output_is_binary = True

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def xǁPstatsRendererǁframe_key__mutmut_orig(self, frame: Frame) -> FrameKey:
        return (frame.file_path or "", frame.line_no or 0, frame.function)

    def xǁPstatsRendererǁframe_key__mutmut_1(self, frame: Frame) -> FrameKey:
        return (frame.file_path and "", frame.line_no or 0, frame.function)

    def xǁPstatsRendererǁframe_key__mutmut_2(self, frame: Frame) -> FrameKey:
        return (frame.file_path or "XXXX", frame.line_no or 0, frame.function)

    def xǁPstatsRendererǁframe_key__mutmut_3(self, frame: Frame) -> FrameKey:
        return (frame.file_path or "", frame.line_no and 0, frame.function)

    def xǁPstatsRendererǁframe_key__mutmut_4(self, frame: Frame) -> FrameKey:
        return (frame.file_path or "", frame.line_no or 1, frame.function)
    
    xǁPstatsRendererǁframe_key__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPstatsRendererǁframe_key__mutmut_1': xǁPstatsRendererǁframe_key__mutmut_1, 
        'xǁPstatsRendererǁframe_key__mutmut_2': xǁPstatsRendererǁframe_key__mutmut_2, 
        'xǁPstatsRendererǁframe_key__mutmut_3': xǁPstatsRendererǁframe_key__mutmut_3, 
        'xǁPstatsRendererǁframe_key__mutmut_4': xǁPstatsRendererǁframe_key__mutmut_4
    }
    
    def frame_key(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPstatsRendererǁframe_key__mutmut_orig"), object.__getattribute__(self, "xǁPstatsRendererǁframe_key__mutmut_mutants"), args, kwargs, self)
        return result 
    
    frame_key.__signature__ = _mutmut_signature(xǁPstatsRendererǁframe_key__mutmut_orig)
    xǁPstatsRendererǁframe_key__mutmut_orig.__name__ = 'xǁPstatsRendererǁframe_key'

    def xǁPstatsRendererǁrender_frame__mutmut_orig(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_1(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is not None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_2(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = None

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_3(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(None)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_4(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_5(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = None
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_6(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = +1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_7(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -2
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_8(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = None
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_9(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = +1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_10(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -2
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_11(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = None
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_12(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 1
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_13(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = None
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_14(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 1
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_15(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = None
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_16(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = None

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_17(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time = frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_18(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time -= frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_19(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time = frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_20(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time -= frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_21(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = None
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_22(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(None)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_23(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_24(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = None
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_25(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = +1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_26(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -2
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_27(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = None
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_28(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = +1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_29(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -2
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_30(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = None
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_31(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 1
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_32(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = None
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_33(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 1
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_34(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = None

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_35(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time = frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_36(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time -= frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_37(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time = frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_38(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time -= frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_39(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = None

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_40(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = None

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_41(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if child.is_synthetic:
                self.render_frame(child, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_42(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(None, stats)

    def xǁPstatsRendererǁrender_frame__mutmut_43(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, None)

    def xǁPstatsRendererǁrender_frame__mutmut_44(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(stats)

    def xǁPstatsRendererǁrender_frame__mutmut_45(self, frame: Frame | None, stats: StatsDict) -> None:
        if frame is None:
            return

        key = self.frame_key(frame)

        if key not in stats:
            # create a new entry
            # being a statistical profiler, we don't know the exact call time or
            # number of calls, they're stubbed out
            call_time = -1
            number_calls = -1
            total_time = 0
            cumulative_time = 0
            callers: dict[FrameKey, CallerValue] = {}
        else:
            call_time, number_calls, total_time, cumulative_time, callers = stats[key]

        # update the total time and cumulative time
        total_time += frame.total_self_time
        cumulative_time += frame.time

        if frame.parent:
            parent_key = self.frame_key(frame.parent)
            if parent_key not in callers:
                p_call_time = -1
                p_number_calls = -1
                p_total_time = 0
                p_cumulative_time = 0
            else:
                p_call_time, p_number_calls, p_total_time, p_cumulative_time = callers[parent_key]

            p_total_time += frame.total_self_time
            p_cumulative_time += frame.time

            callers[parent_key] = p_call_time, p_number_calls, p_total_time, p_cumulative_time

        stats[key] = (call_time, number_calls, total_time, cumulative_time, callers)

        for child in frame.children:
            if not child.is_synthetic:
                self.render_frame(child, )
    
    xǁPstatsRendererǁrender_frame__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPstatsRendererǁrender_frame__mutmut_1': xǁPstatsRendererǁrender_frame__mutmut_1, 
        'xǁPstatsRendererǁrender_frame__mutmut_2': xǁPstatsRendererǁrender_frame__mutmut_2, 
        'xǁPstatsRendererǁrender_frame__mutmut_3': xǁPstatsRendererǁrender_frame__mutmut_3, 
        'xǁPstatsRendererǁrender_frame__mutmut_4': xǁPstatsRendererǁrender_frame__mutmut_4, 
        'xǁPstatsRendererǁrender_frame__mutmut_5': xǁPstatsRendererǁrender_frame__mutmut_5, 
        'xǁPstatsRendererǁrender_frame__mutmut_6': xǁPstatsRendererǁrender_frame__mutmut_6, 
        'xǁPstatsRendererǁrender_frame__mutmut_7': xǁPstatsRendererǁrender_frame__mutmut_7, 
        'xǁPstatsRendererǁrender_frame__mutmut_8': xǁPstatsRendererǁrender_frame__mutmut_8, 
        'xǁPstatsRendererǁrender_frame__mutmut_9': xǁPstatsRendererǁrender_frame__mutmut_9, 
        'xǁPstatsRendererǁrender_frame__mutmut_10': xǁPstatsRendererǁrender_frame__mutmut_10, 
        'xǁPstatsRendererǁrender_frame__mutmut_11': xǁPstatsRendererǁrender_frame__mutmut_11, 
        'xǁPstatsRendererǁrender_frame__mutmut_12': xǁPstatsRendererǁrender_frame__mutmut_12, 
        'xǁPstatsRendererǁrender_frame__mutmut_13': xǁPstatsRendererǁrender_frame__mutmut_13, 
        'xǁPstatsRendererǁrender_frame__mutmut_14': xǁPstatsRendererǁrender_frame__mutmut_14, 
        'xǁPstatsRendererǁrender_frame__mutmut_15': xǁPstatsRendererǁrender_frame__mutmut_15, 
        'xǁPstatsRendererǁrender_frame__mutmut_16': xǁPstatsRendererǁrender_frame__mutmut_16, 
        'xǁPstatsRendererǁrender_frame__mutmut_17': xǁPstatsRendererǁrender_frame__mutmut_17, 
        'xǁPstatsRendererǁrender_frame__mutmut_18': xǁPstatsRendererǁrender_frame__mutmut_18, 
        'xǁPstatsRendererǁrender_frame__mutmut_19': xǁPstatsRendererǁrender_frame__mutmut_19, 
        'xǁPstatsRendererǁrender_frame__mutmut_20': xǁPstatsRendererǁrender_frame__mutmut_20, 
        'xǁPstatsRendererǁrender_frame__mutmut_21': xǁPstatsRendererǁrender_frame__mutmut_21, 
        'xǁPstatsRendererǁrender_frame__mutmut_22': xǁPstatsRendererǁrender_frame__mutmut_22, 
        'xǁPstatsRendererǁrender_frame__mutmut_23': xǁPstatsRendererǁrender_frame__mutmut_23, 
        'xǁPstatsRendererǁrender_frame__mutmut_24': xǁPstatsRendererǁrender_frame__mutmut_24, 
        'xǁPstatsRendererǁrender_frame__mutmut_25': xǁPstatsRendererǁrender_frame__mutmut_25, 
        'xǁPstatsRendererǁrender_frame__mutmut_26': xǁPstatsRendererǁrender_frame__mutmut_26, 
        'xǁPstatsRendererǁrender_frame__mutmut_27': xǁPstatsRendererǁrender_frame__mutmut_27, 
        'xǁPstatsRendererǁrender_frame__mutmut_28': xǁPstatsRendererǁrender_frame__mutmut_28, 
        'xǁPstatsRendererǁrender_frame__mutmut_29': xǁPstatsRendererǁrender_frame__mutmut_29, 
        'xǁPstatsRendererǁrender_frame__mutmut_30': xǁPstatsRendererǁrender_frame__mutmut_30, 
        'xǁPstatsRendererǁrender_frame__mutmut_31': xǁPstatsRendererǁrender_frame__mutmut_31, 
        'xǁPstatsRendererǁrender_frame__mutmut_32': xǁPstatsRendererǁrender_frame__mutmut_32, 
        'xǁPstatsRendererǁrender_frame__mutmut_33': xǁPstatsRendererǁrender_frame__mutmut_33, 
        'xǁPstatsRendererǁrender_frame__mutmut_34': xǁPstatsRendererǁrender_frame__mutmut_34, 
        'xǁPstatsRendererǁrender_frame__mutmut_35': xǁPstatsRendererǁrender_frame__mutmut_35, 
        'xǁPstatsRendererǁrender_frame__mutmut_36': xǁPstatsRendererǁrender_frame__mutmut_36, 
        'xǁPstatsRendererǁrender_frame__mutmut_37': xǁPstatsRendererǁrender_frame__mutmut_37, 
        'xǁPstatsRendererǁrender_frame__mutmut_38': xǁPstatsRendererǁrender_frame__mutmut_38, 
        'xǁPstatsRendererǁrender_frame__mutmut_39': xǁPstatsRendererǁrender_frame__mutmut_39, 
        'xǁPstatsRendererǁrender_frame__mutmut_40': xǁPstatsRendererǁrender_frame__mutmut_40, 
        'xǁPstatsRendererǁrender_frame__mutmut_41': xǁPstatsRendererǁrender_frame__mutmut_41, 
        'xǁPstatsRendererǁrender_frame__mutmut_42': xǁPstatsRendererǁrender_frame__mutmut_42, 
        'xǁPstatsRendererǁrender_frame__mutmut_43': xǁPstatsRendererǁrender_frame__mutmut_43, 
        'xǁPstatsRendererǁrender_frame__mutmut_44': xǁPstatsRendererǁrender_frame__mutmut_44, 
        'xǁPstatsRendererǁrender_frame__mutmut_45': xǁPstatsRendererǁrender_frame__mutmut_45
    }
    
    def render_frame(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPstatsRendererǁrender_frame__mutmut_orig"), object.__getattribute__(self, "xǁPstatsRendererǁrender_frame__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render_frame.__signature__ = _mutmut_signature(xǁPstatsRendererǁrender_frame__mutmut_orig)
    xǁPstatsRendererǁrender_frame__mutmut_orig.__name__ = 'xǁPstatsRendererǁrender_frame'

    def xǁPstatsRendererǁrender__mutmut_orig(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_1(self, session: Session):
        frame = None

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_2(self, session: Session):
        frame = self.preprocess(None)

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_3(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = None
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_4(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(None, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_5(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, None)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_6(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_7(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, )

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_8(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding=None, errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_9(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors=None)

    def xǁPstatsRendererǁrender__mutmut_10(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_11(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", )

    def xǁPstatsRendererǁrender__mutmut_12(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(None).decode(encoding="utf-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_13(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="XXutf-8XX", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_14(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="UTF-8", errors="surrogateescape")

    def xǁPstatsRendererǁrender__mutmut_15(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="XXsurrogateescapeXX")

    def xǁPstatsRendererǁrender__mutmut_16(self, session: Session):
        frame = self.preprocess(session.root_frame())

        stats: StatsDict = {}
        self.render_frame(frame, stats)

        # marshal.dumps returns bytes, so we need to decode it to a string
        # using surrogateescape
        return marshal.dumps(stats).decode(encoding="utf-8", errors="SURROGATEESCAPE")
    
    xǁPstatsRendererǁrender__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPstatsRendererǁrender__mutmut_1': xǁPstatsRendererǁrender__mutmut_1, 
        'xǁPstatsRendererǁrender__mutmut_2': xǁPstatsRendererǁrender__mutmut_2, 
        'xǁPstatsRendererǁrender__mutmut_3': xǁPstatsRendererǁrender__mutmut_3, 
        'xǁPstatsRendererǁrender__mutmut_4': xǁPstatsRendererǁrender__mutmut_4, 
        'xǁPstatsRendererǁrender__mutmut_5': xǁPstatsRendererǁrender__mutmut_5, 
        'xǁPstatsRendererǁrender__mutmut_6': xǁPstatsRendererǁrender__mutmut_6, 
        'xǁPstatsRendererǁrender__mutmut_7': xǁPstatsRendererǁrender__mutmut_7, 
        'xǁPstatsRendererǁrender__mutmut_8': xǁPstatsRendererǁrender__mutmut_8, 
        'xǁPstatsRendererǁrender__mutmut_9': xǁPstatsRendererǁrender__mutmut_9, 
        'xǁPstatsRendererǁrender__mutmut_10': xǁPstatsRendererǁrender__mutmut_10, 
        'xǁPstatsRendererǁrender__mutmut_11': xǁPstatsRendererǁrender__mutmut_11, 
        'xǁPstatsRendererǁrender__mutmut_12': xǁPstatsRendererǁrender__mutmut_12, 
        'xǁPstatsRendererǁrender__mutmut_13': xǁPstatsRendererǁrender__mutmut_13, 
        'xǁPstatsRendererǁrender__mutmut_14': xǁPstatsRendererǁrender__mutmut_14, 
        'xǁPstatsRendererǁrender__mutmut_15': xǁPstatsRendererǁrender__mutmut_15, 
        'xǁPstatsRendererǁrender__mutmut_16': xǁPstatsRendererǁrender__mutmut_16
    }
    
    def render(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPstatsRendererǁrender__mutmut_orig"), object.__getattribute__(self, "xǁPstatsRendererǁrender__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render.__signature__ = _mutmut_signature(xǁPstatsRendererǁrender__mutmut_orig)
    xǁPstatsRendererǁrender__mutmut_orig.__name__ = 'xǁPstatsRendererǁrender'

    def default_processors(self) -> ProcessorList:
        return [
            processors.remove_importlib,
            processors.remove_tracebackhide,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.remove_irrelevant_nodes,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_first_pyinstrument_frames_processor,
        ]
