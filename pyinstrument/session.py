import io, json
from collections import deque
from pyinstrument.frame import Frame, SelfTimeFrame
from pyinstrument.vendor.six import PY2

ASSERTION_MESSAGE = ('Please raise an issue at http://github.com/pyinstrument/issues and '
                     'let me know how you caused this error!')

class ProfilerSession(object):
    def __init__(self, frame_records, start_time, duration, sample_count, start_call_stack, 
                 program, cpu_time=None):
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.program = program
        self.cpu_time = cpu_time

    @staticmethod
    def load(filename):
        with io.open(filename, 'rb' if PY2 else 'r') as f:
            return ProfilerSession.from_json(json.load(f))

    def save(self, filename):
        with io.open(filename, 'wb' if PY2 else 'w') as f:
            json.dump(self.to_json(), f)

    def to_json(self):
        return {
            'frame_records': self.frame_records,
            'start_time': self.start_time,
            'duration': self.duration,
            'sample_count': self.sample_count,
            'start_call_stack': self.start_call_stack,
            'program': self.program,
            'cpu_time': self.cpu_time,
        }

    @staticmethod
    def from_json(json_dict):
        return ProfilerSession(
            frame_records=json_dict['frame_records'],
            start_time=json_dict['start_time'],
            duration=json_dict['duration'],
            sample_count=json_dict['sample_count'],
            start_call_stack=json_dict['start_call_stack'],
            program=json_dict['program'],
            cpu_time=json_dict['cpu_time'],
        )

    def root_frame(self, trim_stem=True):
        ''' 
        Parses the internal frame records and returns a tree of Frame objects
        '''
        root_frame = None

        frame_stack = []

        for frame_tuple in self.frame_records:
            identifier_stack = frame_tuple[0]
            time = frame_tuple[1]

            # now we must create a stack of frame objects and assign this time to the leaf
            for stack_depth, frame_identifier in enumerate(identifier_stack):
                if stack_depth < len(frame_stack):
                    if frame_identifier != frame_stack[stack_depth].identifier:
                        # trim any frames after and including this one
                        del frame_stack[stack_depth:]

                if stack_depth >= len(frame_stack):
                    frame = Frame(frame_identifier)
                    frame_stack.append(frame)
                    
                    if stack_depth == 0:
                        # There should only be one root frame, as far as I know
                        assert root_frame is None, ASSERTION_MESSAGE
                        root_frame = frame
                    else:
                        parent = frame_stack[stack_depth-1]
                        parent.add_child(frame)

            # trim any extra frames
            del frame_stack[stack_depth+1:]  # pylint: disable=W0631

            # assign the time to the final frame
            frame_stack[-1].add_child(SelfTimeFrame(self_time=time))
        
        if root_frame is None:
            return None
        
        if trim_stem:
            root_frame = self._trim_stem(root_frame)
        
        return root_frame

    def _trim_stem(self, frame):
        # trim the start of the tree before any branches.
        # we also don't want to trim beyond the call to profiler.start()

        start_stack = deque(self.start_call_stack)
        if start_stack.popleft() != frame.identifier:
            # the frame doesn't match where the profiler was started. Don't trim.
            return frame

        while frame.self_time == 0 and len(frame.children) == 1:
            # check child matches the start_call_stack, otherwise stop descending
            if len(start_stack) == 0 or frame.children[0].identifier != start_stack.popleft():
                break

            frame = frame.children[0]

        frame.remove_from_parent()
        return frame
