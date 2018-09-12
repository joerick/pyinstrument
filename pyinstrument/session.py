import io, json
from pyinstrument.frame import Frame

class ProfilerSession(object):
    def __init__(self, frame_records, start_time, duration, sample_count, program, cpu_time=None):
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.sample_count = sample_count
        self.program = program
        self.cpu_time = cpu_time

    @staticmethod
    def load(filename):
        with io.open(filename, 'r') as f:
            return ProfilerSession.from_json(json.load(f))

    def save(self, filename):
        with io.open(filename, 'w') as f:
            json.dump(self.to_json(), f)

    def to_json(self):
        return {
            'frame_records': self.frame_records,
            'start_time': self.start_time,
            'duration': self.duration,
            'sample_count': self.sample_count,
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
            program=json_dict['program'],
            cpu_time=json_dict['cpu_time'],
        )

    def root_frame(self):
        ''' 
        Parses the internal frame records and returns a tree of Frame objects
        '''
        root_frame = Frame()

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
                    if stack_depth == 0:
                        parent = root_frame
                    else:
                        parent = frame_stack[stack_depth-1]

                    frame = Frame(frame_identifier)
                    parent.add_child(frame)
                    frame_stack.append(frame)

            # trim any extra frames
            del frame_stack[stack_depth+1:]

            # assign the time to the final frame
            frame_stack[-1].self_time += time

        return root_frame
