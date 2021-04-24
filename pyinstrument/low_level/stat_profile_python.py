import sys
import timeit
import types
from typing import Any, List

timer = timeit.default_timer


class PythonStatProfiler:
    await_stack: List[str]

    def __init__(self, target, interval, context_var):
        self.target = target
        self.interval = interval
        self.last_invocation = timer()
        self.context_var = context_var
        self.last_context_var_value = context_var.get() if context_var else None
        self.await_stack = []

    def profile(self, frame: types.FrameType, event: str, arg: Any):
        now = timer()

        if self.context_var:
            context_var_value = self.context_var.get()
            last_context_var_value = self.last_context_var_value

            if context_var_value is not last_context_var_value:
                context_change_frame = frame.f_back if event == 'call' else frame
                self.target(context_change_frame, 'context_changed', (context_var_value, last_context_var_value, self.await_stack))
                self.last_context_var_value = context_var_value

            # 0x80 == CO_COROUTINE (i.e. defined with 'async def')
            if event == 'return' and frame.f_code.co_flags & 0x80:
                self.await_stack.append("%s\x00%s\x00%i" % (
                    frame.f_code.co_name,
                    frame.f_code.co_filename,
                    frame.f_code.co_firstlineno,
                ))
            else:
                self.await_stack.clear()

        if now < self.last_invocation + self.interval:
            return

        self.last_invocation = now
        return self.target(frame, event, arg)


'''
A reimplementation of setstatprofile in Python, for prototyping/reference
purposes. Not used in normal execution.
'''
def setstatprofile(target, interval=0.001, context_var=None):
    if target:
        sys.setprofile(PythonStatProfiler(target, interval, context_var).profile)
    else:
        sys.setprofile(None)
