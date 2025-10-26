from __future__ import annotations

import codecs
import json
import tempfile
import urllib.parse
import warnings
import webbrowser
from pathlib import Path

from pyinstrument.renderers.base import FrameRenderer, ProcessorList, Renderer
from pyinstrument.session import Session
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

# pyright: strict


class HTMLRenderer(Renderer):
    """
    Renders a rich, interactive web page, as a string of HTML.
    """

    output_file_extension = "html"

    def xǁHTMLRendererǁ__init____mutmut_orig(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_1(
        self,
        show_all: bool = True,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_2(
        self,
        show_all: bool = False,
        timeline: bool = True,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_3(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                None,
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_4(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                None,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_5(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=None,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_6(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_7(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_8(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_9(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=4,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_10(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                None,
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_11(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                None,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_12(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=None,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_13(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_14(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_15(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_16(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=4,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = []

    def xǁHTMLRendererǁ__init____mutmut_17(
        self,
        show_all: bool = False,
        timeline: bool = False,
    ):
        super().__init__()
        if show_all:
            warnings.warn(
                f"the show_all option is deprecated on the HTML renderer, and has no effect. Use the view options in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        if timeline:
            warnings.warn(
                f"timeline is deprecated on the HTML renderer, and has no effect. Use the timeline view in the webpage instead.",
                DeprecationWarning,
                stacklevel=3,
            )
        # this is an undocumented option for use by the ipython magic, might
        # be removed later
        self.preprocessors: ProcessorList = None
    
    xǁHTMLRendererǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHTMLRendererǁ__init____mutmut_1': xǁHTMLRendererǁ__init____mutmut_1, 
        'xǁHTMLRendererǁ__init____mutmut_2': xǁHTMLRendererǁ__init____mutmut_2, 
        'xǁHTMLRendererǁ__init____mutmut_3': xǁHTMLRendererǁ__init____mutmut_3, 
        'xǁHTMLRendererǁ__init____mutmut_4': xǁHTMLRendererǁ__init____mutmut_4, 
        'xǁHTMLRendererǁ__init____mutmut_5': xǁHTMLRendererǁ__init____mutmut_5, 
        'xǁHTMLRendererǁ__init____mutmut_6': xǁHTMLRendererǁ__init____mutmut_6, 
        'xǁHTMLRendererǁ__init____mutmut_7': xǁHTMLRendererǁ__init____mutmut_7, 
        'xǁHTMLRendererǁ__init____mutmut_8': xǁHTMLRendererǁ__init____mutmut_8, 
        'xǁHTMLRendererǁ__init____mutmut_9': xǁHTMLRendererǁ__init____mutmut_9, 
        'xǁHTMLRendererǁ__init____mutmut_10': xǁHTMLRendererǁ__init____mutmut_10, 
        'xǁHTMLRendererǁ__init____mutmut_11': xǁHTMLRendererǁ__init____mutmut_11, 
        'xǁHTMLRendererǁ__init____mutmut_12': xǁHTMLRendererǁ__init____mutmut_12, 
        'xǁHTMLRendererǁ__init____mutmut_13': xǁHTMLRendererǁ__init____mutmut_13, 
        'xǁHTMLRendererǁ__init____mutmut_14': xǁHTMLRendererǁ__init____mutmut_14, 
        'xǁHTMLRendererǁ__init____mutmut_15': xǁHTMLRendererǁ__init____mutmut_15, 
        'xǁHTMLRendererǁ__init____mutmut_16': xǁHTMLRendererǁ__init____mutmut_16, 
        'xǁHTMLRendererǁ__init____mutmut_17': xǁHTMLRendererǁ__init____mutmut_17
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHTMLRendererǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁHTMLRendererǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁHTMLRendererǁ__init____mutmut_orig)
    xǁHTMLRendererǁ__init____mutmut_orig.__name__ = 'xǁHTMLRendererǁ__init__'

    def xǁHTMLRendererǁrender__mutmut_orig(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_1(self, session: Session):
        json_renderer = None
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_2(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = None
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_3(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = None

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_4(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(None)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_5(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = None

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_6(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent * "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_7(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(None).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_8(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "XXhtml_resourcesXX"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_9(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "HTML_RESOURCES"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_10(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = None
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_11(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir * "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_12(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "XXapp.jsXX"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_13(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "APP.JS"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_14(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = None

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_15(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir * "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_16(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "XXapp.cssXX"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_17(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "APP.CSS"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_18(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() and not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_19(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_20(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_21(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                None
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_22(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "XXCould not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?XX"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_23(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "could not find app.js / app.css. perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_24(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "COULD NOT FIND APP.JS / APP.CSS. PERHAPS YOU NEED TO RUN BIN/BUILD_JS_BUNDLE.PY?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_25(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = None
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_26(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding=None)
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_27(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="XXutf-8XX")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_28(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="UTF-8")
        css = css_file.read_text(encoding="utf-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_29(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = None

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_30(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding=None)

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_31(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="XXutf-8XX")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_32(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="UTF-8")

        page = f"""<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>

                <script>{js}</script>
                <style>{css}</style>

                <script>
                    const sessionData = {session_json};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData);
                </script>
            </body>
            </html>
        """

        return page

    def xǁHTMLRendererǁrender__mutmut_33(self, session: Session):
        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        session_json = json_renderer.render(session)

        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text(encoding="utf-8")
        css = css_file.read_text(encoding="utf-8")

        page = None

        return page
    
    xǁHTMLRendererǁrender__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHTMLRendererǁrender__mutmut_1': xǁHTMLRendererǁrender__mutmut_1, 
        'xǁHTMLRendererǁrender__mutmut_2': xǁHTMLRendererǁrender__mutmut_2, 
        'xǁHTMLRendererǁrender__mutmut_3': xǁHTMLRendererǁrender__mutmut_3, 
        'xǁHTMLRendererǁrender__mutmut_4': xǁHTMLRendererǁrender__mutmut_4, 
        'xǁHTMLRendererǁrender__mutmut_5': xǁHTMLRendererǁrender__mutmut_5, 
        'xǁHTMLRendererǁrender__mutmut_6': xǁHTMLRendererǁrender__mutmut_6, 
        'xǁHTMLRendererǁrender__mutmut_7': xǁHTMLRendererǁrender__mutmut_7, 
        'xǁHTMLRendererǁrender__mutmut_8': xǁHTMLRendererǁrender__mutmut_8, 
        'xǁHTMLRendererǁrender__mutmut_9': xǁHTMLRendererǁrender__mutmut_9, 
        'xǁHTMLRendererǁrender__mutmut_10': xǁHTMLRendererǁrender__mutmut_10, 
        'xǁHTMLRendererǁrender__mutmut_11': xǁHTMLRendererǁrender__mutmut_11, 
        'xǁHTMLRendererǁrender__mutmut_12': xǁHTMLRendererǁrender__mutmut_12, 
        'xǁHTMLRendererǁrender__mutmut_13': xǁHTMLRendererǁrender__mutmut_13, 
        'xǁHTMLRendererǁrender__mutmut_14': xǁHTMLRendererǁrender__mutmut_14, 
        'xǁHTMLRendererǁrender__mutmut_15': xǁHTMLRendererǁrender__mutmut_15, 
        'xǁHTMLRendererǁrender__mutmut_16': xǁHTMLRendererǁrender__mutmut_16, 
        'xǁHTMLRendererǁrender__mutmut_17': xǁHTMLRendererǁrender__mutmut_17, 
        'xǁHTMLRendererǁrender__mutmut_18': xǁHTMLRendererǁrender__mutmut_18, 
        'xǁHTMLRendererǁrender__mutmut_19': xǁHTMLRendererǁrender__mutmut_19, 
        'xǁHTMLRendererǁrender__mutmut_20': xǁHTMLRendererǁrender__mutmut_20, 
        'xǁHTMLRendererǁrender__mutmut_21': xǁHTMLRendererǁrender__mutmut_21, 
        'xǁHTMLRendererǁrender__mutmut_22': xǁHTMLRendererǁrender__mutmut_22, 
        'xǁHTMLRendererǁrender__mutmut_23': xǁHTMLRendererǁrender__mutmut_23, 
        'xǁHTMLRendererǁrender__mutmut_24': xǁHTMLRendererǁrender__mutmut_24, 
        'xǁHTMLRendererǁrender__mutmut_25': xǁHTMLRendererǁrender__mutmut_25, 
        'xǁHTMLRendererǁrender__mutmut_26': xǁHTMLRendererǁrender__mutmut_26, 
        'xǁHTMLRendererǁrender__mutmut_27': xǁHTMLRendererǁrender__mutmut_27, 
        'xǁHTMLRendererǁrender__mutmut_28': xǁHTMLRendererǁrender__mutmut_28, 
        'xǁHTMLRendererǁrender__mutmut_29': xǁHTMLRendererǁrender__mutmut_29, 
        'xǁHTMLRendererǁrender__mutmut_30': xǁHTMLRendererǁrender__mutmut_30, 
        'xǁHTMLRendererǁrender__mutmut_31': xǁHTMLRendererǁrender__mutmut_31, 
        'xǁHTMLRendererǁrender__mutmut_32': xǁHTMLRendererǁrender__mutmut_32, 
        'xǁHTMLRendererǁrender__mutmut_33': xǁHTMLRendererǁrender__mutmut_33
    }
    
    def render(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHTMLRendererǁrender__mutmut_orig"), object.__getattribute__(self, "xǁHTMLRendererǁrender__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render.__signature__ = _mutmut_signature(xǁHTMLRendererǁrender__mutmut_orig)
    xǁHTMLRendererǁrender__mutmut_orig.__name__ = 'xǁHTMLRendererǁrender'

    def xǁHTMLRendererǁopen_in_browser__mutmut_orig(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_1(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is not None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_2(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = None
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_3(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=None, delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_4(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=None)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_5(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_6(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", )
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_7(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix="XX.htmlXX", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_8(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".HTML", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_9(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=True)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_10(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = None
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_11(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(None) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_12(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter(None)(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_13(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("XXutf-8XX")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_14(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("UTF-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_15(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(None)
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_16(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(None))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_17(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(None, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_18(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, None, "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_19(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", None) as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_20(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open("w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_21(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_22(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", ) as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_23(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "XXwXX", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_24(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "W", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_25(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "XXutf-8XX") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_26(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "UTF-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_27(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(None)

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_28(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(None))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_29(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = None
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_30(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(None)
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_31(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("XXfileXX", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_32(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("FILE", "", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_33(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "XXXX", output_filename, "", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_34(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "XXXX", "", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_35(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "XXXX", ""))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_36(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", "XXXX"))
        webbrowser.open(url)
        return output_filename

    def xǁHTMLRendererǁopen_in_browser__mutmut_37(self, session: Session, output_filename: str | None = None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
            output_filename = output_file.name
            with codecs.getwriter("utf-8")(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, "w", "utf-8") as f:
                f.write(self.render(session))

        url = urllib.parse.urlunparse(("file", "", output_filename, "", "", ""))
        webbrowser.open(None)
        return output_filename
    
    xǁHTMLRendererǁopen_in_browser__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁHTMLRendererǁopen_in_browser__mutmut_1': xǁHTMLRendererǁopen_in_browser__mutmut_1, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_2': xǁHTMLRendererǁopen_in_browser__mutmut_2, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_3': xǁHTMLRendererǁopen_in_browser__mutmut_3, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_4': xǁHTMLRendererǁopen_in_browser__mutmut_4, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_5': xǁHTMLRendererǁopen_in_browser__mutmut_5, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_6': xǁHTMLRendererǁopen_in_browser__mutmut_6, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_7': xǁHTMLRendererǁopen_in_browser__mutmut_7, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_8': xǁHTMLRendererǁopen_in_browser__mutmut_8, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_9': xǁHTMLRendererǁopen_in_browser__mutmut_9, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_10': xǁHTMLRendererǁopen_in_browser__mutmut_10, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_11': xǁHTMLRendererǁopen_in_browser__mutmut_11, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_12': xǁHTMLRendererǁopen_in_browser__mutmut_12, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_13': xǁHTMLRendererǁopen_in_browser__mutmut_13, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_14': xǁHTMLRendererǁopen_in_browser__mutmut_14, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_15': xǁHTMLRendererǁopen_in_browser__mutmut_15, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_16': xǁHTMLRendererǁopen_in_browser__mutmut_16, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_17': xǁHTMLRendererǁopen_in_browser__mutmut_17, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_18': xǁHTMLRendererǁopen_in_browser__mutmut_18, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_19': xǁHTMLRendererǁopen_in_browser__mutmut_19, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_20': xǁHTMLRendererǁopen_in_browser__mutmut_20, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_21': xǁHTMLRendererǁopen_in_browser__mutmut_21, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_22': xǁHTMLRendererǁopen_in_browser__mutmut_22, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_23': xǁHTMLRendererǁopen_in_browser__mutmut_23, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_24': xǁHTMLRendererǁopen_in_browser__mutmut_24, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_25': xǁHTMLRendererǁopen_in_browser__mutmut_25, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_26': xǁHTMLRendererǁopen_in_browser__mutmut_26, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_27': xǁHTMLRendererǁopen_in_browser__mutmut_27, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_28': xǁHTMLRendererǁopen_in_browser__mutmut_28, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_29': xǁHTMLRendererǁopen_in_browser__mutmut_29, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_30': xǁHTMLRendererǁopen_in_browser__mutmut_30, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_31': xǁHTMLRendererǁopen_in_browser__mutmut_31, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_32': xǁHTMLRendererǁopen_in_browser__mutmut_32, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_33': xǁHTMLRendererǁopen_in_browser__mutmut_33, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_34': xǁHTMLRendererǁopen_in_browser__mutmut_34, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_35': xǁHTMLRendererǁopen_in_browser__mutmut_35, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_36': xǁHTMLRendererǁopen_in_browser__mutmut_36, 
        'xǁHTMLRendererǁopen_in_browser__mutmut_37': xǁHTMLRendererǁopen_in_browser__mutmut_37
    }
    
    def open_in_browser(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁHTMLRendererǁopen_in_browser__mutmut_orig"), object.__getattribute__(self, "xǁHTMLRendererǁopen_in_browser__mutmut_mutants"), args, kwargs, self)
        return result 
    
    open_in_browser.__signature__ = _mutmut_signature(xǁHTMLRendererǁopen_in_browser__mutmut_orig)
    xǁHTMLRendererǁopen_in_browser__mutmut_orig.__name__ = 'xǁHTMLRendererǁopen_in_browser'


class JSONForHTMLRenderer(FrameRenderer):
    """
    The HTML takes a special form of JSON-encoded session, which includes
    an unprocessed frame tree rather than a list of frame records. This
    reduces the amount of parsing code that must be included in the
    Typescript renderer.
    """

    output_file_extension = "json"

    def default_processors(self) -> ProcessorList:
        return []

    def xǁJSONForHTMLRendererǁrender__mutmut_orig(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_1(self, session: Session) -> str:
        session_json = None
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_2(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=None)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_3(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=True)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_4(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = None
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_5(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(None)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_6(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = None
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_7(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = None
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_8(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(None)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_9(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = None
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_10(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "XXnullXX"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_11(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "NULL"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_12(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' / (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_13(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return 'XX{"session": %s, "frame_tree": %s}XX' % (session_json_str, frame_tree_json_str)

    def xǁJSONForHTMLRendererǁrender__mutmut_14(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"SESSION": %S, "FRAME_TREE": %S}' % (session_json_str, frame_tree_json_str)
    
    xǁJSONForHTMLRendererǁrender__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁJSONForHTMLRendererǁrender__mutmut_1': xǁJSONForHTMLRendererǁrender__mutmut_1, 
        'xǁJSONForHTMLRendererǁrender__mutmut_2': xǁJSONForHTMLRendererǁrender__mutmut_2, 
        'xǁJSONForHTMLRendererǁrender__mutmut_3': xǁJSONForHTMLRendererǁrender__mutmut_3, 
        'xǁJSONForHTMLRendererǁrender__mutmut_4': xǁJSONForHTMLRendererǁrender__mutmut_4, 
        'xǁJSONForHTMLRendererǁrender__mutmut_5': xǁJSONForHTMLRendererǁrender__mutmut_5, 
        'xǁJSONForHTMLRendererǁrender__mutmut_6': xǁJSONForHTMLRendererǁrender__mutmut_6, 
        'xǁJSONForHTMLRendererǁrender__mutmut_7': xǁJSONForHTMLRendererǁrender__mutmut_7, 
        'xǁJSONForHTMLRendererǁrender__mutmut_8': xǁJSONForHTMLRendererǁrender__mutmut_8, 
        'xǁJSONForHTMLRendererǁrender__mutmut_9': xǁJSONForHTMLRendererǁrender__mutmut_9, 
        'xǁJSONForHTMLRendererǁrender__mutmut_10': xǁJSONForHTMLRendererǁrender__mutmut_10, 
        'xǁJSONForHTMLRendererǁrender__mutmut_11': xǁJSONForHTMLRendererǁrender__mutmut_11, 
        'xǁJSONForHTMLRendererǁrender__mutmut_12': xǁJSONForHTMLRendererǁrender__mutmut_12, 
        'xǁJSONForHTMLRendererǁrender__mutmut_13': xǁJSONForHTMLRendererǁrender__mutmut_13, 
        'xǁJSONForHTMLRendererǁrender__mutmut_14': xǁJSONForHTMLRendererǁrender__mutmut_14
    }
    
    def render(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁJSONForHTMLRendererǁrender__mutmut_orig"), object.__getattribute__(self, "xǁJSONForHTMLRendererǁrender__mutmut_mutants"), args, kwargs, self)
        return result 
    
    render.__signature__ = _mutmut_signature(xǁJSONForHTMLRendererǁrender__mutmut_orig)
    xǁJSONForHTMLRendererǁrender__mutmut_orig.__name__ = 'xǁJSONForHTMLRendererǁrender'
