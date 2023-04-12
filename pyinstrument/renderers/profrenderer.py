from __future__ import annotations

import marshal
from typing import Any, Callable

from pyinstrument import processors
from pyinstrument.frame import Frame
from pyinstrument.renderers.base import FrameRenderer, ProcessorList
from pyinstrument.session import Session

# pyright: strict



class ProfRenderer(FrameRenderer):
    """
    Outputs a marshaled dict, containing processed frames.
    """

    output_file_extension = "prof"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def render_frame(self, frame: Frame | None, stats: dict) -> dict:
        if frame is None:
            return {}

        key = (frame.file_path or "", frame.line_no or 0, frame.function)
        # Format is (call_time, number_calls, total_time, cumulative_time, callers)
        val = [-1, -1, frame.time, frame.total_self_time, {}]
        if frame.parent:
            p = frame.parent
            val[-1][(p.file_path or "", p.line_no or 0, p.function)] = val[:-1]
        if key in stats:
            return
        stats[key] = tuple(val)
        for child in frame.children:
            if not frame.is_synthetic:
                self.render_frame(child, stats)
        return stats

    def render(self, session: Session):
        frame = self.preprocess(session.root_frame())


        stats = {}
        self.render_frame(frame, stats)

        return marshal.dumps(stats)

    def default_processors(self) -> ProcessorList:
        return [
            processors.remove_importlib,
            processors.remove_tracebackhide,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
            processors.remove_first_pyinstrument_frames_processor,
        ]
