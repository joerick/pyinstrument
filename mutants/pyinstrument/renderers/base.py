from __future__ import annotations

import contextlib
from typing import Any, List

from pyinstrument import processors
from pyinstrument.frame import Frame
from pyinstrument.session import Session

# pyright: strict


ProcessorList = List[processors.ProcessorType]
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


class Renderer:
    """
    Abstract base class for renderers.
    """

    output_file_extension: str = "txt"
    """
    Renderer output file extension without dot prefix. The default value is `txt`
    """

    output_is_binary: bool = False
    """
    Whether the output of this renderer is binary data. The default value is `False`.
    """

    def __init__(self):
        pass

    def render(self, session: Session) -> str:
        """
        Return a string that contains the rendered form of `frame`.
        """
        raise NotImplementedError()

    class MisconfigurationError(Exception):
        pass


class FrameRenderer(Renderer):
    """
    An abstract base class for renderers that process Frame objects using
    processor functions. Provides a common interface to manipulate the
    processors before rendering.
    """

    processors: ProcessorList
    """
    Processors installed on this renderer. This property is defined on the
    base class to provide a common way for users to add and
    manipulate them before calling :func:`render`.
    """

    processor_options: dict[str, Any]
    """
    Dictionary containing processor options, passed to each processor.
    """

    show_all: bool
    timeline: bool

    def xǁFrameRendererǁ__init____mutmut_orig(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_1(
        self,
        show_all: bool = True,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_2(
        self,
        show_all: bool = False,
        timeline: bool = True,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_3(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = None
        self.processor_options = processor_options or {}

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_4(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = None

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_5(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options and {}

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_6(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        self.show_all = None
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_7(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        self.show_all = show_all
        self.timeline = None

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_8(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(None):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_9(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(None)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_10(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(None):
                self.processors.remove(processors.aggregate_repeated_calls)

    def xǁFrameRendererǁ__init____mutmut_11(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide or filter frames - show everything that pyinstrument captures.
        :param timeline: Instead of aggregating time, leave the samples in chronological order.
        :param processor_options: A dictionary of processor options.
        """
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        self.show_all = show_all
        self.timeline = timeline

        if show_all:
            for p in (
                processors.group_library_frames_processor,
                processors.remove_importlib,
                processors.remove_irrelevant_nodes,
                processors.remove_tracebackhide,
                # note: we're not removing these processors
                # processors.remove_unnecessary_self_time_nodes,
                #    (still hide the inner pyinstrument synthetic frames)
                # processors.remove_first_pyinstrument_frames_processor,
                #    (still hide the outer pyinstrument calling frames)
            ):
                with contextlib.suppress(ValueError):
                    # don't care if the processor isn't in the list
                    self.processors.remove(p)

        if timeline:
            with contextlib.suppress(ValueError):
                self.processors.remove(None)
    
    xǁFrameRendererǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameRendererǁ__init____mutmut_1': xǁFrameRendererǁ__init____mutmut_1, 
        'xǁFrameRendererǁ__init____mutmut_2': xǁFrameRendererǁ__init____mutmut_2, 
        'xǁFrameRendererǁ__init____mutmut_3': xǁFrameRendererǁ__init____mutmut_3, 
        'xǁFrameRendererǁ__init____mutmut_4': xǁFrameRendererǁ__init____mutmut_4, 
        'xǁFrameRendererǁ__init____mutmut_5': xǁFrameRendererǁ__init____mutmut_5, 
        'xǁFrameRendererǁ__init____mutmut_6': xǁFrameRendererǁ__init____mutmut_6, 
        'xǁFrameRendererǁ__init____mutmut_7': xǁFrameRendererǁ__init____mutmut_7, 
        'xǁFrameRendererǁ__init____mutmut_8': xǁFrameRendererǁ__init____mutmut_8, 
        'xǁFrameRendererǁ__init____mutmut_9': xǁFrameRendererǁ__init____mutmut_9, 
        'xǁFrameRendererǁ__init____mutmut_10': xǁFrameRendererǁ__init____mutmut_10, 
        'xǁFrameRendererǁ__init____mutmut_11': xǁFrameRendererǁ__init____mutmut_11
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameRendererǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁFrameRendererǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁFrameRendererǁ__init____mutmut_orig)
    xǁFrameRendererǁ__init____mutmut_orig.__name__ = 'xǁFrameRendererǁ__init__'

    def default_processors(self) -> ProcessorList:
        """
        Return a list of processors that this renderer uses by default.
        """
        raise NotImplementedError()

    def xǁFrameRendererǁpreprocess__mutmut_orig(self, root_frame: Frame | None) -> Frame | None:
        frame = root_frame
        for processor in self.processors:
            frame = processor(frame, options=self.processor_options)
        return frame

    def xǁFrameRendererǁpreprocess__mutmut_1(self, root_frame: Frame | None) -> Frame | None:
        frame = None
        for processor in self.processors:
            frame = processor(frame, options=self.processor_options)
        return frame

    def xǁFrameRendererǁpreprocess__mutmut_2(self, root_frame: Frame | None) -> Frame | None:
        frame = root_frame
        for processor in self.processors:
            frame = None
        return frame

    def xǁFrameRendererǁpreprocess__mutmut_3(self, root_frame: Frame | None) -> Frame | None:
        frame = root_frame
        for processor in self.processors:
            frame = processor(None, options=self.processor_options)
        return frame

    def xǁFrameRendererǁpreprocess__mutmut_4(self, root_frame: Frame | None) -> Frame | None:
        frame = root_frame
        for processor in self.processors:
            frame = processor(frame, options=None)
        return frame

    def xǁFrameRendererǁpreprocess__mutmut_5(self, root_frame: Frame | None) -> Frame | None:
        frame = root_frame
        for processor in self.processors:
            frame = processor(options=self.processor_options)
        return frame

    def xǁFrameRendererǁpreprocess__mutmut_6(self, root_frame: Frame | None) -> Frame | None:
        frame = root_frame
        for processor in self.processors:
            frame = processor(frame, )
        return frame
    
    xǁFrameRendererǁpreprocess__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁFrameRendererǁpreprocess__mutmut_1': xǁFrameRendererǁpreprocess__mutmut_1, 
        'xǁFrameRendererǁpreprocess__mutmut_2': xǁFrameRendererǁpreprocess__mutmut_2, 
        'xǁFrameRendererǁpreprocess__mutmut_3': xǁFrameRendererǁpreprocess__mutmut_3, 
        'xǁFrameRendererǁpreprocess__mutmut_4': xǁFrameRendererǁpreprocess__mutmut_4, 
        'xǁFrameRendererǁpreprocess__mutmut_5': xǁFrameRendererǁpreprocess__mutmut_5, 
        'xǁFrameRendererǁpreprocess__mutmut_6': xǁFrameRendererǁpreprocess__mutmut_6
    }
    
    def preprocess(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁFrameRendererǁpreprocess__mutmut_orig"), object.__getattribute__(self, "xǁFrameRendererǁpreprocess__mutmut_mutants"), args, kwargs, self)
        return result 
    
    preprocess.__signature__ = _mutmut_signature(xǁFrameRendererǁpreprocess__mutmut_orig)
    xǁFrameRendererǁpreprocess__mutmut_orig.__name__ = 'xǁFrameRendererǁpreprocess'

    def render(self, session: Session) -> str:
        """
        Return a string that contains the rendered form of `frame`.
        """
        raise NotImplementedError()
