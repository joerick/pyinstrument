import os, io
import codecs
import tempfile
import webbrowser
from pyinstrument.renderers.base import Renderer
from pyinstrument.renderers.jsonrenderer import JSONRenderer
from pyinstrument import processors


class HTMLRenderer(Renderer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, session):
        resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_resources/')

        if not os.path.exists(os.path.join(resources_dir, 'app.js')):
            raise RuntimeError("Could not find app.js. If you are running "
                               "pyinstrument from a git checkout, run 'python "
                               "setup.py build' to compile the Javascript "
                               "(requires nodejs).")

        with io.open(os.path.join(resources_dir, 'app.js'), encoding='utf-8') as f:
            js = f.read()

        session_json = self.render_json(session)

        page = u'''<!DOCTYPE html>
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
            </html>'''.format(js=js, session_json=session_json)

        return page

    def open_in_browser(self, session, output_filename=None):
        """
        Open the rendered HTML in a webbrowser.

        If output_filename=None (the default), a tempfile is used.

        The filename of the HTML file is returned.

        """
        if output_filename is None:
            output_file = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
            output_filename = output_file.name
            with codecs.getwriter('utf-8')(output_file) as f:
                f.write(self.render(session))
        else:
            with codecs.open(output_filename, 'w', 'utf-8') as f:
                f.write(self.render(session))

        from pyinstrument.vendor.six.moves import urllib
        url = urllib.parse.urlunparse(('file', '', output_filename, '', '', ''))
        webbrowser.open(url)
        return output_filename

    def render_json(self, session):
        json_renderer = JSONRenderer()
        json_renderer.processors = self.processors
        return json_renderer.render(session)

    def default_processors(self):
        return [
            processors.remove_importlib,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
        ]
