from __future__ import annotations

import codecs
import os
import tempfile
import urllib.parse
import webbrowser
from typing import Any

from pyinstrument import processors
from pyinstrument.renderers.base import ProcessorList, Renderer
from pyinstrument.renderers.jsonrenderer import JSONRenderer
from pyinstrument.session import Session

# pyright: strict


class HTMLRenderer(Renderer):
    """
    Renders a rich, interactive web page, as a string of HTML.
    """

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def render(self, session: Session):
        resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html_resources/")

        if not os.path.exists(os.path.join(resources_dir, "app.js")):
            raise RuntimeError(
                "Could not find app.js. If you are running "
                "pyinstrument from a git checkout, run 'python "
                "setup.py build' to compile the Javascript "
                "(requires nodejs)."
            )

        with open(os.path.join(resources_dir, "app.js"), encoding="utf-8") as f:
            js = f.read()

        session_json = self.render_json(session)

        page = """<!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
            </head>
            <body>
                <div id="app"></div>
                <script>
                    window.profileSession = {session_json}
                </script>
                <script>
                    {js}
                </script>
            </body>
            </html>""".format(
            js=js, session_json=session_json
        )

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
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
        ]
