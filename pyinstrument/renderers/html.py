from __future__ import annotations

import codecs
import json
import sys
import tempfile
import urllib.parse
import warnings
import webbrowser
from pathlib import Path
from typing import Any

from pyinstrument.renderers.base import FrameRenderer, ProcessorList, Renderer
from pyinstrument.session import Session

# pyright: strict


class HTMLRenderer(Renderer):
    """
    Renders a rich, interactive web page, as a string of HTML.
    """

    output_file_extension = "html"

    preprocessors: ProcessorList
    """
    Preprocessors installed on this renderer. This property is similar to
    :attr:`FrameRenderer.processors`, but all pyinstrument's processing is
    done in the webapp, so these are only used to modify the JSON data sent to
    the webapp. For example, you might want to use preprocessors to remove
    unneeded frames from the data to reduce the size of the HTML file.
    """

    preprocessor_options: dict[str, Any]
    """
    Options to pass to the preprocessors, like :attr:`FrameRenderer.processor_options`.
    """

    def __init__(
        self,
        *,
        resample_interval: float | None = None,
        show_all: bool = False,
        timeline: bool = False,
    ):
        """
        :param resample_interval: Controls how the renderer deals with very large sessions. The typically struggles with sessions of more than 100,000 samples. If the session has more samples than this number, it will be automatically resampled to a coarser interval. You can control this interval with this parameter. If None (the default), the interval will be chosen automatically. Setting this to 0 disables resampling.
        """
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

        self.resample_interval = resample_interval

        # These settings are passed down to JSONForHTMLRenderer, and can be
        # used to modify its output. E.g. they can be used to lower the size
        # of the output file, by excluding function calls which take a small
        # fraction of total time.
        self.preprocessors = []
        self.preprocessor_options = {}

    def render(self, session: Session):
        if len(session.frame_records) > 100_000:
            original_session = session
            resample_interval = self.resample_interval
            if resample_interval is None:
                # auto mode: choose an interval that gives us 0.01% resolution
                resample_interval = session.duration / 10000

            if resample_interval > 0:
                session = original_session.resample(interval=resample_interval)

                while len(session.frame_records) > 100_000:
                    resample_interval *= 2
                    session = original_session.resample(interval=resample_interval)
                print(
                    f"pyinstrument: session has {len(original_session.frame_records)} samples, which is too many for the HTML renderer to handle. Resampled to {len(session.frame_records)} samples with interval {resample_interval:.6f} seconds. Set the renderer option resample_interval to control this behaviour.",
                    file=sys.stderr,
                )

        json_renderer = JSONForHTMLRenderer()
        json_renderer.processors = self.preprocessors
        json_renderer.processor_options = self.preprocessor_options
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

    def open_in_browser(self, session: Session, output_filename: str | None = None):
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

    def render(self, session: Session) -> str:
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        root_frame = self.preprocess(root_frame)
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)
