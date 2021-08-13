from __future__ import annotations

import os
import sys
import uuid
from typing import Sequence

# pyright: strict


class BaseFrame:
    group: FrameGroup | None

    def __init__(self, parent: Frame | None = None, self_time: float = 0):
        self.parent = parent
        self._self_time = self_time
        self.group = None

    def remove_from_parent(self):
        """
        Removes this frame from its parent, and nulls the parent link
        """
        if self.parent:
            self.parent._children.remove(self)  # type: ignore
            self.parent._invalidate_time_caches()  # type: ignore
            self.parent = None

    @staticmethod
    def new_subclass_with_identifier(identifier: str) -> BaseFrame:
        if identifier == AWAIT_FRAME_IDENTIFIER:
            return AwaitTimeFrame()
        elif identifier == OUT_OF_CONTEXT_FRAME_IDENTIFIER:
            return OutOfContextFrame()
        else:
            return Frame(identifier=identifier)

    @property
    def proportion_of_parent(self) -> float:
        if self.parent:
            try:
                return self.time() / self.parent.time()
            except ZeroDivisionError:
                return float("nan")
        else:
            return 1.0

    @property
    def total_self_time(self) -> float:
        """
        The total amount of self time in this frame (including self time recorded by SelfTimeFrame
        children, and await time from AwaitTimeFrame children)
        """
        self_time = self.self_time
        for child in self.children:
            if isinstance(child, SelfTimeFrame) or isinstance(child, AwaitTimeFrame):
                self_time += child.self_time
        return self_time

    @property
    def self_time(self) -> float:
        return self._self_time

    @self_time.setter
    def self_time(self, self_time: float):
        self._self_time = self_time
        self._invalidate_time_caches()

    # invalidates the cache for the time() function.
    # called whenever self_time or _children is modified.
    def _invalidate_time_caches(self):
        pass

    # stylistically I'd rather this was a property, but using @property appears to use twice
    # as many stack frames, so I'm forced into using a function since this method is recursive
    # down the call tree.
    def time(self) -> float:
        """
        Wall-clock time spent in the function. Includes time spent in 'await',
        if applicable.
        """
        raise NotImplementedError()

    def await_time(self) -> float:
        raise NotImplementedError()

    @property
    def identifier(self) -> str:
        raise NotImplementedError()

    @property
    def function(self) -> str | None:
        raise NotImplementedError()

    @property
    def file_path(self) -> str | None:
        raise NotImplementedError()

    @property
    def line_no(self) -> int | None:
        raise NotImplementedError()

    @property
    def file_path_short(self) -> str | None:
        raise NotImplementedError()

    @property
    def is_application_code(self) -> bool | None:
        raise NotImplementedError()

    @property
    def code_position_short(self) -> str | None:
        raise NotImplementedError()

    @property
    def children(self) -> Sequence[BaseFrame]:
        raise NotImplementedError()


class Frame(BaseFrame):
    """
    Object that represents a stack frame in the parsed tree
    """

    _children: list[BaseFrame]
    _time: float | None
    _await_time: float | None
    _identifier: str

    def __init__(
        self,
        identifier: str = "",
        parent: Frame | None = None,
        children: Sequence[BaseFrame] | None = None,
        self_time: float = 0,
    ):
        super().__init__(parent=parent, self_time=self_time)

        self._identifier = identifier
        self._children = []

        self._time = None
        self._await_time = None

        if children:
            for child in children:
                self.add_child(child)

    def add_child(self, frame: BaseFrame, after: BaseFrame | None = None):
        """
        Adds a child frame, updating the parent link.
        Optionally, insert the frame in a specific position by passing the frame to insert
        this one after.
        """
        frame.remove_from_parent()
        frame.parent = self
        if after is None:
            self._children.append(frame)
        else:
            index = self._children.index(after) + 1
            self._children.insert(index, frame)

        self._invalidate_time_caches()

    def add_children(self, frames: Sequence[BaseFrame], after: BaseFrame | None = None):
        """
        Convenience method to add multiple frames at once.
        """
        if after is not None:
            # if there's an 'after' parameter, add the frames in reverse so the order is
            # preserved.
            for frame in reversed(frames):
                self.add_child(frame, after=after)
        else:
            for frame in frames:
                self.add_child(frame)

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def children(self) -> Sequence[BaseFrame]:
        # Return an immutable copy (this property should only be mutated using methods)
        # Also, returning a copy avoid problems when mutating while iterating, which happens a lot
        # in processors!
        return tuple(self._children)

    @property
    def function(self) -> str | None:
        if self.identifier:
            return self.identifier.split("\x00")[0]

    @property
    def file_path(self) -> str | None:
        if self.identifier:
            return self.identifier.split("\x00")[1]

    @property
    def line_no(self) -> int | None:
        if self.identifier:
            return int(self.identifier.split("\x00")[2])

    @property
    def file_path_short(self) -> str | None:
        """Return the path resolved against the closest entry in sys.path"""
        if not hasattr(self, "_file_path_short"):
            if self.file_path:
                result = None

                for path in sys.path:
                    # On Windows, if self.file_path and path are on different drives, relpath
                    # will result in exception, because it cannot compute a relpath in this case.
                    # The root cause is that on Windows, there is no root dir like '/' on Linux.
                    try:
                        candidate = os.path.relpath(self.file_path, path)
                    except ValueError:
                        continue

                    if not result or (len(candidate.split(os.sep)) < len(result.split(os.sep))):
                        result = candidate

                self._file_path_short = result
            else:
                self._file_path_short = None

        return self._file_path_short

    @property
    def is_application_code(self) -> bool | None:
        if self.identifier:
            file_path = self.file_path

            if not file_path:
                return False

            if "/lib/" in file_path:
                return False

            if os.sep != "/":
                # windows uses back-slash too, so let's look for that too.
                if (f"{os.sep}lib{os.sep}") in file_path:
                    return False

            if file_path.startswith("<"):
                if file_path.startswith("<ipython-input-"):
                    # lines typed at a console or in a notebook are app code
                    return True
                else:
                    # otherwise, this is probably some library-internal code gen
                    return False

            return True

    @property
    def code_position_short(self) -> str | None:
        if self.identifier:
            return "%s:%i" % (self.file_path_short, self.line_no)

    def time(self):
        if self._time is None:
            # can't use a sum(<generator>) expression here sadly, because this method
            # recurses down the call tree, and the generator uses an extra stack frame,
            # meaning we hit the stack limit when the profiled code is 500 frames deep.
            self._time = self.self_time

            for child in self.children:
                self._time += child.time()

        return self._time

    def await_time(self):
        if self._await_time is None:
            await_time = 0

            for child in self.children:
                await_time += child.await_time()

            self._await_time = await_time

        return self._await_time

    # pylint: disable=W0212
    def _invalidate_time_caches(self):
        self._time = None
        self._await_time = None
        # null all the parent's caches also.
        frame = self
        while frame.parent is not None:
            frame = frame.parent
            frame._time = None
            frame._await_time = None

    def __repr__(self):
        return "Frame(identifier=%s, time=%f, len(children)=%d), group=%r" % (
            self.identifier,
            self.time(),
            len(self.children),
            self.group,
        )


