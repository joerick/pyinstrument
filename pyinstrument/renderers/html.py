import os, io
from pyinstrument.renderers.base import Renderer
from pyinstrument.renderers.jsonrenderer import JSONRenderer
from pyinstrument import processors


class HTMLRenderer(Renderer):
    def render(self, session):
        resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_resources/')

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
