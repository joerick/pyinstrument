from __future__ import annotations

import re
import textwrap
import time
from typing import Any, Dict, List, Tuple

import pyinstrument
from pyinstrument import processors
from pyinstrument.frame import Frame, FrameGroup
from pyinstrument.renderers.base import FrameRenderer, ProcessorList, Renderer
from pyinstrument.session import Session
from pyinstrument.typing import LiteralStr
from pyinstrument.util import truncate

# pyright: strict

FlatTimeMode = LiteralStr["self", "total"]


class ConsoleRenderer(FrameRenderer):
    """
    Produces text-based output, suitable for text files or ANSI-compatible
    consoles.
    """

    def __init__(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
        unicode: bool = False,
        color: bool = False,
        flat: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat_time: FlatTimeMode = "self",
        short_mode: bool = False,
    ) -> None:
        """
        :param unicode: Use unicode, like box-drawing characters in the output.
        :param color: Enable color support, using ANSI color sequences.
        :param flat: Display a flat profile instead of a call graph.
        :param time: How to display the duration of each frame - ``'seconds'`` or ``'percent_of_total'``
        :param flat_time: Show ``'self'`` time or ``'total'`` time (including children) in flat profile.
        :param short_mode: Display a short version of the output.
        :param show_all: See :class:`FrameRenderer`.
        :param timeline: See :class:`FrameRenderer`.
        :param processor_options: See :class:`FrameRenderer`.
        """
        super().__init__(show_all=show_all, timeline=timeline, processor_options=processor_options)
        self.unicode = unicode
        self.color = color
        self.flat = flat
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def render(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, indent=indent)
            else:
                result += self.render_frame(self.root_frame, indent=indent, child_indent=indent)

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    # pylint: disable=W1401
    def render_preamble(self, session: Session) -> str:
        if self.short_mode:
            return textwrap.dedent(
                f"""
                    pyinstrument ........................................
                    .
                    .  {session.target_description}
                    .
                """
            )

        lines = [
            r"",
            r"  _     ._   __/__   _ _  _  _ _/_  ",
            r" /_//_/// /_\ / //_// / //_'/ //    ",
            r"/   _/        {:>20}".format("v" + pyinstrument.__version__),
        ]

        lines[1] += " Recorded: {:<9}".format(
            time.strftime("%X", time.localtime(session.start_time))
        )
        lines[2] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    def should_render_frame(self, frame: Frame) -> bool:
        if frame.group and not self.should_ignore_group(frame.group):
            return self.should_render_frame_in_group(frame)
        return True

    def should_render_frame_in_group(self, frame: Frame) -> bool:
        # Only render the root frame, or frames that are significant
        assert frame.group
        return (
            frame.group.root == frame
            or frame.total_self_time > 0.2 * self.root_frame.time
            or frame in frame.group.exit_frames
        )

    def should_ignore_group(self, group: FrameGroup) -> bool:
        """
        If a group is ignored, its frames are all printed - they're not hidden.
        """
        hidden_frames = [f for f in group.frames if not self.should_render_frame_in_group(f)]
        # don't bother printing groups with one/zero hidden frames
        return len(hidden_frames) < 2

    def group_description(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def libraries_for_frames(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def render_frame(self, frame: Frame, indent: str = "", child_indent: str = "") -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if (
                frame.group
                and frame.group.root == frame
                and not self.should_ignore_group(frame.group)
            ):
                result += f"{child_indent}   {self.group_description(frame.group)}"
                for key in indents:
                    indents[key] = "      "
        else:
            result = ""
            indents = {"├": "", "│": "", "└": "", " ": ""}

        if frame.children:
            children_to_be_rendered_indices = [
                i for i, f in enumerate(frame.children) if self.should_render_frame(f)
            ]
            last_rendered_child_index = (
                children_to_be_rendered_indices[-1] if children_to_be_rendered_indices else -1
            )

            for i, child in enumerate(frame.children):
                if i < last_rendered_child_index:
                    c_indent = child_indent + indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(child, indent=c_indent, child_indent=cc_indent)

        return result

    def render_frame_flat(self, frame: Frame, indent: str) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, 0) + frame.total_self_time
                if self.flat_time == "self"
                else frame.time
            )

            frame_id_to_frame[frame.identifier] = frame

            for child in frame.children:
                walk(child)

        frame_id_to_time: Dict[str, float] = {}
        frame_id_to_frame: Dict[str, Frame] = {}

        walk(frame)

        id_time_pairs: List[Tuple[str, float]] = sorted(
            frame_id_to_time.items(), key=(lambda item: item[1]), reverse=True
        )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(frame_id_to_frame[frame_id], override_time=self_time)
            result += "\n"

        return result

    def frame_description(self, frame: Frame, *, override_time: float | None = None) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.3f}"

        value_str = f"{time_color}{time_str}{self.colors.end}"

        class_name = frame.class_name
        if class_name:
            function_name = f"{class_name}.{frame.function}"
        else:
            function_name = frame.function
        function_color = self._ansi_color_for_name(frame)
        function_str = f"{function_color}{function_name}{self.colors.end}"

        code_position_short = frame.code_position_short()
        if code_position_short:
            code_position_str = f"{self.colors.faint}{code_position_short}{self.colors.end}"
        else:
            code_position_str = ""

        return f"{value_str} {function_str}  {code_position_str}"

    def frame_proportion_of_total_time(self, time: float) -> float:
        if self.root_frame.time == 0:
            return 1
        return time / self.root_frame.time

    def _ansi_color_for_time(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def _ansi_color_for_name(self, frame: Frame) -> str:
        if frame.is_application_code:
            return self.colors.bg_dark_blue_255 + self.colors.white_255
        else:
            return ""

    def default_processors(self) -> ProcessorList:
        return [
            processors.remove_importlib,
            processors.remove_tracebackhide,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.remove_irrelevant_nodes,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_first_pyinstrument_frames_processor,
            processors.group_library_frames_processor,
        ]

    class colors_enabled:
        red = "\033[31m"
        green = "\033[32m"
        yellow = "\033[33m"
        blue = "\033[34m"
        cyan = "\033[36m"
        bright_green = "\033[92m"
        white = "\033[37m\033[97m"

        bg_dark_blue_255 = "\033[48;5;24m"
        white_255 = "\033[38;5;15m"

        bold = "\033[1m"
        faint = "\033[2m"

        end = "\033[0m"

    class colors_disabled:
        red = ""
        green = ""
        yellow = ""
        blue = ""
        cyan = ""
        bright_green = ""
        white = ""

        bg_dark_blue_255 = ""
        white_255 = ""

        bold = ""
        faint = ""

        end = ""
