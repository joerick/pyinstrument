from __future__ import annotations

import math
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


class ConsoleRenderer(FrameRenderer):
    """
    Produces text-based output, suitable for text files or ANSI-compatible
    consoles.
    """

    def xǁConsoleRendererǁ__init____mutmut_orig(
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

    def xǁConsoleRendererǁ__init____mutmut_1(
        self,
        show_all: bool = True,
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

    def xǁConsoleRendererǁ__init____mutmut_2(
        self,
        show_all: bool = False,
        timeline: bool = True,
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

    def xǁConsoleRendererǁ__init____mutmut_3(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
        unicode: bool = True,
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

    def xǁConsoleRendererǁ__init____mutmut_4(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
        unicode: bool = False,
        color: bool = True,
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

    def xǁConsoleRendererǁ__init____mutmut_5(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
        unicode: bool = False,
        color: bool = False,
        flat: bool = True,
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

    def xǁConsoleRendererǁ__init____mutmut_6(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
        unicode: bool = False,
        color: bool = False,
        flat: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "XXsecondsXX",
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

    def xǁConsoleRendererǁ__init____mutmut_7(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
        unicode: bool = False,
        color: bool = False,
        flat: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "SECONDS",
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

    def xǁConsoleRendererǁ__init____mutmut_8(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
        unicode: bool = False,
        color: bool = False,
        flat: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat_time: FlatTimeMode = "XXselfXX",
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

    def xǁConsoleRendererǁ__init____mutmut_9(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
        unicode: bool = False,
        color: bool = False,
        flat: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat_time: FlatTimeMode = "SELF",
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

    def xǁConsoleRendererǁ__init____mutmut_10(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
        unicode: bool = False,
        color: bool = False,
        flat: bool = False,
        time: LiteralStr["seconds", "percent_of_total"] = "seconds",
        flat_time: FlatTimeMode = "self",
        short_mode: bool = True,
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

    def xǁConsoleRendererǁ__init____mutmut_11(
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
        super().__init__(show_all=None, timeline=timeline, processor_options=processor_options)
        self.unicode = unicode
        self.color = color
        self.flat = flat
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_12(
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
        super().__init__(show_all=show_all, timeline=None, processor_options=processor_options)
        self.unicode = unicode
        self.color = color
        self.flat = flat
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_13(
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
        super().__init__(show_all=show_all, timeline=timeline, processor_options=None)
        self.unicode = unicode
        self.color = color
        self.flat = flat
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_14(
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
        super().__init__(timeline=timeline, processor_options=processor_options)
        self.unicode = unicode
        self.color = color
        self.flat = flat
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_15(
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
        super().__init__(show_all=show_all, processor_options=processor_options)
        self.unicode = unicode
        self.color = color
        self.flat = flat
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_16(
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
        super().__init__(show_all=show_all, timeline=timeline, )
        self.unicode = unicode
        self.color = color
        self.flat = flat
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_17(
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
        self.unicode = None
        self.color = color
        self.flat = flat
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_18(
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
        self.color = None
        self.flat = flat
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_19(
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
        self.flat = None
        self.time = time
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_20(
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
        self.time = None
        self.flat_time = flat_time
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_21(
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
        self.flat_time = None
        self.short_mode = short_mode

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_22(
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
        self.short_mode = None

        if self.flat and self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_23(
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

        if self.flat or self.timeline:
            raise Renderer.MisconfigurationError("Cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_24(
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
            raise Renderer.MisconfigurationError(None)

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_25(
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
            raise Renderer.MisconfigurationError("XXCannot use timeline and flat options together.XX")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_26(
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
            raise Renderer.MisconfigurationError("cannot use timeline and flat options together.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_27(
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
            raise Renderer.MisconfigurationError("CANNOT USE TIMELINE AND FLAT OPTIONS TOGETHER.")

        self.colors = self.colors_enabled if color else self.colors_disabled

    def xǁConsoleRendererǁ__init____mutmut_28(
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

        self.colors = None
    
    xǁConsoleRendererǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁ__init____mutmut_1': xǁConsoleRendererǁ__init____mutmut_1, 
        'xǁConsoleRendererǁ__init____mutmut_2': xǁConsoleRendererǁ__init____mutmut_2, 
        'xǁConsoleRendererǁ__init____mutmut_3': xǁConsoleRendererǁ__init____mutmut_3, 
        'xǁConsoleRendererǁ__init____mutmut_4': xǁConsoleRendererǁ__init____mutmut_4, 
        'xǁConsoleRendererǁ__init____mutmut_5': xǁConsoleRendererǁ__init____mutmut_5, 
        'xǁConsoleRendererǁ__init____mutmut_6': xǁConsoleRendererǁ__init____mutmut_6, 
        'xǁConsoleRendererǁ__init____mutmut_7': xǁConsoleRendererǁ__init____mutmut_7, 
        'xǁConsoleRendererǁ__init____mutmut_8': xǁConsoleRendererǁ__init____mutmut_8, 
        'xǁConsoleRendererǁ__init____mutmut_9': xǁConsoleRendererǁ__init____mutmut_9, 
        'xǁConsoleRendererǁ__init____mutmut_10': xǁConsoleRendererǁ__init____mutmut_10, 
        'xǁConsoleRendererǁ__init____mutmut_11': xǁConsoleRendererǁ__init____mutmut_11, 
        'xǁConsoleRendererǁ__init____mutmut_12': xǁConsoleRendererǁ__init____mutmut_12, 
        'xǁConsoleRendererǁ__init____mutmut_13': xǁConsoleRendererǁ__init____mutmut_13, 
        'xǁConsoleRendererǁ__init____mutmut_14': xǁConsoleRendererǁ__init____mutmut_14, 
        'xǁConsoleRendererǁ__init____mutmut_15': xǁConsoleRendererǁ__init____mutmut_15, 
        'xǁConsoleRendererǁ__init____mutmut_16': xǁConsoleRendererǁ__init____mutmut_16, 
        'xǁConsoleRendererǁ__init____mutmut_17': xǁConsoleRendererǁ__init____mutmut_17, 
        'xǁConsoleRendererǁ__init____mutmut_18': xǁConsoleRendererǁ__init____mutmut_18, 
        'xǁConsoleRendererǁ__init____mutmut_19': xǁConsoleRendererǁ__init____mutmut_19, 
        'xǁConsoleRendererǁ__init____mutmut_20': xǁConsoleRendererǁ__init____mutmut_20, 
        'xǁConsoleRendererǁ__init____mutmut_21': xǁConsoleRendererǁ__init____mutmut_21, 
        'xǁConsoleRendererǁ__init____mutmut_22': xǁConsoleRendererǁ__init____mutmut_22, 
        'xǁConsoleRendererǁ__init____mutmut_23': xǁConsoleRendererǁ__init____mutmut_23, 
        'xǁConsoleRendererǁ__init____mutmut_24': xǁConsoleRendererǁ__init____mutmut_24, 
        'xǁConsoleRendererǁ__init____mutmut_25': xǁConsoleRendererǁ__init____mutmut_25, 
        'xǁConsoleRendererǁ__init____mutmut_26': xǁConsoleRendererǁ__init____mutmut_26, 
        'xǁConsoleRendererǁ__init____mutmut_27': xǁConsoleRendererǁ__init____mutmut_27, 
        'xǁConsoleRendererǁ__init____mutmut_28': xǁConsoleRendererǁ__init____mutmut_28
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁConsoleRendererǁ__init____mutmut_orig)
    xǁConsoleRendererǁ__init____mutmut_orig.__name__ = 'xǁConsoleRendererǁ__init__'

    def xǁConsoleRendererǁrender__mutmut_orig(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_1(self, session: Session) -> str:
        result = None

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_2(self, session: Session) -> str:
        result = self.render_preamble(None)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_3(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = None
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_4(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(None)
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_5(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = None
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_6(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = "XX.  XX" if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_7(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else "XXXX"
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_8(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = None

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_9(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(None)

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_10(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(+math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_11(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(None))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_12(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(None, 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_13(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), None)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_14(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_15(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), )))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_16(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(None, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_17(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, None), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_18(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_19(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, ), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_20(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1.000000001, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_21(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 2)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_22(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is not None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_23(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result = f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_24(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result -= f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_25(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = None

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_26(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result = self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_27(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result -= self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_28(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(None, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_29(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=None)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_30(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_31(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, )
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_32(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result = self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_33(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result -= self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_34(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    None, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_35(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=None, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_36(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=None, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_37(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=None
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_38(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_39(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_40(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_41(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_42(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result = f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_43(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result -= f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_44(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result = "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_45(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result -= "." * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_46(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 - "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_47(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." / 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_48(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "XX.XX" * 53 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_49(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 54 + "\n\n"

        return result

    def xǁConsoleRendererǁrender__mutmut_50(self, session: Session) -> str:
        result = self.render_preamble(session)

        frame = self.preprocess(session.root_frame())
        indent = ".  " if self.short_mode else ""
        precision = math.ceil(-math.log10(min(max(1e-9, session.max_interval), 1)))

        if frame is None:
            result += f"{indent}No samples were recorded.\n"
        else:
            self.root_frame = frame

            if self.flat:
                result += self.render_frame_flat(self.root_frame, precision=precision)
            else:
                result += self.render_frame(
                    self.root_frame, precision=precision, indent=indent, child_indent=indent
                )

        result += f"{indent}\n"

        if self.short_mode:
            result += "." * 53 + "XX\n\nXX"

        return result
    
    xǁConsoleRendererǁrender__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁrender__mutmut_1': xǁConsoleRendererǁrender__mutmut_1, 
        'xǁConsoleRendererǁrender__mutmut_2': xǁConsoleRendererǁrender__mutmut_2, 
        'xǁConsoleRendererǁrender__mutmut_3': xǁConsoleRendererǁrender__mutmut_3, 
        'xǁConsoleRendererǁrender__mutmut_4': xǁConsoleRendererǁrender__mutmut_4, 
        'xǁConsoleRendererǁrender__mutmut_5': xǁConsoleRendererǁrender__mutmut_5, 
        'xǁConsoleRendererǁrender__mutmut_6': xǁConsoleRendererǁrender__mutmut_6, 
        'xǁConsoleRendererǁrender__mutmut_7': xǁConsoleRendererǁrender__mutmut_7, 
        'xǁConsoleRendererǁrender__mutmut_8': xǁConsoleRendererǁrender__mutmut_8, 
        'xǁConsoleRendererǁrender__mutmut_9': xǁConsoleRendererǁrender__mutmut_9, 
        'xǁConsoleRendererǁrender__mutmut_10': xǁConsoleRendererǁrender__mutmut_10, 
        'xǁConsoleRendererǁrender__mutmut_11': xǁConsoleRendererǁrender__mutmut_11, 
        'xǁConsoleRendererǁrender__mutmut_12': xǁConsoleRendererǁrender__mutmut_12, 
        'xǁConsoleRendererǁrender__mutmut_13': xǁConsoleRendererǁrender__mutmut_13, 
        'xǁConsoleRendererǁrender__mutmut_14': xǁConsoleRendererǁrender__mutmut_14, 
        'xǁConsoleRendererǁrender__mutmut_15': xǁConsoleRendererǁrender__mutmut_15, 
        'xǁConsoleRendererǁrender__mutmut_16': xǁConsoleRendererǁrender__mutmut_16, 
        'xǁConsoleRendererǁrender__mutmut_17': xǁConsoleRendererǁrender__mutmut_17, 
        'xǁConsoleRendererǁrender__mutmut_18': xǁConsoleRendererǁrender__mutmut_18, 
        'xǁConsoleRendererǁrender__mutmut_19': xǁConsoleRendererǁrender__mutmut_19, 
        'xǁConsoleRendererǁrender__mutmut_20': xǁConsoleRendererǁrender__mutmut_20, 
        'xǁConsoleRendererǁrender__mutmut_21': xǁConsoleRendererǁrender__mutmut_21, 
        'xǁConsoleRendererǁrender__mutmut_22': xǁConsoleRendererǁrender__mutmut_22, 
        'xǁConsoleRendererǁrender__mutmut_23': xǁConsoleRendererǁrender__mutmut_23, 
        'xǁConsoleRendererǁrender__mutmut_24': xǁConsoleRendererǁrender__mutmut_24, 
        'xǁConsoleRendererǁrender__mutmut_25': xǁConsoleRendererǁrender__mutmut_25, 
        'xǁConsoleRendererǁrender__mutmut_26': xǁConsoleRendererǁrender__mutmut_26, 
        'xǁConsoleRendererǁrender__mutmut_27': xǁConsoleRendererǁrender__mutmut_27, 
        'xǁConsoleRendererǁrender__mutmut_28': xǁConsoleRendererǁrender__mutmut_28, 
        'xǁConsoleRendererǁrender__mutmut_29': xǁConsoleRendererǁrender__mutmut_29, 
        'xǁConsoleRendererǁrender__mutmut_30': xǁConsoleRendererǁrender__mutmut_30, 
        'xǁConsoleRendererǁrender__mutmut_31': xǁConsoleRendererǁrender__mutmut_31, 
        'xǁConsoleRendererǁrender__mutmut_32': xǁConsoleRendererǁrender__mutmut_32, 
        'xǁConsoleRendererǁrender__mutmut_33': xǁConsoleRendererǁrender__mutmut_33, 
        'xǁConsoleRendererǁrender__mutmut_34': xǁConsoleRendererǁrender__mutmut_34, 
        'xǁConsoleRendererǁrender__mutmut_35': xǁConsoleRendererǁrender__mutmut_35, 
        'xǁConsoleRendererǁrender__mutmut_36': xǁConsoleRendererǁrender__mutmut_36, 
        'xǁConsoleRendererǁrender__mutmut_37': xǁConsoleRendererǁrender__mutmut_37, 
        'xǁConsoleRendererǁrender__mutmut_38': xǁConsoleRendererǁrender__mutmut_38, 
        'xǁConsoleRendererǁrender__mutmut_39': xǁConsoleRendererǁrender__mutmut_39, 
        'xǁConsoleRendererǁrender__mutmut_40': xǁConsoleRendererǁrender__mutmut_40, 
        'xǁConsoleRendererǁrender__mutmut_41': xǁConsoleRendererǁrender__mutmut_41, 
        'xǁConsoleRendererǁrender__mutmut_42': xǁConsoleRendererǁrender__mutmut_42, 
        'xǁConsoleRendererǁrender__mutmut_43': xǁConsoleRendererǁrender__mutmut_43, 
        'xǁConsoleRendererǁrender__mutmut_44': xǁConsoleRendererǁrender__mutmut_44, 
        'xǁConsoleRendererǁrender__mutmut_45': xǁConsoleRendererǁrender__mutmut_45, 
        'xǁConsoleRendererǁrender__mutmut_46': xǁConsoleRendererǁrender__mutmut_46, 
        'xǁConsoleRendererǁrender__mutmut_47': xǁConsoleRendererǁrender__mutmut_47, 
        'xǁConsoleRendererǁrender__mutmut_48': xǁConsoleRendererǁrender__mutmut_48, 
        'xǁConsoleRendererǁrender__mutmut_49': xǁConsoleRendererǁrender__mutmut_49, 
        'xǁConsoleRendererǁrender__mutmut_50': xǁConsoleRendererǁrender__mutmut_50
    }
    
    def render(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁrender__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁrender__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render.__signature__ = _mutmut_signature(xǁConsoleRendererǁrender__mutmut_orig)
    xǁConsoleRendererǁrender__mutmut_orig.__name__ = 'xǁConsoleRendererǁrender'

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_orig(self, session: Session) -> str:
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_1(self, session: Session) -> str:
        if self.short_mode:
            return textwrap.dedent(
                None
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_2(self, session: Session) -> str:
        if self.short_mode:
            return textwrap.dedent(
                f"""
                    pyinstrument ........................................
                    .
                    .  {session.target_description}
                    .
                """
            )

        lines = None

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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_3(self, session: Session) -> str:
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
            r"XXXX",
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_4(self, session: Session) -> str:
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_5(self, session: Session) -> str:
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_6(self, session: Session) -> str:
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
            r"XX  _     ._   __/__   _ _  _  _ _/_  XX",
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_7(self, session: Session) -> str:
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_8(self, session: Session) -> str:
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_9(self, session: Session) -> str:
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
            r"XX /_//_/// /_\ / //_// / //_'/ //    XX",
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_10(self, session: Session) -> str:
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_11(self, session: Session) -> str:
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_12(self, session: Session) -> str:
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
            r"/   _/        {:>20}".format(None),
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_13(self, session: Session) -> str:
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
            r"XX/   _/        {:>20}XX".format("v" + pyinstrument.__version__),
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_14(self, session: Session) -> str:
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_15(self, session: Session) -> str:
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_16(self, session: Session) -> str:
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
            r"/   _/        {:>20}".format("v" - pyinstrument.__version__),
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_17(self, session: Session) -> str:
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
            r"/   _/        {:>20}".format("XXvXX" + pyinstrument.__version__),
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_18(self, session: Session) -> str:
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
            r"/   _/        {:>20}".format("V" + pyinstrument.__version__),
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_19(self, session: Session) -> str:
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

        lines[1] = " Recorded: {:<9}".format(
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_20(self, session: Session) -> str:
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

        lines[1] -= " Recorded: {:<9}".format(
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_21(self, session: Session) -> str:
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

        lines[2] += " Recorded: {:<9}".format(
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_22(self, session: Session) -> str:
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
            None
        )
        lines[2] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_23(self, session: Session) -> str:
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

        lines[1] += "XX Recorded: {:<9}XX".format(
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_24(self, session: Session) -> str:
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

        lines[1] += " recorded: {:<9}".format(
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_25(self, session: Session) -> str:
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

        lines[1] += " RECORDED: {:<9}".format(
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

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_26(self, session: Session) -> str:
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
            time.strftime(None, time.localtime(session.start_time))
        )
        lines[2] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_27(self, session: Session) -> str:
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
            time.strftime("%X", None)
        )
        lines[2] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_28(self, session: Session) -> str:
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
            time.strftime(time.localtime(session.start_time))
        )
        lines[2] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_29(self, session: Session) -> str:
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
            time.strftime("%X", )
        )
        lines[2] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_30(self, session: Session) -> str:
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
            time.strftime("XX%XXX", time.localtime(session.start_time))
        )
        lines[2] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_31(self, session: Session) -> str:
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
            time.strftime("%x", time.localtime(session.start_time))
        )
        lines[2] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_32(self, session: Session) -> str:
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
            time.strftime("%X", time.localtime(None))
        )
        lines[2] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_33(self, session: Session) -> str:
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
        lines[2] = f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_34(self, session: Session) -> str:
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
        lines[2] -= f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_35(self, session: Session) -> str:
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
        lines[3] += f" Duration: {session.duration:<9.3f}"
        lines[1] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_36(self, session: Session) -> str:
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
        lines[1] = f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_37(self, session: Session) -> str:
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
        lines[1] -= f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_38(self, session: Session) -> str:
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
        lines[2] += f" Samples:  {session.sample_count}"
        lines[2] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_39(self, session: Session) -> str:
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
        lines[2] = f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_40(self, session: Session) -> str:
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
        lines[2] -= f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_41(self, session: Session) -> str:
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
        lines[3] += f" CPU time: {session.cpu_time:.3f}"

        lines.append("")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_42(self, session: Session) -> str:
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

        lines.append(None)
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_43(self, session: Session) -> str:
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

        lines.append("XXXX")
        lines.append(session.target_description)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_44(self, session: Session) -> str:
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
        lines.append(None)
        lines.append("")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_45(self, session: Session) -> str:
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
        lines.append(None)
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_46(self, session: Session) -> str:
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
        lines.append("XXXX")
        lines.append("")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_47(self, session: Session) -> str:
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
        lines.append(None)

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_48(self, session: Session) -> str:
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
        lines.append("XXXX")

        return "\n".join(lines)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_49(self, session: Session) -> str:
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

        return "\n".join(None)

    # pylint: disable=W1401
    def xǁConsoleRendererǁrender_preamble__mutmut_50(self, session: Session) -> str:
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

        return "XX\nXX".join(lines)
    
    xǁConsoleRendererǁrender_preamble__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁrender_preamble__mutmut_1': xǁConsoleRendererǁrender_preamble__mutmut_1, 
        'xǁConsoleRendererǁrender_preamble__mutmut_2': xǁConsoleRendererǁrender_preamble__mutmut_2, 
        'xǁConsoleRendererǁrender_preamble__mutmut_3': xǁConsoleRendererǁrender_preamble__mutmut_3, 
        'xǁConsoleRendererǁrender_preamble__mutmut_4': xǁConsoleRendererǁrender_preamble__mutmut_4, 
        'xǁConsoleRendererǁrender_preamble__mutmut_5': xǁConsoleRendererǁrender_preamble__mutmut_5, 
        'xǁConsoleRendererǁrender_preamble__mutmut_6': xǁConsoleRendererǁrender_preamble__mutmut_6, 
        'xǁConsoleRendererǁrender_preamble__mutmut_7': xǁConsoleRendererǁrender_preamble__mutmut_7, 
        'xǁConsoleRendererǁrender_preamble__mutmut_8': xǁConsoleRendererǁrender_preamble__mutmut_8, 
        'xǁConsoleRendererǁrender_preamble__mutmut_9': xǁConsoleRendererǁrender_preamble__mutmut_9, 
        'xǁConsoleRendererǁrender_preamble__mutmut_10': xǁConsoleRendererǁrender_preamble__mutmut_10, 
        'xǁConsoleRendererǁrender_preamble__mutmut_11': xǁConsoleRendererǁrender_preamble__mutmut_11, 
        'xǁConsoleRendererǁrender_preamble__mutmut_12': xǁConsoleRendererǁrender_preamble__mutmut_12, 
        'xǁConsoleRendererǁrender_preamble__mutmut_13': xǁConsoleRendererǁrender_preamble__mutmut_13, 
        'xǁConsoleRendererǁrender_preamble__mutmut_14': xǁConsoleRendererǁrender_preamble__mutmut_14, 
        'xǁConsoleRendererǁrender_preamble__mutmut_15': xǁConsoleRendererǁrender_preamble__mutmut_15, 
        'xǁConsoleRendererǁrender_preamble__mutmut_16': xǁConsoleRendererǁrender_preamble__mutmut_16, 
        'xǁConsoleRendererǁrender_preamble__mutmut_17': xǁConsoleRendererǁrender_preamble__mutmut_17, 
        'xǁConsoleRendererǁrender_preamble__mutmut_18': xǁConsoleRendererǁrender_preamble__mutmut_18, 
        'xǁConsoleRendererǁrender_preamble__mutmut_19': xǁConsoleRendererǁrender_preamble__mutmut_19, 
        'xǁConsoleRendererǁrender_preamble__mutmut_20': xǁConsoleRendererǁrender_preamble__mutmut_20, 
        'xǁConsoleRendererǁrender_preamble__mutmut_21': xǁConsoleRendererǁrender_preamble__mutmut_21, 
        'xǁConsoleRendererǁrender_preamble__mutmut_22': xǁConsoleRendererǁrender_preamble__mutmut_22, 
        'xǁConsoleRendererǁrender_preamble__mutmut_23': xǁConsoleRendererǁrender_preamble__mutmut_23, 
        'xǁConsoleRendererǁrender_preamble__mutmut_24': xǁConsoleRendererǁrender_preamble__mutmut_24, 
        'xǁConsoleRendererǁrender_preamble__mutmut_25': xǁConsoleRendererǁrender_preamble__mutmut_25, 
        'xǁConsoleRendererǁrender_preamble__mutmut_26': xǁConsoleRendererǁrender_preamble__mutmut_26, 
        'xǁConsoleRendererǁrender_preamble__mutmut_27': xǁConsoleRendererǁrender_preamble__mutmut_27, 
        'xǁConsoleRendererǁrender_preamble__mutmut_28': xǁConsoleRendererǁrender_preamble__mutmut_28, 
        'xǁConsoleRendererǁrender_preamble__mutmut_29': xǁConsoleRendererǁrender_preamble__mutmut_29, 
        'xǁConsoleRendererǁrender_preamble__mutmut_30': xǁConsoleRendererǁrender_preamble__mutmut_30, 
        'xǁConsoleRendererǁrender_preamble__mutmut_31': xǁConsoleRendererǁrender_preamble__mutmut_31, 
        'xǁConsoleRendererǁrender_preamble__mutmut_32': xǁConsoleRendererǁrender_preamble__mutmut_32, 
        'xǁConsoleRendererǁrender_preamble__mutmut_33': xǁConsoleRendererǁrender_preamble__mutmut_33, 
        'xǁConsoleRendererǁrender_preamble__mutmut_34': xǁConsoleRendererǁrender_preamble__mutmut_34, 
        'xǁConsoleRendererǁrender_preamble__mutmut_35': xǁConsoleRendererǁrender_preamble__mutmut_35, 
        'xǁConsoleRendererǁrender_preamble__mutmut_36': xǁConsoleRendererǁrender_preamble__mutmut_36, 
        'xǁConsoleRendererǁrender_preamble__mutmut_37': xǁConsoleRendererǁrender_preamble__mutmut_37, 
        'xǁConsoleRendererǁrender_preamble__mutmut_38': xǁConsoleRendererǁrender_preamble__mutmut_38, 
        'xǁConsoleRendererǁrender_preamble__mutmut_39': xǁConsoleRendererǁrender_preamble__mutmut_39, 
        'xǁConsoleRendererǁrender_preamble__mutmut_40': xǁConsoleRendererǁrender_preamble__mutmut_40, 
        'xǁConsoleRendererǁrender_preamble__mutmut_41': xǁConsoleRendererǁrender_preamble__mutmut_41, 
        'xǁConsoleRendererǁrender_preamble__mutmut_42': xǁConsoleRendererǁrender_preamble__mutmut_42, 
        'xǁConsoleRendererǁrender_preamble__mutmut_43': xǁConsoleRendererǁrender_preamble__mutmut_43, 
        'xǁConsoleRendererǁrender_preamble__mutmut_44': xǁConsoleRendererǁrender_preamble__mutmut_44, 
        'xǁConsoleRendererǁrender_preamble__mutmut_45': xǁConsoleRendererǁrender_preamble__mutmut_45, 
        'xǁConsoleRendererǁrender_preamble__mutmut_46': xǁConsoleRendererǁrender_preamble__mutmut_46, 
        'xǁConsoleRendererǁrender_preamble__mutmut_47': xǁConsoleRendererǁrender_preamble__mutmut_47, 
        'xǁConsoleRendererǁrender_preamble__mutmut_48': xǁConsoleRendererǁrender_preamble__mutmut_48, 
        'xǁConsoleRendererǁrender_preamble__mutmut_49': xǁConsoleRendererǁrender_preamble__mutmut_49, 
        'xǁConsoleRendererǁrender_preamble__mutmut_50': xǁConsoleRendererǁrender_preamble__mutmut_50
    }
    
    def render_preamble(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁrender_preamble__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁrender_preamble__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render_preamble.__signature__ = _mutmut_signature(xǁConsoleRendererǁrender_preamble__mutmut_orig)
    xǁConsoleRendererǁrender_preamble__mutmut_orig.__name__ = 'xǁConsoleRendererǁrender_preamble'

    def xǁConsoleRendererǁshould_render_frame__mutmut_orig(self, frame: Frame) -> bool:
        if frame.group and not self.should_ignore_group(frame.group):
            return self.should_render_frame_in_group(frame)
        return True

    def xǁConsoleRendererǁshould_render_frame__mutmut_1(self, frame: Frame) -> bool:
        if frame.group or not self.should_ignore_group(frame.group):
            return self.should_render_frame_in_group(frame)
        return True

    def xǁConsoleRendererǁshould_render_frame__mutmut_2(self, frame: Frame) -> bool:
        if frame.group and self.should_ignore_group(frame.group):
            return self.should_render_frame_in_group(frame)
        return True

    def xǁConsoleRendererǁshould_render_frame__mutmut_3(self, frame: Frame) -> bool:
        if frame.group and not self.should_ignore_group(None):
            return self.should_render_frame_in_group(frame)
        return True

    def xǁConsoleRendererǁshould_render_frame__mutmut_4(self, frame: Frame) -> bool:
        if frame.group and not self.should_ignore_group(frame.group):
            return self.should_render_frame_in_group(None)
        return True

    def xǁConsoleRendererǁshould_render_frame__mutmut_5(self, frame: Frame) -> bool:
        if frame.group and not self.should_ignore_group(frame.group):
            return self.should_render_frame_in_group(frame)
        return False
    
    xǁConsoleRendererǁshould_render_frame__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁshould_render_frame__mutmut_1': xǁConsoleRendererǁshould_render_frame__mutmut_1, 
        'xǁConsoleRendererǁshould_render_frame__mutmut_2': xǁConsoleRendererǁshould_render_frame__mutmut_2, 
        'xǁConsoleRendererǁshould_render_frame__mutmut_3': xǁConsoleRendererǁshould_render_frame__mutmut_3, 
        'xǁConsoleRendererǁshould_render_frame__mutmut_4': xǁConsoleRendererǁshould_render_frame__mutmut_4, 
        'xǁConsoleRendererǁshould_render_frame__mutmut_5': xǁConsoleRendererǁshould_render_frame__mutmut_5
    }
    
    def should_render_frame(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁshould_render_frame__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁshould_render_frame__mutmut_mutants"), args, kwargs, self)
        return result 
    
    should_render_frame.__signature__ = _mutmut_signature(xǁConsoleRendererǁshould_render_frame__mutmut_orig)
    xǁConsoleRendererǁshould_render_frame__mutmut_orig.__name__ = 'xǁConsoleRendererǁshould_render_frame'

    def xǁConsoleRendererǁshould_render_frame_in_group__mutmut_orig(self, frame: Frame) -> bool:
        # Only render the root frame, or frames that are significant
        assert frame.group
        return (
            frame.group.root == frame
            or frame.total_self_time > 0.2 * self.root_frame.time
            or frame in frame.group.exit_frames
        )

    def xǁConsoleRendererǁshould_render_frame_in_group__mutmut_1(self, frame: Frame) -> bool:
        # Only render the root frame, or frames that are significant
        assert frame.group
        return (
            frame.group.root == frame
            or frame.total_self_time > 0.2 * self.root_frame.time and frame in frame.group.exit_frames
        )

    def xǁConsoleRendererǁshould_render_frame_in_group__mutmut_2(self, frame: Frame) -> bool:
        # Only render the root frame, or frames that are significant
        assert frame.group
        return (
            frame.group.root == frame and frame.total_self_time > 0.2 * self.root_frame.time
            or frame in frame.group.exit_frames
        )

    def xǁConsoleRendererǁshould_render_frame_in_group__mutmut_3(self, frame: Frame) -> bool:
        # Only render the root frame, or frames that are significant
        assert frame.group
        return (
            frame.group.root != frame
            or frame.total_self_time > 0.2 * self.root_frame.time
            or frame in frame.group.exit_frames
        )

    def xǁConsoleRendererǁshould_render_frame_in_group__mutmut_4(self, frame: Frame) -> bool:
        # Only render the root frame, or frames that are significant
        assert frame.group
        return (
            frame.group.root == frame
            or frame.total_self_time >= 0.2 * self.root_frame.time
            or frame in frame.group.exit_frames
        )

    def xǁConsoleRendererǁshould_render_frame_in_group__mutmut_5(self, frame: Frame) -> bool:
        # Only render the root frame, or frames that are significant
        assert frame.group
        return (
            frame.group.root == frame
            or frame.total_self_time > 0.2 / self.root_frame.time
            or frame in frame.group.exit_frames
        )

    def xǁConsoleRendererǁshould_render_frame_in_group__mutmut_6(self, frame: Frame) -> bool:
        # Only render the root frame, or frames that are significant
        assert frame.group
        return (
            frame.group.root == frame
            or frame.total_self_time > 1.2 * self.root_frame.time
            or frame in frame.group.exit_frames
        )

    def xǁConsoleRendererǁshould_render_frame_in_group__mutmut_7(self, frame: Frame) -> bool:
        # Only render the root frame, or frames that are significant
        assert frame.group
        return (
            frame.group.root == frame
            or frame.total_self_time > 0.2 * self.root_frame.time
            or frame not in frame.group.exit_frames
        )
    
    xǁConsoleRendererǁshould_render_frame_in_group__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁshould_render_frame_in_group__mutmut_1': xǁConsoleRendererǁshould_render_frame_in_group__mutmut_1, 
        'xǁConsoleRendererǁshould_render_frame_in_group__mutmut_2': xǁConsoleRendererǁshould_render_frame_in_group__mutmut_2, 
        'xǁConsoleRendererǁshould_render_frame_in_group__mutmut_3': xǁConsoleRendererǁshould_render_frame_in_group__mutmut_3, 
        'xǁConsoleRendererǁshould_render_frame_in_group__mutmut_4': xǁConsoleRendererǁshould_render_frame_in_group__mutmut_4, 
        'xǁConsoleRendererǁshould_render_frame_in_group__mutmut_5': xǁConsoleRendererǁshould_render_frame_in_group__mutmut_5, 
        'xǁConsoleRendererǁshould_render_frame_in_group__mutmut_6': xǁConsoleRendererǁshould_render_frame_in_group__mutmut_6, 
        'xǁConsoleRendererǁshould_render_frame_in_group__mutmut_7': xǁConsoleRendererǁshould_render_frame_in_group__mutmut_7
    }
    
    def should_render_frame_in_group(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁshould_render_frame_in_group__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁshould_render_frame_in_group__mutmut_mutants"), args, kwargs, self)
        return result 
    
    should_render_frame_in_group.__signature__ = _mutmut_signature(xǁConsoleRendererǁshould_render_frame_in_group__mutmut_orig)
    xǁConsoleRendererǁshould_render_frame_in_group__mutmut_orig.__name__ = 'xǁConsoleRendererǁshould_render_frame_in_group'

    def xǁConsoleRendererǁshould_ignore_group__mutmut_orig(self, group: FrameGroup) -> bool:
        """
        If a group is ignored, its frames are all printed - they're not hidden.
        """
        hidden_frames = [f for f in group.frames if not self.should_render_frame_in_group(f)]
        # don't bother printing groups with one/zero hidden frames
        return len(hidden_frames) < 2

    def xǁConsoleRendererǁshould_ignore_group__mutmut_1(self, group: FrameGroup) -> bool:
        """
        If a group is ignored, its frames are all printed - they're not hidden.
        """
        hidden_frames = None
        # don't bother printing groups with one/zero hidden frames
        return len(hidden_frames) < 2

    def xǁConsoleRendererǁshould_ignore_group__mutmut_2(self, group: FrameGroup) -> bool:
        """
        If a group is ignored, its frames are all printed - they're not hidden.
        """
        hidden_frames = [f for f in group.frames if self.should_render_frame_in_group(f)]
        # don't bother printing groups with one/zero hidden frames
        return len(hidden_frames) < 2

    def xǁConsoleRendererǁshould_ignore_group__mutmut_3(self, group: FrameGroup) -> bool:
        """
        If a group is ignored, its frames are all printed - they're not hidden.
        """
        hidden_frames = [f for f in group.frames if not self.should_render_frame_in_group(None)]
        # don't bother printing groups with one/zero hidden frames
        return len(hidden_frames) < 2

    def xǁConsoleRendererǁshould_ignore_group__mutmut_4(self, group: FrameGroup) -> bool:
        """
        If a group is ignored, its frames are all printed - they're not hidden.
        """
        hidden_frames = [f for f in group.frames if not self.should_render_frame_in_group(f)]
        # don't bother printing groups with one/zero hidden frames
        return len(hidden_frames) <= 2

    def xǁConsoleRendererǁshould_ignore_group__mutmut_5(self, group: FrameGroup) -> bool:
        """
        If a group is ignored, its frames are all printed - they're not hidden.
        """
        hidden_frames = [f for f in group.frames if not self.should_render_frame_in_group(f)]
        # don't bother printing groups with one/zero hidden frames
        return len(hidden_frames) < 3
    
    xǁConsoleRendererǁshould_ignore_group__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁshould_ignore_group__mutmut_1': xǁConsoleRendererǁshould_ignore_group__mutmut_1, 
        'xǁConsoleRendererǁshould_ignore_group__mutmut_2': xǁConsoleRendererǁshould_ignore_group__mutmut_2, 
        'xǁConsoleRendererǁshould_ignore_group__mutmut_3': xǁConsoleRendererǁshould_ignore_group__mutmut_3, 
        'xǁConsoleRendererǁshould_ignore_group__mutmut_4': xǁConsoleRendererǁshould_ignore_group__mutmut_4, 
        'xǁConsoleRendererǁshould_ignore_group__mutmut_5': xǁConsoleRendererǁshould_ignore_group__mutmut_5
    }
    
    def should_ignore_group(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁshould_ignore_group__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁshould_ignore_group__mutmut_mutants"), args, kwargs, self)
        return result 
    
    should_ignore_group.__signature__ = _mutmut_signature(xǁConsoleRendererǁshould_ignore_group__mutmut_orig)
    xǁConsoleRendererǁshould_ignore_group__mutmut_orig.__name__ = 'xǁConsoleRendererǁshould_ignore_group'

    def xǁConsoleRendererǁgroup_description__mutmut_orig(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_1(self, group: FrameGroup) -> str:
        hidden_frames = None
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_2(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_3(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(None)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_4(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = None
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_5(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(None)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_6(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=None,
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_7(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=None,
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_8(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=None,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_9(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_10(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_11(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            )

    def xǁConsoleRendererǁgroup_description__mutmut_12(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "XX[{count} frames hidden]  {c.faint}{libraries}{c.end}\nXX".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_13(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{COUNT} FRAMES HIDDEN]  {C.FAINT}{LIBRARIES}{C.END}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_14(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(None, 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_15(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), None),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_16(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_17(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), ),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_18(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(None), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_19(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate("XX, XX".join(libraries), 40),
            c=self.colors,
        )

    def xǁConsoleRendererǁgroup_description__mutmut_20(self, group: FrameGroup) -> str:
        hidden_frames = [f for f in group.frames if not self.should_render_frame(f)]
        libraries = self.libraries_for_frames(hidden_frames)
        return "[{count} frames hidden]  {c.faint}{libraries}{c.end}\n".format(
            count=len(hidden_frames),
            libraries=truncate(", ".join(libraries), 41),
            c=self.colors,
        )
    
    xǁConsoleRendererǁgroup_description__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁgroup_description__mutmut_1': xǁConsoleRendererǁgroup_description__mutmut_1, 
        'xǁConsoleRendererǁgroup_description__mutmut_2': xǁConsoleRendererǁgroup_description__mutmut_2, 
        'xǁConsoleRendererǁgroup_description__mutmut_3': xǁConsoleRendererǁgroup_description__mutmut_3, 
        'xǁConsoleRendererǁgroup_description__mutmut_4': xǁConsoleRendererǁgroup_description__mutmut_4, 
        'xǁConsoleRendererǁgroup_description__mutmut_5': xǁConsoleRendererǁgroup_description__mutmut_5, 
        'xǁConsoleRendererǁgroup_description__mutmut_6': xǁConsoleRendererǁgroup_description__mutmut_6, 
        'xǁConsoleRendererǁgroup_description__mutmut_7': xǁConsoleRendererǁgroup_description__mutmut_7, 
        'xǁConsoleRendererǁgroup_description__mutmut_8': xǁConsoleRendererǁgroup_description__mutmut_8, 
        'xǁConsoleRendererǁgroup_description__mutmut_9': xǁConsoleRendererǁgroup_description__mutmut_9, 
        'xǁConsoleRendererǁgroup_description__mutmut_10': xǁConsoleRendererǁgroup_description__mutmut_10, 
        'xǁConsoleRendererǁgroup_description__mutmut_11': xǁConsoleRendererǁgroup_description__mutmut_11, 
        'xǁConsoleRendererǁgroup_description__mutmut_12': xǁConsoleRendererǁgroup_description__mutmut_12, 
        'xǁConsoleRendererǁgroup_description__mutmut_13': xǁConsoleRendererǁgroup_description__mutmut_13, 
        'xǁConsoleRendererǁgroup_description__mutmut_14': xǁConsoleRendererǁgroup_description__mutmut_14, 
        'xǁConsoleRendererǁgroup_description__mutmut_15': xǁConsoleRendererǁgroup_description__mutmut_15, 
        'xǁConsoleRendererǁgroup_description__mutmut_16': xǁConsoleRendererǁgroup_description__mutmut_16, 
        'xǁConsoleRendererǁgroup_description__mutmut_17': xǁConsoleRendererǁgroup_description__mutmut_17, 
        'xǁConsoleRendererǁgroup_description__mutmut_18': xǁConsoleRendererǁgroup_description__mutmut_18, 
        'xǁConsoleRendererǁgroup_description__mutmut_19': xǁConsoleRendererǁgroup_description__mutmut_19, 
        'xǁConsoleRendererǁgroup_description__mutmut_20': xǁConsoleRendererǁgroup_description__mutmut_20
    }
    
    def group_description(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁgroup_description__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁgroup_description__mutmut_mutants"), args, kwargs, self)
        return result 
    
    group_description.__signature__ = _mutmut_signature(xǁConsoleRendererǁgroup_description__mutmut_orig)
    xǁConsoleRendererǁgroup_description__mutmut_orig.__name__ = 'xǁConsoleRendererǁgroup_description'

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_orig(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_1(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = None
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_2(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = None

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_3(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(None, frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_4(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", None, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_5(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=None)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_6(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_7(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_8(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, )[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_9(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.rsplit(r"[\\/\.]", frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_10(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"XX[\\/\.]XX", frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_11(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_12(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_13(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=2)[0]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_14(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=1)[1]

                if library and library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_15(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=1)[0]

                if library or library not in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_16(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=1)[0]

                if library and library in libraries:
                    libraries.append(library)
        return libraries

    def xǁConsoleRendererǁlibraries_for_frames__mutmut_17(self, frames: list[Frame]) -> list[str]:
        libraries: list[str] = []
        for frame in frames:
            if frame.file_path_short:
                library = re.split(r"[\\/\.]", frame.file_path_short, maxsplit=1)[0]

                if library and library not in libraries:
                    libraries.append(None)
        return libraries
    
    xǁConsoleRendererǁlibraries_for_frames__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁlibraries_for_frames__mutmut_1': xǁConsoleRendererǁlibraries_for_frames__mutmut_1, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_2': xǁConsoleRendererǁlibraries_for_frames__mutmut_2, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_3': xǁConsoleRendererǁlibraries_for_frames__mutmut_3, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_4': xǁConsoleRendererǁlibraries_for_frames__mutmut_4, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_5': xǁConsoleRendererǁlibraries_for_frames__mutmut_5, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_6': xǁConsoleRendererǁlibraries_for_frames__mutmut_6, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_7': xǁConsoleRendererǁlibraries_for_frames__mutmut_7, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_8': xǁConsoleRendererǁlibraries_for_frames__mutmut_8, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_9': xǁConsoleRendererǁlibraries_for_frames__mutmut_9, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_10': xǁConsoleRendererǁlibraries_for_frames__mutmut_10, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_11': xǁConsoleRendererǁlibraries_for_frames__mutmut_11, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_12': xǁConsoleRendererǁlibraries_for_frames__mutmut_12, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_13': xǁConsoleRendererǁlibraries_for_frames__mutmut_13, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_14': xǁConsoleRendererǁlibraries_for_frames__mutmut_14, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_15': xǁConsoleRendererǁlibraries_for_frames__mutmut_15, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_16': xǁConsoleRendererǁlibraries_for_frames__mutmut_16, 
        'xǁConsoleRendererǁlibraries_for_frames__mutmut_17': xǁConsoleRendererǁlibraries_for_frames__mutmut_17
    }
    
    def libraries_for_frames(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁlibraries_for_frames__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁlibraries_for_frames__mutmut_mutants"), args, kwargs, self)
        return result 
    
    libraries_for_frames.__signature__ = _mutmut_signature(xǁConsoleRendererǁlibraries_for_frames__mutmut_orig)
    xǁConsoleRendererǁlibraries_for_frames__mutmut_orig.__name__ = 'xǁConsoleRendererǁlibraries_for_frames'

    def xǁConsoleRendererǁrender_frame__mutmut_orig(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_1(
        self, frame: Frame, precision: int, indent: str = "XXXX", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_2(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = "XXXX"
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_3(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(None):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_4(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = None

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_5(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(None, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_6(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=None)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_7(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_8(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, )}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_9(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = None
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_10(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"XX├XX": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_11(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "XX├─ XX", "│": "│  ", "└": "└─ ", " ": "   "}
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_12(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "XX│XX": "│  ", "└": "└─ ", " ": "   "}
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_13(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "XX│  XX", "└": "└─ ", " ": "   "}
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_14(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "XX└XX": "└─ ", " ": "   "}
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_15(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "XX└─ XX", " ": "   "}
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_16(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", "XX XX": "   "}
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_17(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "XX   XX"}
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_18(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = None

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_19(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"XX├XX": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_20(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "XX|- XX", "│": "|  ", "└": "`- ", " ": "   "}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_21(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "XX│XX": "|  ", "└": "`- ", " ": "   "}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_22(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "XX|  XX", "└": "`- ", " ": "   "}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_23(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "XX└XX": "`- ", " ": "   "}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_24(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "XX`- XX", " ": "   "}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_25(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", "XX XX": "   "}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_26(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "XX   XX"}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_27(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if (
                frame.group
                and frame.group.root == frame or not self.should_ignore_group(frame.group)
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_28(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if (
                frame.group or frame.group.root == frame
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_29(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if (
                frame.group
                and frame.group.root != frame
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_30(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if (
                frame.group
                and frame.group.root == frame
                and self.should_ignore_group(frame.group)
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_31(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if (
                frame.group
                and frame.group.root == frame
                and not self.should_ignore_group(None)
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_32(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if (
                frame.group
                and frame.group.root == frame
                and not self.should_ignore_group(frame.group)
            ):
                result = f"{child_indent}   {self.group_description(frame.group)}"
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_33(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if (
                frame.group
                and frame.group.root == frame
                and not self.should_ignore_group(frame.group)
            ):
                result -= f"{child_indent}   {self.group_description(frame.group)}"
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_34(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

            if self.unicode:
                indents = {"├": "├─ ", "│": "│  ", "└": "└─ ", " ": "   "}
            else:
                indents = {"├": "|- ", "│": "|  ", "└": "`- ", " ": "   "}

            if (
                frame.group
                and frame.group.root == frame
                and not self.should_ignore_group(frame.group)
            ):
                result += f"{child_indent}   {self.group_description(None)}"
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_35(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    indents[key] = None
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_36(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    indents[key] = "XX      XX"
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_37(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            result = None
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_38(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            result = "XXXX"
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_39(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            indents = None

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_40(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            indents = {"XX├XX": "", "│": "", "└": "", " ": ""}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_41(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            indents = {"├": "XXXX", "│": "", "└": "", " ": ""}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_42(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            indents = {"├": "", "XX│XX": "", "└": "", " ": ""}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_43(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            indents = {"├": "", "│": "XXXX", "└": "", " ": ""}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_44(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            indents = {"├": "", "│": "", "XX└XX": "", " ": ""}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_45(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            indents = {"├": "", "│": "", "└": "XXXX", " ": ""}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_46(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            indents = {"├": "", "│": "", "└": "", "XX XX": ""}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_47(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            indents = {"├": "", "│": "", "└": "", " ": "XXXX"}

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_48(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            children_to_be_rendered_indices = None
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_49(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                i for i, f in enumerate(None) if self.should_render_frame(f)
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_50(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                i for i, f in enumerate(frame.children) if self.should_render_frame(None)
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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_51(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
            last_rendered_child_index = None

            for i, child in enumerate(frame.children):
                if i < last_rendered_child_index:
                    c_indent = child_indent + indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_52(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                children_to_be_rendered_indices[+1] if children_to_be_rendered_indices else -1
            )

            for i, child in enumerate(frame.children):
                if i < last_rendered_child_index:
                    c_indent = child_indent + indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_53(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                children_to_be_rendered_indices[-2] if children_to_be_rendered_indices else -1
            )

            for i, child in enumerate(frame.children):
                if i < last_rendered_child_index:
                    c_indent = child_indent + indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_54(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                children_to_be_rendered_indices[-1] if children_to_be_rendered_indices else +1
            )

            for i, child in enumerate(frame.children):
                if i < last_rendered_child_index:
                    c_indent = child_indent + indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_55(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                children_to_be_rendered_indices[-1] if children_to_be_rendered_indices else -2
            )

            for i, child in enumerate(frame.children):
                if i < last_rendered_child_index:
                    c_indent = child_indent + indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_56(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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

            for i, child in enumerate(None):
                if i < last_rendered_child_index:
                    c_indent = child_indent + indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_57(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                if i <= last_rendered_child_index:
                    c_indent = child_indent + indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_58(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    c_indent = None
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_59(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    c_indent = child_indent - indents["├"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_60(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    c_indent = child_indent + indents["XX├XX"]
                    cc_indent = child_indent + indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_61(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    cc_indent = None
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_62(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    cc_indent = child_indent - indents["│"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_63(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    cc_indent = child_indent + indents["XX│XX"]
                else:
                    c_indent = child_indent + indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_64(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    c_indent = None
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_65(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    c_indent = child_indent - indents["└"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_66(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    c_indent = child_indent + indents["XX└XX"]
                    cc_indent = child_indent + indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_67(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    cc_indent = None
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_68(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    cc_indent = child_indent - indents[" "]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_69(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                    cc_indent = child_indent + indents["XX XX"]
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_70(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result = self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_71(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result -= self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_72(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    None, precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_73(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=None, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_74(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=None, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_75(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, child_indent=None
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_76(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    precision=precision, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_77(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, indent=c_indent, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_78(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, child_indent=cc_indent
                )

        return result

    def xǁConsoleRendererǁrender_frame__mutmut_79(
        self, frame: Frame, precision: int, indent: str = "", child_indent: str = ""
    ) -> str:
        if self.should_render_frame(frame):
            result = f"{indent}{self.frame_description(frame, precision=precision)}\n"

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
                result += self.render_frame(
                    child, precision=precision, indent=c_indent, )

        return result
    
    xǁConsoleRendererǁrender_frame__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁrender_frame__mutmut_1': xǁConsoleRendererǁrender_frame__mutmut_1, 
        'xǁConsoleRendererǁrender_frame__mutmut_2': xǁConsoleRendererǁrender_frame__mutmut_2, 
        'xǁConsoleRendererǁrender_frame__mutmut_3': xǁConsoleRendererǁrender_frame__mutmut_3, 
        'xǁConsoleRendererǁrender_frame__mutmut_4': xǁConsoleRendererǁrender_frame__mutmut_4, 
        'xǁConsoleRendererǁrender_frame__mutmut_5': xǁConsoleRendererǁrender_frame__mutmut_5, 
        'xǁConsoleRendererǁrender_frame__mutmut_6': xǁConsoleRendererǁrender_frame__mutmut_6, 
        'xǁConsoleRendererǁrender_frame__mutmut_7': xǁConsoleRendererǁrender_frame__mutmut_7, 
        'xǁConsoleRendererǁrender_frame__mutmut_8': xǁConsoleRendererǁrender_frame__mutmut_8, 
        'xǁConsoleRendererǁrender_frame__mutmut_9': xǁConsoleRendererǁrender_frame__mutmut_9, 
        'xǁConsoleRendererǁrender_frame__mutmut_10': xǁConsoleRendererǁrender_frame__mutmut_10, 
        'xǁConsoleRendererǁrender_frame__mutmut_11': xǁConsoleRendererǁrender_frame__mutmut_11, 
        'xǁConsoleRendererǁrender_frame__mutmut_12': xǁConsoleRendererǁrender_frame__mutmut_12, 
        'xǁConsoleRendererǁrender_frame__mutmut_13': xǁConsoleRendererǁrender_frame__mutmut_13, 
        'xǁConsoleRendererǁrender_frame__mutmut_14': xǁConsoleRendererǁrender_frame__mutmut_14, 
        'xǁConsoleRendererǁrender_frame__mutmut_15': xǁConsoleRendererǁrender_frame__mutmut_15, 
        'xǁConsoleRendererǁrender_frame__mutmut_16': xǁConsoleRendererǁrender_frame__mutmut_16, 
        'xǁConsoleRendererǁrender_frame__mutmut_17': xǁConsoleRendererǁrender_frame__mutmut_17, 
        'xǁConsoleRendererǁrender_frame__mutmut_18': xǁConsoleRendererǁrender_frame__mutmut_18, 
        'xǁConsoleRendererǁrender_frame__mutmut_19': xǁConsoleRendererǁrender_frame__mutmut_19, 
        'xǁConsoleRendererǁrender_frame__mutmut_20': xǁConsoleRendererǁrender_frame__mutmut_20, 
        'xǁConsoleRendererǁrender_frame__mutmut_21': xǁConsoleRendererǁrender_frame__mutmut_21, 
        'xǁConsoleRendererǁrender_frame__mutmut_22': xǁConsoleRendererǁrender_frame__mutmut_22, 
        'xǁConsoleRendererǁrender_frame__mutmut_23': xǁConsoleRendererǁrender_frame__mutmut_23, 
        'xǁConsoleRendererǁrender_frame__mutmut_24': xǁConsoleRendererǁrender_frame__mutmut_24, 
        'xǁConsoleRendererǁrender_frame__mutmut_25': xǁConsoleRendererǁrender_frame__mutmut_25, 
        'xǁConsoleRendererǁrender_frame__mutmut_26': xǁConsoleRendererǁrender_frame__mutmut_26, 
        'xǁConsoleRendererǁrender_frame__mutmut_27': xǁConsoleRendererǁrender_frame__mutmut_27, 
        'xǁConsoleRendererǁrender_frame__mutmut_28': xǁConsoleRendererǁrender_frame__mutmut_28, 
        'xǁConsoleRendererǁrender_frame__mutmut_29': xǁConsoleRendererǁrender_frame__mutmut_29, 
        'xǁConsoleRendererǁrender_frame__mutmut_30': xǁConsoleRendererǁrender_frame__mutmut_30, 
        'xǁConsoleRendererǁrender_frame__mutmut_31': xǁConsoleRendererǁrender_frame__mutmut_31, 
        'xǁConsoleRendererǁrender_frame__mutmut_32': xǁConsoleRendererǁrender_frame__mutmut_32, 
        'xǁConsoleRendererǁrender_frame__mutmut_33': xǁConsoleRendererǁrender_frame__mutmut_33, 
        'xǁConsoleRendererǁrender_frame__mutmut_34': xǁConsoleRendererǁrender_frame__mutmut_34, 
        'xǁConsoleRendererǁrender_frame__mutmut_35': xǁConsoleRendererǁrender_frame__mutmut_35, 
        'xǁConsoleRendererǁrender_frame__mutmut_36': xǁConsoleRendererǁrender_frame__mutmut_36, 
        'xǁConsoleRendererǁrender_frame__mutmut_37': xǁConsoleRendererǁrender_frame__mutmut_37, 
        'xǁConsoleRendererǁrender_frame__mutmut_38': xǁConsoleRendererǁrender_frame__mutmut_38, 
        'xǁConsoleRendererǁrender_frame__mutmut_39': xǁConsoleRendererǁrender_frame__mutmut_39, 
        'xǁConsoleRendererǁrender_frame__mutmut_40': xǁConsoleRendererǁrender_frame__mutmut_40, 
        'xǁConsoleRendererǁrender_frame__mutmut_41': xǁConsoleRendererǁrender_frame__mutmut_41, 
        'xǁConsoleRendererǁrender_frame__mutmut_42': xǁConsoleRendererǁrender_frame__mutmut_42, 
        'xǁConsoleRendererǁrender_frame__mutmut_43': xǁConsoleRendererǁrender_frame__mutmut_43, 
        'xǁConsoleRendererǁrender_frame__mutmut_44': xǁConsoleRendererǁrender_frame__mutmut_44, 
        'xǁConsoleRendererǁrender_frame__mutmut_45': xǁConsoleRendererǁrender_frame__mutmut_45, 
        'xǁConsoleRendererǁrender_frame__mutmut_46': xǁConsoleRendererǁrender_frame__mutmut_46, 
        'xǁConsoleRendererǁrender_frame__mutmut_47': xǁConsoleRendererǁrender_frame__mutmut_47, 
        'xǁConsoleRendererǁrender_frame__mutmut_48': xǁConsoleRendererǁrender_frame__mutmut_48, 
        'xǁConsoleRendererǁrender_frame__mutmut_49': xǁConsoleRendererǁrender_frame__mutmut_49, 
        'xǁConsoleRendererǁrender_frame__mutmut_50': xǁConsoleRendererǁrender_frame__mutmut_50, 
        'xǁConsoleRendererǁrender_frame__mutmut_51': xǁConsoleRendererǁrender_frame__mutmut_51, 
        'xǁConsoleRendererǁrender_frame__mutmut_52': xǁConsoleRendererǁrender_frame__mutmut_52, 
        'xǁConsoleRendererǁrender_frame__mutmut_53': xǁConsoleRendererǁrender_frame__mutmut_53, 
        'xǁConsoleRendererǁrender_frame__mutmut_54': xǁConsoleRendererǁrender_frame__mutmut_54, 
        'xǁConsoleRendererǁrender_frame__mutmut_55': xǁConsoleRendererǁrender_frame__mutmut_55, 
        'xǁConsoleRendererǁrender_frame__mutmut_56': xǁConsoleRendererǁrender_frame__mutmut_56, 
        'xǁConsoleRendererǁrender_frame__mutmut_57': xǁConsoleRendererǁrender_frame__mutmut_57, 
        'xǁConsoleRendererǁrender_frame__mutmut_58': xǁConsoleRendererǁrender_frame__mutmut_58, 
        'xǁConsoleRendererǁrender_frame__mutmut_59': xǁConsoleRendererǁrender_frame__mutmut_59, 
        'xǁConsoleRendererǁrender_frame__mutmut_60': xǁConsoleRendererǁrender_frame__mutmut_60, 
        'xǁConsoleRendererǁrender_frame__mutmut_61': xǁConsoleRendererǁrender_frame__mutmut_61, 
        'xǁConsoleRendererǁrender_frame__mutmut_62': xǁConsoleRendererǁrender_frame__mutmut_62, 
        'xǁConsoleRendererǁrender_frame__mutmut_63': xǁConsoleRendererǁrender_frame__mutmut_63, 
        'xǁConsoleRendererǁrender_frame__mutmut_64': xǁConsoleRendererǁrender_frame__mutmut_64, 
        'xǁConsoleRendererǁrender_frame__mutmut_65': xǁConsoleRendererǁrender_frame__mutmut_65, 
        'xǁConsoleRendererǁrender_frame__mutmut_66': xǁConsoleRendererǁrender_frame__mutmut_66, 
        'xǁConsoleRendererǁrender_frame__mutmut_67': xǁConsoleRendererǁrender_frame__mutmut_67, 
        'xǁConsoleRendererǁrender_frame__mutmut_68': xǁConsoleRendererǁrender_frame__mutmut_68, 
        'xǁConsoleRendererǁrender_frame__mutmut_69': xǁConsoleRendererǁrender_frame__mutmut_69, 
        'xǁConsoleRendererǁrender_frame__mutmut_70': xǁConsoleRendererǁrender_frame__mutmut_70, 
        'xǁConsoleRendererǁrender_frame__mutmut_71': xǁConsoleRendererǁrender_frame__mutmut_71, 
        'xǁConsoleRendererǁrender_frame__mutmut_72': xǁConsoleRendererǁrender_frame__mutmut_72, 
        'xǁConsoleRendererǁrender_frame__mutmut_73': xǁConsoleRendererǁrender_frame__mutmut_73, 
        'xǁConsoleRendererǁrender_frame__mutmut_74': xǁConsoleRendererǁrender_frame__mutmut_74, 
        'xǁConsoleRendererǁrender_frame__mutmut_75': xǁConsoleRendererǁrender_frame__mutmut_75, 
        'xǁConsoleRendererǁrender_frame__mutmut_76': xǁConsoleRendererǁrender_frame__mutmut_76, 
        'xǁConsoleRendererǁrender_frame__mutmut_77': xǁConsoleRendererǁrender_frame__mutmut_77, 
        'xǁConsoleRendererǁrender_frame__mutmut_78': xǁConsoleRendererǁrender_frame__mutmut_78, 
        'xǁConsoleRendererǁrender_frame__mutmut_79': xǁConsoleRendererǁrender_frame__mutmut_79
    }
    
    def render_frame(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁrender_frame__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁrender_frame__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render_frame.__signature__ = _mutmut_signature(xǁConsoleRendererǁrender_frame__mutmut_orig)
    xǁConsoleRendererǁrender_frame__mutmut_orig.__name__ = 'xǁConsoleRendererǁrender_frame'

    def xǁConsoleRendererǁrender_frame_flat__mutmut_orig(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_1(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = None

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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_2(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, 0) - frame.total_self_time
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_3(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(None, 0) + frame.total_self_time
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_4(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, None) + frame.total_self_time
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_5(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(0) + frame.total_self_time
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_6(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, ) + frame.total_self_time
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_7(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, 1) + frame.total_self_time
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_8(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, 0) + frame.total_self_time
                if self.flat_time != "self"
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_9(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, 0) + frame.total_self_time
                if self.flat_time == "XXselfXX"
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_10(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, 0) + frame.total_self_time
                if self.flat_time == "SELF"
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_11(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, 0) + frame.total_self_time
                if self.flat_time == "self"
                else frame.time
            )

            frame_id_to_frame[frame.identifier] = None

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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_12(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, 0) + frame.total_self_time
                if self.flat_time == "self"
                else frame.time
            )

            frame_id_to_frame[frame.identifier] = frame

            for child in frame.children:
                walk(None)

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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_13(self, frame: Frame, precision: int) -> str:
        def walk(frame: Frame):
            frame_id_to_time[frame.identifier] = (
                frame_id_to_time.get(frame.identifier, 0) + frame.total_self_time
                if self.flat_time == "self"
                else frame.time
            )

            frame_id_to_frame[frame.identifier] = frame

            for child in frame.children:
                walk(child)

        frame_id_to_time: Dict[str, float] = None
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_14(self, frame: Frame, precision: int) -> str:
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
        frame_id_to_frame: Dict[str, Frame] = None

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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_15(self, frame: Frame, precision: int) -> str:
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

        walk(None)

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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_16(self, frame: Frame, precision: int) -> str:
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

        id_time_pairs: List[Tuple[str, float]] = None

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_17(self, frame: Frame, precision: int) -> str:
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
            None, key=(lambda item: item[1]), reverse=True
        )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_18(self, frame: Frame, precision: int) -> str:
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
            frame_id_to_time.items(), key=None, reverse=True
        )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_19(self, frame: Frame, precision: int) -> str:
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
            frame_id_to_time.items(), key=(lambda item: item[1]), reverse=None
        )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_20(self, frame: Frame, precision: int) -> str:
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
            key=(lambda item: item[1]), reverse=True
        )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_21(self, frame: Frame, precision: int) -> str:
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
            frame_id_to_time.items(), reverse=True
        )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_22(self, frame: Frame, precision: int) -> str:
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
            frame_id_to_time.items(), key=(lambda item: item[1]), )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_23(self, frame: Frame, precision: int) -> str:
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
            frame_id_to_time.items(), key=(lambda item: None), reverse=True
        )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_24(self, frame: Frame, precision: int) -> str:
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
            frame_id_to_time.items(), key=(lambda item: item[2]), reverse=True
        )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_25(self, frame: Frame, precision: int) -> str:
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
            frame_id_to_time.items(), key=(lambda item: item[1]), reverse=False
        )

        if not self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_26(self, frame: Frame, precision: int) -> str:
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

        if self.show_all:
            # remove nodes that represent less than 0.1% of the total time
            id_time_pairs = [
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_27(self, frame: Frame, precision: int) -> str:
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
            id_time_pairs = None

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_28(self, frame: Frame, precision: int) -> str:
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
                pair for pair in id_time_pairs if pair[1] * self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_29(self, frame: Frame, precision: int) -> str:
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
                pair for pair in id_time_pairs if pair[2] / self.root_frame.time > 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_30(self, frame: Frame, precision: int) -> str:
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
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time >= 0.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_31(self, frame: Frame, precision: int) -> str:
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
                pair for pair in id_time_pairs if pair[1] / self.root_frame.time > 1.001
            ]

        result = ""

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_32(self, frame: Frame, precision: int) -> str:
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

        result = None

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_33(self, frame: Frame, precision: int) -> str:
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

        result = "XXXX"

        for frame_id, self_time in id_time_pairs:
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_34(self, frame: Frame, precision: int) -> str:
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
            result = self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_35(self, frame: Frame, precision: int) -> str:
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
            result -= self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_36(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                None, precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_37(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=None, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_38(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=None
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_39(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                precision=precision, override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_40(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], override_time=self_time
            )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_41(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, )
            result += "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_42(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result = "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_43(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result -= "\n"

        return result

    def xǁConsoleRendererǁrender_frame_flat__mutmut_44(self, frame: Frame, precision: int) -> str:
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
            result += self.frame_description(
                frame_id_to_frame[frame_id], precision=precision, override_time=self_time
            )
            result += "XX\nXX"

        return result
    
    xǁConsoleRendererǁrender_frame_flat__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁrender_frame_flat__mutmut_1': xǁConsoleRendererǁrender_frame_flat__mutmut_1, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_2': xǁConsoleRendererǁrender_frame_flat__mutmut_2, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_3': xǁConsoleRendererǁrender_frame_flat__mutmut_3, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_4': xǁConsoleRendererǁrender_frame_flat__mutmut_4, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_5': xǁConsoleRendererǁrender_frame_flat__mutmut_5, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_6': xǁConsoleRendererǁrender_frame_flat__mutmut_6, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_7': xǁConsoleRendererǁrender_frame_flat__mutmut_7, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_8': xǁConsoleRendererǁrender_frame_flat__mutmut_8, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_9': xǁConsoleRendererǁrender_frame_flat__mutmut_9, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_10': xǁConsoleRendererǁrender_frame_flat__mutmut_10, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_11': xǁConsoleRendererǁrender_frame_flat__mutmut_11, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_12': xǁConsoleRendererǁrender_frame_flat__mutmut_12, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_13': xǁConsoleRendererǁrender_frame_flat__mutmut_13, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_14': xǁConsoleRendererǁrender_frame_flat__mutmut_14, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_15': xǁConsoleRendererǁrender_frame_flat__mutmut_15, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_16': xǁConsoleRendererǁrender_frame_flat__mutmut_16, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_17': xǁConsoleRendererǁrender_frame_flat__mutmut_17, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_18': xǁConsoleRendererǁrender_frame_flat__mutmut_18, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_19': xǁConsoleRendererǁrender_frame_flat__mutmut_19, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_20': xǁConsoleRendererǁrender_frame_flat__mutmut_20, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_21': xǁConsoleRendererǁrender_frame_flat__mutmut_21, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_22': xǁConsoleRendererǁrender_frame_flat__mutmut_22, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_23': xǁConsoleRendererǁrender_frame_flat__mutmut_23, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_24': xǁConsoleRendererǁrender_frame_flat__mutmut_24, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_25': xǁConsoleRendererǁrender_frame_flat__mutmut_25, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_26': xǁConsoleRendererǁrender_frame_flat__mutmut_26, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_27': xǁConsoleRendererǁrender_frame_flat__mutmut_27, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_28': xǁConsoleRendererǁrender_frame_flat__mutmut_28, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_29': xǁConsoleRendererǁrender_frame_flat__mutmut_29, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_30': xǁConsoleRendererǁrender_frame_flat__mutmut_30, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_31': xǁConsoleRendererǁrender_frame_flat__mutmut_31, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_32': xǁConsoleRendererǁrender_frame_flat__mutmut_32, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_33': xǁConsoleRendererǁrender_frame_flat__mutmut_33, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_34': xǁConsoleRendererǁrender_frame_flat__mutmut_34, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_35': xǁConsoleRendererǁrender_frame_flat__mutmut_35, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_36': xǁConsoleRendererǁrender_frame_flat__mutmut_36, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_37': xǁConsoleRendererǁrender_frame_flat__mutmut_37, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_38': xǁConsoleRendererǁrender_frame_flat__mutmut_38, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_39': xǁConsoleRendererǁrender_frame_flat__mutmut_39, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_40': xǁConsoleRendererǁrender_frame_flat__mutmut_40, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_41': xǁConsoleRendererǁrender_frame_flat__mutmut_41, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_42': xǁConsoleRendererǁrender_frame_flat__mutmut_42, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_43': xǁConsoleRendererǁrender_frame_flat__mutmut_43, 
        'xǁConsoleRendererǁrender_frame_flat__mutmut_44': xǁConsoleRendererǁrender_frame_flat__mutmut_44
    }
    
    def render_frame_flat(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁrender_frame_flat__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁrender_frame_flat__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render_frame_flat.__signature__ = _mutmut_signature(xǁConsoleRendererǁrender_frame_flat__mutmut_orig)
    xǁConsoleRendererǁrender_frame_flat__mutmut_orig.__name__ = 'xǁConsoleRendererǁrender_frame_flat'

    def xǁConsoleRendererǁframe_description__mutmut_orig(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_1(
        self, frame: Frame, *, precision: int = 4, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_2(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = None
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_3(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_4(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = None

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_5(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(None)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_6(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time != "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_7(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "XXpercent_of_totalXX":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_8(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "PERCENT_OF_TOTAL":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_9(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = None
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_10(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) / 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_11(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(None) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_12(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 101:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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

    def xǁConsoleRendererǁframe_description__mutmut_13(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = None

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

    def xǁConsoleRendererǁframe_description__mutmut_14(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

        value_str = None

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

    def xǁConsoleRendererǁframe_description__mutmut_15(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

        value_str = f"{time_color}{time_str}{self.colors.end}"

        class_name = None
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

    def xǁConsoleRendererǁframe_description__mutmut_16(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

        value_str = f"{time_color}{time_str}{self.colors.end}"

        class_name = frame.class_name
        if class_name:
            function_name = None
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

    def xǁConsoleRendererǁframe_description__mutmut_17(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

        value_str = f"{time_color}{time_str}{self.colors.end}"

        class_name = frame.class_name
        if class_name:
            function_name = f"{class_name}.{frame.function}"
        else:
            function_name = None
        function_color = self._ansi_color_for_name(frame)
        function_str = f"{function_color}{function_name}{self.colors.end}"

        code_position_short = frame.code_position_short()
        if code_position_short:
            code_position_str = f"{self.colors.faint}{code_position_short}{self.colors.end}"
        else:
            code_position_str = ""

        return f"{value_str} {function_str}  {code_position_str}"

    def xǁConsoleRendererǁframe_description__mutmut_18(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

        value_str = f"{time_color}{time_str}{self.colors.end}"

        class_name = frame.class_name
        if class_name:
            function_name = f"{class_name}.{frame.function}"
        else:
            function_name = frame.function
        function_color = None
        function_str = f"{function_color}{function_name}{self.colors.end}"

        code_position_short = frame.code_position_short()
        if code_position_short:
            code_position_str = f"{self.colors.faint}{code_position_short}{self.colors.end}"
        else:
            code_position_str = ""

        return f"{value_str} {function_str}  {code_position_str}"

    def xǁConsoleRendererǁframe_description__mutmut_19(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

        value_str = f"{time_color}{time_str}{self.colors.end}"

        class_name = frame.class_name
        if class_name:
            function_name = f"{class_name}.{frame.function}"
        else:
            function_name = frame.function
        function_color = self._ansi_color_for_name(None)
        function_str = f"{function_color}{function_name}{self.colors.end}"

        code_position_short = frame.code_position_short()
        if code_position_short:
            code_position_str = f"{self.colors.faint}{code_position_short}{self.colors.end}"
        else:
            code_position_str = ""

        return f"{value_str} {function_str}  {code_position_str}"

    def xǁConsoleRendererǁframe_description__mutmut_20(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

        value_str = f"{time_color}{time_str}{self.colors.end}"

        class_name = frame.class_name
        if class_name:
            function_name = f"{class_name}.{frame.function}"
        else:
            function_name = frame.function
        function_color = self._ansi_color_for_name(frame)
        function_str = None

        code_position_short = frame.code_position_short()
        if code_position_short:
            code_position_str = f"{self.colors.faint}{code_position_short}{self.colors.end}"
        else:
            code_position_str = ""

        return f"{value_str} {function_str}  {code_position_str}"

    def xǁConsoleRendererǁframe_description__mutmut_21(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

        value_str = f"{time_color}{time_str}{self.colors.end}"

        class_name = frame.class_name
        if class_name:
            function_name = f"{class_name}.{frame.function}"
        else:
            function_name = frame.function
        function_color = self._ansi_color_for_name(frame)
        function_str = f"{function_color}{function_name}{self.colors.end}"

        code_position_short = None
        if code_position_short:
            code_position_str = f"{self.colors.faint}{code_position_short}{self.colors.end}"
        else:
            code_position_str = ""

        return f"{value_str} {function_str}  {code_position_str}"

    def xǁConsoleRendererǁframe_description__mutmut_22(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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
            code_position_str = None
        else:
            code_position_str = ""

        return f"{value_str} {function_str}  {code_position_str}"

    def xǁConsoleRendererǁframe_description__mutmut_23(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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
            code_position_str = None

        return f"{value_str} {function_str}  {code_position_str}"

    def xǁConsoleRendererǁframe_description__mutmut_24(
        self, frame: Frame, *, precision: int = 3, override_time: float | None = None
    ) -> str:
        time = override_time if override_time is not None else frame.time
        time_color = self._ansi_color_for_time(time)

        if self.time == "percent_of_total":
            time_str = f"{self.frame_proportion_of_total_time(time) * 100:.1f}%"
        else:
            time_str = f"{time:.{precision}f}"

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
            code_position_str = "XXXX"

        return f"{value_str} {function_str}  {code_position_str}"
    
    xǁConsoleRendererǁframe_description__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁframe_description__mutmut_1': xǁConsoleRendererǁframe_description__mutmut_1, 
        'xǁConsoleRendererǁframe_description__mutmut_2': xǁConsoleRendererǁframe_description__mutmut_2, 
        'xǁConsoleRendererǁframe_description__mutmut_3': xǁConsoleRendererǁframe_description__mutmut_3, 
        'xǁConsoleRendererǁframe_description__mutmut_4': xǁConsoleRendererǁframe_description__mutmut_4, 
        'xǁConsoleRendererǁframe_description__mutmut_5': xǁConsoleRendererǁframe_description__mutmut_5, 
        'xǁConsoleRendererǁframe_description__mutmut_6': xǁConsoleRendererǁframe_description__mutmut_6, 
        'xǁConsoleRendererǁframe_description__mutmut_7': xǁConsoleRendererǁframe_description__mutmut_7, 
        'xǁConsoleRendererǁframe_description__mutmut_8': xǁConsoleRendererǁframe_description__mutmut_8, 
        'xǁConsoleRendererǁframe_description__mutmut_9': xǁConsoleRendererǁframe_description__mutmut_9, 
        'xǁConsoleRendererǁframe_description__mutmut_10': xǁConsoleRendererǁframe_description__mutmut_10, 
        'xǁConsoleRendererǁframe_description__mutmut_11': xǁConsoleRendererǁframe_description__mutmut_11, 
        'xǁConsoleRendererǁframe_description__mutmut_12': xǁConsoleRendererǁframe_description__mutmut_12, 
        'xǁConsoleRendererǁframe_description__mutmut_13': xǁConsoleRendererǁframe_description__mutmut_13, 
        'xǁConsoleRendererǁframe_description__mutmut_14': xǁConsoleRendererǁframe_description__mutmut_14, 
        'xǁConsoleRendererǁframe_description__mutmut_15': xǁConsoleRendererǁframe_description__mutmut_15, 
        'xǁConsoleRendererǁframe_description__mutmut_16': xǁConsoleRendererǁframe_description__mutmut_16, 
        'xǁConsoleRendererǁframe_description__mutmut_17': xǁConsoleRendererǁframe_description__mutmut_17, 
        'xǁConsoleRendererǁframe_description__mutmut_18': xǁConsoleRendererǁframe_description__mutmut_18, 
        'xǁConsoleRendererǁframe_description__mutmut_19': xǁConsoleRendererǁframe_description__mutmut_19, 
        'xǁConsoleRendererǁframe_description__mutmut_20': xǁConsoleRendererǁframe_description__mutmut_20, 
        'xǁConsoleRendererǁframe_description__mutmut_21': xǁConsoleRendererǁframe_description__mutmut_21, 
        'xǁConsoleRendererǁframe_description__mutmut_22': xǁConsoleRendererǁframe_description__mutmut_22, 
        'xǁConsoleRendererǁframe_description__mutmut_23': xǁConsoleRendererǁframe_description__mutmut_23, 
        'xǁConsoleRendererǁframe_description__mutmut_24': xǁConsoleRendererǁframe_description__mutmut_24
    }
    
    def frame_description(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁframe_description__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁframe_description__mutmut_mutants"), args, kwargs, self)
        return result 
    
    frame_description.__signature__ = _mutmut_signature(xǁConsoleRendererǁframe_description__mutmut_orig)
    xǁConsoleRendererǁframe_description__mutmut_orig.__name__ = 'xǁConsoleRendererǁframe_description'

    def xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_orig(self, time: float) -> float:
        if self.root_frame.time == 0:
            return 1
        return time / self.root_frame.time

    def xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_1(self, time: float) -> float:
        if self.root_frame.time != 0:
            return 1
        return time / self.root_frame.time

    def xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_2(self, time: float) -> float:
        if self.root_frame.time == 1:
            return 1
        return time / self.root_frame.time

    def xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_3(self, time: float) -> float:
        if self.root_frame.time == 0:
            return 2
        return time / self.root_frame.time

    def xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_4(self, time: float) -> float:
        if self.root_frame.time == 0:
            return 1
        return time * self.root_frame.time
    
    xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_1': xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_1, 
        'xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_2': xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_2, 
        'xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_3': xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_3, 
        'xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_4': xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_4
    }
    
    def frame_proportion_of_total_time(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_mutants"), args, kwargs, self)
        return result 
    
    frame_proportion_of_total_time.__signature__ = _mutmut_signature(xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_orig)
    xǁConsoleRendererǁframe_proportion_of_total_time__mutmut_orig.__name__ = 'xǁConsoleRendererǁframe_proportion_of_total_time'

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_orig(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_1(self, time: float) -> str:
        proportion_of_total = None

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_2(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(None)

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_3(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total >= 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_4(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total > 1.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_5(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total >= 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_6(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 1.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_7(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total >= 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_8(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 1.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def xǁConsoleRendererǁ_ansi_color_for_time__mutmut_9(self, time: float) -> str:
        proportion_of_total = self.frame_proportion_of_total_time(time)

        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green - self.colors.faint
    
    xǁConsoleRendererǁ_ansi_color_for_time__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁ_ansi_color_for_time__mutmut_1': xǁConsoleRendererǁ_ansi_color_for_time__mutmut_1, 
        'xǁConsoleRendererǁ_ansi_color_for_time__mutmut_2': xǁConsoleRendererǁ_ansi_color_for_time__mutmut_2, 
        'xǁConsoleRendererǁ_ansi_color_for_time__mutmut_3': xǁConsoleRendererǁ_ansi_color_for_time__mutmut_3, 
        'xǁConsoleRendererǁ_ansi_color_for_time__mutmut_4': xǁConsoleRendererǁ_ansi_color_for_time__mutmut_4, 
        'xǁConsoleRendererǁ_ansi_color_for_time__mutmut_5': xǁConsoleRendererǁ_ansi_color_for_time__mutmut_5, 
        'xǁConsoleRendererǁ_ansi_color_for_time__mutmut_6': xǁConsoleRendererǁ_ansi_color_for_time__mutmut_6, 
        'xǁConsoleRendererǁ_ansi_color_for_time__mutmut_7': xǁConsoleRendererǁ_ansi_color_for_time__mutmut_7, 
        'xǁConsoleRendererǁ_ansi_color_for_time__mutmut_8': xǁConsoleRendererǁ_ansi_color_for_time__mutmut_8, 
        'xǁConsoleRendererǁ_ansi_color_for_time__mutmut_9': xǁConsoleRendererǁ_ansi_color_for_time__mutmut_9
    }
    
    def _ansi_color_for_time(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁ_ansi_color_for_time__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁ_ansi_color_for_time__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _ansi_color_for_time.__signature__ = _mutmut_signature(xǁConsoleRendererǁ_ansi_color_for_time__mutmut_orig)
    xǁConsoleRendererǁ_ansi_color_for_time__mutmut_orig.__name__ = 'xǁConsoleRendererǁ_ansi_color_for_time'

    def xǁConsoleRendererǁ_ansi_color_for_name__mutmut_orig(self, frame: Frame) -> str:
        if frame.is_application_code:
            return self.colors.bg_dark_blue_255 + self.colors.white_255
        else:
            return ""

    def xǁConsoleRendererǁ_ansi_color_for_name__mutmut_1(self, frame: Frame) -> str:
        if frame.is_application_code:
            return self.colors.bg_dark_blue_255 - self.colors.white_255
        else:
            return ""

    def xǁConsoleRendererǁ_ansi_color_for_name__mutmut_2(self, frame: Frame) -> str:
        if frame.is_application_code:
            return self.colors.bg_dark_blue_255 + self.colors.white_255
        else:
            return "XXXX"
    
    xǁConsoleRendererǁ_ansi_color_for_name__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁConsoleRendererǁ_ansi_color_for_name__mutmut_1': xǁConsoleRendererǁ_ansi_color_for_name__mutmut_1, 
        'xǁConsoleRendererǁ_ansi_color_for_name__mutmut_2': xǁConsoleRendererǁ_ansi_color_for_name__mutmut_2
    }
    
    def _ansi_color_for_name(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁConsoleRendererǁ_ansi_color_for_name__mutmut_orig"), object.__getattribute__(self, "xǁConsoleRendererǁ_ansi_color_for_name__mutmut_mutants"), args, kwargs, self)
        return result 
    
    _ansi_color_for_name.__signature__ = _mutmut_signature(xǁConsoleRendererǁ_ansi_color_for_name__mutmut_orig)
    xǁConsoleRendererǁ_ansi_color_for_name__mutmut_orig.__name__ = 'xǁConsoleRendererǁ_ansi_color_for_name'

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
