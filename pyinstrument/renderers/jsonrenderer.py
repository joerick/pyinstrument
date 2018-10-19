import json
from pyinstrument.renderers.base import Renderer
from pyinstrument import processors

# note: this file is called jsonrenderer to avoid hiding built-in module 'json'.

class JSONRenderer(Renderer):
    def __init__(self, include_groups=True, **kwargs):
        super(JSONRenderer, self).__init__(**kwargs)
        self.include_groups = include_groups

    def render_frame(self, frame):
        frame_dict = {
            'function': frame.function,
            'file_path_short': frame.file_path_short,
            'file_path': frame.file_path,
            'line_no': frame.line_no,
            'time': frame.time(),
        }

        # can't use list comprehension here because it uses two stack frames each time.
        children_json = []
        for child in frame.children:
            children_json.append(self.render_frame(child))
        frame_dict['children'] = children_json

        if self.include_groups and frame.group:
            frame_dict['group_id'] = frame.group.id
        
        return frame_dict

    def render(self, session):
        frame = self.preprocess(session.root_frame())
        return json.dumps({
            'root_frame': self.render_frame(frame),
            'start_time': session.start_time,
            'duration': session.duration,
            'sample_count': session.sample_count,
            'program': session.program,
            'cpu_time': session.cpu_time,
        }, indent=2)

    def default_processors(self):
        return processors.default_time_aggregate_processors()
