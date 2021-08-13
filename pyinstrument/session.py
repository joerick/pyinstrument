from __future__ import annotations

import json
from collections import deque
from typing import Any, List, Tuple, cast

from pyinstrument.frame import BaseFrame, DummyFrame, Frame, SelfTimeFrame
from pyinstrument.typing import PathOrStr

# pyright: strict


ASSERTION_MESSAGE = (
    "Please raise an issue at http://github.com/pyinstrument/issues and "
    "let me know how you caused this error!"
)

FrameRecordType = Tuple[List[str], float]


class Session:
    def __init__(
        self,
        frame_records: list[FrameRecordType],
        start_time: float,
        duration: float,
        sample_count: int,
        start_call_stack: list[str],
        program: str,
        cpu_time: float,
    ):
        """Session()

        Represents a profile session, contains the data collected during a profile session.

        :meta private:
        """
        self.frame_records = frame_records
        self.start_time = start_time
        self.duration = duration
        self.sample_count = sample_count
        self.start_call_stack = start_call_stack
        self.program = program
        self.cpu_time = cpu_time

    @staticmethod
    def load(filename: PathOrStr) -> Session:
        """
        Load a previously saved session from disk.

        :param filename: The path to load from.
        :rtype: Session
        """
        with open(filename) as f:
            return Session.from_json(json.load(f))

    def save(self, filename: PathOrStr) -> None:
        """
        Saves a Session object to disk, in a JSON format.

        :param filename: The path to save to. Using the ``.pyisession`` extension is recommended.
        """
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
    def from_json(json_dict: dict[str, Any]):
        return Session(
            frame_records=json_dict["frame_records"],
            start_time=json_dict["start_time"],
            duration=json_dict["duration"],
            sample_count=json_dict["sample_count"],
            start_call_stack=json_dict["start_call_stack"],
            program=json_dict["program"],
            cpu_time=json_dict["cpu_time"],
        )

    @staticmethod
    def combine(session1: Session, session2: Session) -> Session:
        """
        Combines two :class:`Session` objects.

        Sessions that are joined in this way probably shouldn't be interpreted
        as timelines, because the samples are simply concatenated. But
        aggregate views (the default) of this data will work.

        :rtype: Session
        """
        if session1.start_time > session2.start_time:
            # swap them around so that session1 is the first one
            session1, session2 = session2, session1

        return Session(
            frame_records=session1.frame_records + session2.frame_records,
            start_time=session1.start_time,
            duration=session1.duration + session2.duration,
            sample_count=session1.sample_count + session2.sample_count,
            start_call_stack=session1.start_call_stack,
            program=session1.program,
            cpu_time=session1.cpu_time + session2.cpu_time,
        )

    def root_frame(self, trim_stem: bool = True) -> BaseFrame | None:
        """
        Parses the internal frame records and returns a tree of :class:`Frame`
        objects. This object can be renderered using a :class:`Renderer`
        object.

        :rtype: A :class:`Frame` object, or None if the session is empty.
        """
        root_frame = None

        frame_stack: list[BaseFrame] = []

        for frame_tuple in self.frame_records:
            identifier_stack = frame_tuple[0]
            time = frame_tuple[1]

            stack_depth = 0

            # now we must create a stack of frame objects and assign this time to the leaf
            for stack_depth, frame_identifier in enumerate(identifier_stack):
                if stack_depth < len(frame_stack):
                    if frame_identifier != frame_stack[stack_depth].identifier:
                        # trim any frames after and including this one
                        del frame_stack[stack_depth:]

                if stack_depth >= len(frame_stack):
                    frame = BaseFrame.new_subclass_with_identifier(frame_identifier)
                    frame_stack.append(frame)

                    if stack_depth == 0:
                        # There should only be one root frame, as far as I know
                        assert root_frame is None, ASSERTION_MESSAGE
                        root_frame = frame
                    else:
                        parent = cast(Frame, frame_stack[stack_depth - 1])
                        parent.add_child(frame)

            # trim any extra frames
            del frame_stack[stack_depth + 1 :]

            # assign the time to the final frame in the stack
            final_frame = frame_stack[-1]
            if isinstance(final_frame, DummyFrame):
                final_frame.self_time += time
            elif isinstance(final_frame, Frame):
                final_frame.add_child(SelfTimeFrame(self_time=time))
            else:
                raise Exception("unknown frame type")

        if root_frame is None:
            return None

        if trim_stem:
            root_frame = self._trim_stem(root_frame)

        return root_frame

    def _trim_stem(self, frame: BaseFrame):
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
