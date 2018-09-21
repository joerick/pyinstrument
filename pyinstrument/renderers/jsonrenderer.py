import json
from pyinstrument.renderers.base import Renderer
from pyinstrument import processors

# note: this file is called jsonrenderer to avoid hiding built-in module 'json'.

class JSONRenderer(Renderer):
    @staticmethod
    def render_frame(frame):
        # can't use list comprehension here because it uses two stack frames each time.
        children_json = []
        for child in frame.children:
            children_json.append(JSONRenderer.render_frame(child))

        return {
            'function': frame.function,
            'file_path_short': frame.file_path_short,
            'file_path': frame.file_path,
            'line_no': frame.line_no,
            'time': frame.time(),
            'children': children_json,
        }

    def render(self, session):
        frame = self.preprocess(session.root_frame())
        return json.dumps(JSONRenderer.render_frame(frame), indent=2)

    def default_processors(self):
        return processors.default_time_aggregate_processors()
