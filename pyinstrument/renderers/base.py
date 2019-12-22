from pyinstrument import processors


class Renderer(object):
    def __init__(self, show_all=False, timeline=False, processor_options=None):
        # processors is defined on the base class to provide a common way for users to
        # add to and manipulate them before calling render()
        self.processors = self.default_processors()
        self.processor_options = processor_options or {}

        if show_all:
            self.processors.remove(processors.group_library_frames_processor)
        if timeline:
            self.processors.remove(processors.aggregate_repeated_calls)

    def default_processors(self):
        ''' 
        Return a list of processors that this renderer uses by default
        '''
        raise NotImplementedError()

    def preprocess(self, root_frame):
        frame = root_frame
        for processor in self.processors:
            frame = processor(frame, options=self.processor_options)
        return frame

    def render(self, session):
        '''
        Return a string that contains the rendered form of `frame`
        '''
        raise NotImplementedError()