class DummyFrame(BaseFrame):
    """
    Informational frame that doesn't represent a real Python frame, but
    represents something about how time was spent in a function
    """

    @property
    def _children(self) -> list[BaseFrame]:
        return []

    @property
    def children(self) -> list[BaseFrame]:
        return []

    @property
    def file_path(self):
        if self.parent:
            return self.parent.file_path

    @property
    def line_no(self):
        if self.parent:
            return self.parent.line_no

    @property
    def file_path_short(self):
        return ""

    @property
    def is_application_code(self):
        return False

    @property
    def code_position_short(self):
        return ""


class SelfTimeFrame(DummyFrame):
    """
    Represents a time spent inside a function
    """

    def time(self):
        return self.self_time

    def await_time(self):
        return 0

    @property
    def function(self):
        return "[self]"

    @property
    def identifier(self):
        return "[self]"


class AwaitTimeFrame(DummyFrame):
    """
    Represents a time spent in an await - waiting for a coroutine to
    reactivate
    """

    def time(self):
        return self.self_time

    def await_time(self):
        return self.self_time

    @property
    def function(self):
        return "[await]"

    @property
    def identifier(self):
        return "[await]"


AWAIT_FRAME_IDENTIFIER = "[await]\x00<await>\x000"


class OutOfContextFrame(DummyFrame):
    """
    Represents a time spent out of the profiler's context.
    """

    def time(self):
        return self.self_time

    @property
    def function(self):
        return "[out-of-context]"

    @property
    def identifier(self):
        return "[out-of-context]"


OUT_OF_CONTEXT_FRAME_IDENTIFIER = "[out-of-context]\x00<out-of-context>\x000"


class FrameGroup:
    _libraries: list[str] | None
    _frames: list[BaseFrame]
    _exit_frames: list[BaseFrame] | None

    def __init__(self, root: BaseFrame):
        self.root = root
        self.id = str(uuid.uuid4())
        self._frames = []
        self._exit_frames = None
        self._libraries = None

        self.add_frame(root)

    @property
    def libraries(self) -> list[str]:
        if self._libraries is None:
            libraries: list[str] = []

            for frame in self.frames:
                if frame.file_path_short:
                    library = frame.file_path_short.split(os.sep)[0]
                    library, _ = os.path.splitext(library)
                    if library and library not in libraries:
                        libraries.append(library)
            self._libraries = libraries

        return self._libraries

    @property
    def frames(self) -> Sequence[BaseFrame]:
        return tuple(self._frames)

    # pylint: disable=W0212
    def add_frame(self, frame: BaseFrame):
        if frame.group:
            frame.group._frames.remove(frame)

        self._frames.append(frame)
        frame.group = self

    @property
    def exit_frames(self):
        """
        Returns a list of frames whose children include a frame outside of the group
        """
        if self._exit_frames is None:
            exit_frames: list[BaseFrame] = []
            for frame in self.frames:
                if any(c.group != self for c in frame.children):
                    exit_frames.append(frame)
            self._exit_frames = exit_frames

        return self._exit_frames

    def __repr__(self):
        return "FrameGroup(len(frames)=%d)" % len(self.frames)
