from __future__ import annotations

from typing import Any, List

from pyinstrument import processors
from pyinstrument.frame import BaseFrame
from pyinstrument.session import Session

# pyright: strict


ProcessorList = List[processors.ProcessorType]


class Renderer:
    """
    Abstract base class for renderers.
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

        if show_all:
            self.processors.remove(processors.group_library_frames_processor)
        if timeline:
            self.processors.remove(processors.aggregate_repeated_calls)

    def default_processors(self) -> ProcessorList:
        """
        Return a list of processors that this renderer uses by default.
        """
        raise NotImplementedError()

    def preprocess(self, root_frame: BaseFrame | None) -> BaseFrame | None:
        frame = root_frame
        for processor in self.processors:
            frame = processor(frame, options=self.processor_options)
        return frame

    def render(self, session: Session) -> str:
        """
        Return a string that contains the rendered form of `frame`.
        """
        raise NotImplementedError()
