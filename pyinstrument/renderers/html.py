from __future__ import annotations

import codecs
import json
import tempfile
import urllib.parse
import webbrowser
from pathlib import Path
from typing import Any

from pyinstrument.renderers.base import Renderer
from pyinstrument.session import Session

# pyright: strict


class HTMLRenderer(Renderer):
    """
    Renders a rich, interactive web page, as a string of HTML.
    """

    output_file_extension = "html"

    def __init__(
        self,
        show_all: bool = False,
        timeline: bool = False,
        processor_options: dict[str, Any] | None = None,
    ):
        super().__init__()
        self.initial_options = {
            "show_all": show_all,
            "timeline": timeline,
            "processor_options": processor_options or {},
        }

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
                    const initialOptions = {json.dumps(self.initial_options)};
                    pyinstrumentHTMLRenderer.render(document.getElementById('app'), sessionData, initialOptions);
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
        session_json = session.to_json(include_frame_records=False)
        session_json_str = json.dumps(session_json)
        root_frame = session.root_frame()
        frame_tree_json_str = root_frame.to_json_str() if root_frame else "null"
        return '{"session": %s, "frame_tree": %s}' % (session_json_str, frame_tree_json_str)
