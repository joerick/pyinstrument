import json
from pyinstrument.renderers.base import Renderer
from pyinstrument import processors

# note: this file is called jsonrenderer to avoid hiding built-in module 'json'.

encode_str = json.encoder.encode_basestring

def encode_bool(a_bool):
    return 'true' if a_bool else 'false'


class JSONRenderer(Renderer):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def render_frame(self, frame):
        if frame is None:
            return u'null'
        # we don't use the json module because it uses 2x stack frames, so 
        # crashes on deep but valid call stacks

        property_decls = []
        property_decls.append(u'"function": %s' % encode_str(frame.function))
        property_decls.append(u'"file_path_short": %s' % encode_str(frame.file_path_short))
        property_decls.append(u'"file_path": %s' % encode_str(frame.file_path))
        property_decls.append(u'"line_no": %d' % frame.line_no)
        property_decls.append(u'"time": %f' % frame.time())
        property_decls.append(u'"is_application_code": %s' % encode_bool(frame.is_application_code))

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append(u'"children": [%s]' % u','.join(children_jsons))

        if frame.group:
            property_decls.append(u'"group_id": %s' % encode_str(frame.group.id))
        
        return u'{%s}' % u','.join(property_decls)

    def render(self, session):
        frame = self.preprocess(session.root_frame())

        property_decls = []
        property_decls.append(u'"start_time": %f' % session.start_time)
        property_decls.append(u'"duration": %f' % session.duration)
        property_decls.append(u'"sample_count": %d' % session.sample_count)
        property_decls.append(u'"program": %s' % encode_str(session.program))
        if session.cpu_time is None:
            property_decls.append(u'"cpu_time": null')
        else:
            property_decls.append(u'"cpu_time": %f' % session.cpu_time)
        property_decls.append(u'"root_frame": %s' % self.render_frame(frame))

        return u'{%s}\n' % u','.join(property_decls)

    def default_processors(self):
        return [
            processors.remove_importlib,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
        ]
