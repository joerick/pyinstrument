from __future__ import annotations

from typing import Any, List

from pyinstrument import processors
from pyinstrument.frame import Frame
from pyinstrument.session import Session

# pyright: strict


ProcessorList = List[processors.ProcessorType]


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

    def __init__(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        """
        :param show_all: Don't hide library frames - show everything that pyinstrument captures.
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
                self.processors.remove(p)
        if timeline:
            self.processors.remove(processors.aggregate_repeated_calls)

    def default_processors(self) -> ProcessorList:
        """
        Return a list of processors that this renderer uses by default.
        """
        raise NotImplementedError()

    def preprocess(self, root_frame: Frame | None) -> Frame | None:
        frame = root_frame
        for processor in self.processors:
            frame = processor(frame, options=self.processor_options)
        return frame

    def render(self, session: Session) -> str:
        """
        Return a string that contains the rendered form of `frame`.
        """
        raise NotImplementedError()
