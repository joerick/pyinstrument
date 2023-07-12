from __future__ import annotations

import codecs
import tempfile
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Any

from pyinstrument import processors
from pyinstrument.renderers.base import FrameRenderer, ProcessorList
from pyinstrument.renderers.jsonrenderer import JSONRenderer
from pyinstrument.session import Session

# pyright: strict


class HTMLRenderer(FrameRenderer):
    """
    Renders a rich, interactive web page, as a string of HTML.
    """

    output_file_extension = "html"

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def render(self, session: Session):
        resources_dir = Path(__file__).parent / "html_resources"

        js_file = resources_dir / "app.js"
        css_file = resources_dir / "app.css"

        if not js_file.exists() or not css_file.exists():
            raise RuntimeError(
                "Could not find app.js / app.css. Perhaps you need to run bin/build_js_bundle.py?"
            )

        js = js_file.read_text()
        css = css_file.read_text()

        session_json = self.render_json(session)

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

    def render_json(self, session: Session):
        json_renderer = JSONRenderer()
        json_renderer.processors = self.processors
        json_renderer.processor_options = self.processor_options
        return json_renderer.render(session)

    def default_processors(self) -> ProcessorList:
        return [
            processors.remove_importlib,
            processors.remove_tracebackhide,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
            processors.remove_first_pyinstrument_frames_processor,
            processors.group_library_frames_processor,
        ]
