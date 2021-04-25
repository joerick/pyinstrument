from __future__ import annotations
import io, json
from collections import deque
from typing import List, Tuple
from pyinstrument.frame import Frame, SelfTimeFrame

ASSERTION_MESSAGE = (
    "Please raise an issue at http://github.com/pyinstrument/issues and "
    "let me know how you caused this error!"
)

FrameRecordType = Tuple[List[str], float]


class ProfilerSession:
    def __init__(
        self,
        frame_records: list[FrameRecordType],
        start_time,
        duration,
        sample_count,
        start_call_stack,
        program,
        cpu_time=None,
    ):
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.program = program
        self.cpu_time = cpu_time

    @staticmethod
    def load(filename):
        with open(filename) as f:
            return ProfilerSession.from_json(json.load(f))

    def save(self, filename):
        with open(filename, "w") as f:
            json.dump(self.to_json(), f)

    def to_json(self):
        return {
            "frame_records": self.frame_records,
            "start_time": self.start_time,
            "duration": self.duration,
            "sample_count": self.sample_count,
            "start_call_stack": self.start_call_stack,
            "program": self.program,
            "cpu_time": self.cpu_time,
        }

    @staticmethod
    def from_json(json_dict):
        return ProfilerSession(
            frame_records=json_dict["frame_records"],
            start_time=json_dict["start_time"],
            duration=json_dict["duration"],
            sample_count=json_dict["sample_count"],
            start_call_stack=json_dict["start_call_stack"],
            program=json_dict["program"],
            cpu_time=json_dict["cpu_time"],
        )

    @staticmethod
    def combine(session1: ProfilerSession, session2: ProfilerSession):
        if session1.start_time > session2.start_time:
            # swap them around so that session1 is the first one
            session1, session2 = session2, session1

        return ProfilerSession(
            frame_records=session1.frame_records + session2.frame_records,
            start_time=session1.start_time,
            duration=session1.duration + session2.duration,
            sample_count=session1.sample_count + session2.sample_count,
            start_call_stack=session1.start_call_stack,
            program=session1.program,
            cpu_time=session1.cpu_time + session2.cpu_time,
        )

    def root_frame(self, trim_stem=True) -> Frame | None:
        """
        Parses the internal frame records and returns a tree of Frame objects
        """
        from pyinstrument.profiler import Profiler

        root_frame = None
        out_of_context_frame = Frame(Profiler.OUT_OF_CONTEXT_FRAME_IDENTIFIER)

        frame_stack = []

        for frame_tuple in self.frame_records:
            identifier_stack = frame_tuple[0]
            time = frame_tuple[1]

            if (
                len(identifier_stack) == 1
                and identifier_stack[0] == Profiler.OUT_OF_CONTEXT_FRAME_IDENTIFIER
            ):
                out_of_context_frame.add_child(SelfTimeFrame(self_time=time))
                continue

            stack_depth = 0

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
                        parent = frame_stack[stack_depth - 1]
                        parent.add_child(frame)

            # trim any extra frames
            del frame_stack[stack_depth + 1 :]

            # assign the time to the final frame
            frame_stack[-1].add_child(SelfTimeFrame(self_time=time))

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        if len(out_of_context_frame.children) > 0:
            # add a synthetic wrapper frame that contains both the root frame
            # and the out of context stuff
            new_root_frame = Frame(
                "Async context\x00\x000",
                children=[
                    root_frame,
                    out_of_context_frame,
                ],
            )
            root_frame = new_root_frame

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
