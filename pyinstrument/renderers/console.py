import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import pyinstrument
from pyinstrument import processors
from pyinstrument.frame import Frame
from pyinstrument.renderers.base import FrameRenderer, ProcessorList
from pyinstrument.session import Session
from pyinstrument.typing import LiteralStr
from pyinstrument.util import truncate

# pyright: strict


class ConsoleRenderer(FrameRenderer):
    """
    Produces text-based output, suitable for text files or ANSI-compatible
    consoles.
    """

    def __init__(
        self,
        unicode: bool = False,
        color: bool = False,
        flat: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        **kwargs: Any,
    ):
        """
        :param unicode: Use unicode, like box-drawing characters in the output.
        :param color: Enable color support, using ANSI color sequences.
        :param time: How to display the duration of each frame - ``'seconds'`` or ``'percent_of_total'``
        """
        super().__init__(**kwargs)

        self.unicode = unicode
        self.color = color
        self.flat = flat
        self.colors = self.colors_enabled if color else self.colors_disabled
        self.time = time

    def render(self, session: Session):
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())

        if frame is None:
            result += "No samples were recorded.\n\n"
            return result

        self.root_frame = frame

        if self.flat:
            result += self.render_frame_flat(self.root_frame)
        else:
            result += self.render_frame(self.root_frame)
        result += "\n"

        return result

    # pylint: disable=W1401
    def render_preamble(self, session: Session):
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
        lines.append("Program: %s" % session.program)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    def render_frame(self, frame: Frame, indent: str = "", child_indent: str = "") -> str:
        if not frame.group or (
            frame.group.root == frame
            or frame.total_self_time > 0.2 * self.root_frame.time
            or frame in frame.group.exit_frames
        ):
            if self.time == "percent_of_total":
                percent = self.frame_proportion_of_total_time(frame.time) * 100
                time_str = (
                    self._ansi_color_for_time(frame.time) + f"{percent:.0f}%" + self.colors.end
                )
            else:
                time_str = (
                    self._ansi_color_for_time(frame.time) + f"{frame.time:.3f}" + self.colors.end
                )

            name_color = self._ansi_color_for_name(frame)

            class_name = frame.class_name
            if class_name:
                name = f"{class_name}.{frame.function}"
            else:
                name = frame.function

            result = "{indent}{time_str} {name_color}{name}{c.end}  {c.faint}{code_position}{c.end}\n".format(
                indent=indent,
                time_str=time_str,
                name_color=name_color,
                name=name,
                code_position=frame.code_position_short,
                c=self.colors,
            )

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if frame.group and frame.group.root == frame:
                result += "{indent}[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
                    indent=child_indent + "   ",
                    count=len(frame.group.frames),
                    libraries=truncate(", ".join(frame.group.libraries), 40),
                    c=self.colors,
                )
                for key in indents:
                    indents[key] = "      "
        else:
            result = ""
            indents = {"├": "", "│": "", "└": "", " ": ""}

        if frame.children:
            last_child = frame.children[-1]

            for child in frame.children:
                if child is not last_child:
                    c_indent = child_indent + indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(child, indent=c_indent, child_indent=cc_indent)

        return result

    def render_frame_flat(self, frame: Frame) -> str:
        @dataclass(frozen=True, eq=True)
        class FrameDesc:
            code_position_short: Optional[str]
            function: str


        def walk(frame: Frame):
            frame_desc = FrameDesc(frame.code_position_short, frame.function)
            frame_desc_to_self_time[frame_desc] = (
                frame_desc_to_self_time.get(frame_desc, 0) + frame.total_self_time
            )
            frame_desc_to_frame[frame_desc] = frame
            frame_desc_to_ncalls[frame_desc] = frame_desc_to_ncalls.get(frame_desc, 0) + 1

            for child in frame.children:
                walk(child)

        frame_desc_to_self_time: Dict[FrameDesc, float] = {}
        frame_desc_to_frame: Dict[FrameDesc, Frame] = {}
        frame_desc_to_ncalls: Dict[FrameDesc, int] = {}

        walk(frame)

        cost_list: List[Tuple[FrameDesc, float]] = sorted(
            frame_desc_to_self_time.items(), key=(lambda item: item[1]), reverse=True
        )

        res = ""

        for frame_desc, self_time in cost_list:
            if self.time == "percent_of_total":
                val = self_time / frame.time * 100
                unit = "%"
            else:
                val = self_time
                unit = "s"

            color = self._ansi_color_for_time(self_time)

            res += "{color}{val:.3f}{unit}{c.end} {name_color}{function}{c.end}  {c.faint}{code_position}{c.end} {ncalls}\n".format(
                color=color,
                val=val,
                unit=unit,
                c=self.colors,
                name_color=self._ansi_color_for_name(frame_desc_to_frame[frame_desc]),
                function=frame_desc.function,
                code_position=frame_desc.code_position_short,
                ncalls=frame_desc_to_ncalls[frame_desc],
            )

        return res

    def frame_proportion_of_total_time(self, time: float):
        return time / self.root_frame.time

    def _ansi_color_for_time(self, time: float):
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def _ansi_color_for_name(self, frame: Frame):
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
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
            processors.remove_first_pyinstrument_frames_processor,
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
