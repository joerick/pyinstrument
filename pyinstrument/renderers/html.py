import os
from pyinstrument.renderers.base import Renderer
from pyinstrument.renderers.jsonrenderer import JSONRenderer
from pyinstrument import processors
try:
    from html import escape as html_escape
except ImportError:
    from cgi import escape as html_escape


class HTMLRenderer(Renderer):
    def render(self, session):
        resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_resources/')

        with open(os.path.join(resources_dir, 'app.js')) as f:
            js = f.read()

        session_json = self.render_json(session)

        page = '''<!DOCTYPE html>
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

    def render_json(self, session):
        json_renderer = JSONRenderer(include_groups=True)
        json_renderer.processors = self.processors
        return json_renderer.render(session)

    def default_processors(self):
        return processors.default_time_aggregate_processors()
