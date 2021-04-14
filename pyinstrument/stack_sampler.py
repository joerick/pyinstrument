import threading
import timeit
import types
from typing import Any, Callable, List, NamedTuple, Optional, Union

from pyinstrument_cext import setstatprofile

thread_locals = threading.local()
timer = timeit.default_timer


class StackSamplerSubscriber(NamedTuple):
    target: Callable[[List[str], float], None]
    desired_interval: float


class StackSampler:
    """ Manages setstatprofile for Profilers on a single thread """

    subscribers: List[StackSamplerSubscriber]
    current_sampling_interval: Optional[float]
    last_profile_time: float

    def __init__(self) -> None:
        self.subscribers = []
        self.current_sampling_interval = None
        self.last_profile_time = 0.0

    def subscribe(self, target, desired_interval):
        self.subscribers.append(
            StackSamplerSubscriber(target=target, desired_interval=desired_interval)
        )
        self._update()

    def unsubscribe(self, target):
        print(self.subscribers)
        self.subscribers = [s for s in self.subscribers if s.target != target]
        print(self.subscribers)
        self._update()

    def _update(self):
        if len(self.subscribers) == 0:
            self._stop_sampling()
            return

        min_subscribers_interval = min(s.desired_interval for s in self.subscribers)

        if self.current_sampling_interval != min_subscribers_interval:
            self._start_sampling(interval=min_subscribers_interval)

    def _start_sampling(self, interval):
        self.current_sampling_interval = interval
        if self.last_profile_time == 0.0:
            self.last_profile_time = timer()
        setstatprofile(self._sample, interval)

    def _stop_sampling(self):
        setstatprofile(None)
        self.current_sampling_interval = None
        self.last_profile_time = 0.0

    def _sample(self, frame, event, arg):
        now = timer()
        time_since_last_sample = now - self.last_profile_time

        call_stack = build_call_stack(frame, event, arg)

        for subscriber in self.subscribers:
            subscriber.target(call_stack, time_since_last_sample)

        self.last_profile_time = now


def get_stack_sampler() -> StackSampler:
    """
    Gets the stack sampler for the current thread, creating it if necessary
    """
    if not hasattr(thread_locals, "stack_sampler"):
        thread_locals.stack_sampler = StackSampler()
    return thread_locals.stack_sampler


def build_call_stack(
    frame: Union[types.FrameType, None], event: str, arg: Any
) -> List[str]:
    call_stack = []

    if event == "call":
        # if we're entering a function, the time should be attributed to
        # the caller
        frame = frame.f_back
    elif event == "c_return" or event == "c_exception":
        # if we're exiting a C function, we should add a frame before
        # any Python frames that attributes the time to that C function
        c_frame_identifier = "%s\x00%s\x00%i" % (
            getattr(arg, "__qualname__", arg.__name__),
            "<built-in>",
            0,
        )
        call_stack.append(c_frame_identifier)

    while frame is not None:
        identifier = "%s\x00%s\x00%i" % (
            frame.f_code.co_name,
            frame.f_code.co_filename,
            frame.f_code.co_firstlineno,
        )
        call_stack.append(identifier)
        frame = frame.f_back

    thread = threading.current_thread()
    thread_identifier = "%s\x00%s\x00%i" % (thread.name, "<thread>", thread.ident)
    call_stack.append(thread_identifier)

    # we iterated from the leaf to the root, we actually want the call stack
    # starting at the root, so reverse this array
    call_stack.reverse()

    return call_stack
