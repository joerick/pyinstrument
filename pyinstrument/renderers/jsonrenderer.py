import json
from pyinstrument.renderers.base import Renderer
from pyinstrument import processors

# note: this file is called jsonrenderer to avoid hiding built-in module 'json'.

class JSONRenderer(Renderer):
    def render_frame(self, frame):
        # we don't use the json module because it uses 2x stack frames 
        encode = json.encoder.encode_basestring

        property_decls = []
        property_decls.append('"function": %s' % encode(frame.function))
        property_decls.append('"file_path_short": %s' % encode(frame.file_path_short))
        property_decls.append('"file_path": %s' % encode(frame.file_path))
        property_decls.append('"line_no": %d' % frame.line_no)
        property_decls.append('"time": %f' % frame.time())

        # can't use list comprehension here because it uses two stack frames each time.
        children_jsons = []
        for child in frame.children:
            children_jsons.append(self.render_frame(child))
        property_decls.append('"children": [%s]' % ','.join(children_jsons))

        if frame.group:
            property_decls.append('"group_id": %s' % encode(frame.group.id))
        
        return '{%s}' % ','.join(property_decls)

    def render(self, session):
        frame = self.preprocess(session.root_frame())
        return self.render_frame(frame)

    def default_processors(self):
        return [
            processors.remove_importlib,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
        ]
