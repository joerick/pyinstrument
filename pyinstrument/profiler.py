# -*- coding: utf-8 -*-
import sys
import os
import timeit
import signal
from collections import deque
from operator import attrgetter

timer = timeit.default_timer


class NotMainThreadError(Exception):
    """pyinstrument.StatProfiler must be used on the main thread"""
    def __init__(self, message=''):
        super(NotMainThreadError, self).__init__(message or NotMainThreadError.__doc__)


class SignalUnavailableError(Exception):
    '''pyinstrument.StatProfiler uses signal.SIGALRM, which is not available on your system.'''
    def __init__(self, message=''):
        super(SignalUnavailableError, self).__init__(message or SignalUnavailableError.__doc__)


class Profiler(object):
    def __init__(self, *args, **kwargs):
        try:
            signal.SIGALRM
        except AttributeError:
            raise SignalUnavailableError()

        self.next_profile_time = 0
        self.interval = 0.001
        self.last_signal_time = 0
        self.stack_self_time = {}

    def start(self):
        try:
            signal.signal(signal.SIGALRM, self.signal)
        except ValueError:
            raise NotMainThreadError()

        signal.setitimer(signal.ITIMER_REAL, self.interval, 0.0)
        self.last_signal_time = timer()

    def stop(self):
        signal.setitimer(signal.ITIMER_REAL, 0.0, 0.0)

        try:
            signal.signal(signal.SIGALRM, signal.SIG_IGN)
        except ValueError:
            raise NotMainThreadError()

    def signal(self, signum, frame):
        now = timer()
        time_since_last_signal = now - self.last_signal_time

        stack = self._call_stack_for_frame(frame)
        self.stack_self_time[stack] = self.stack_self_time.get(stack, 0) + time_since_last_signal

        signal.setitimer(signal.ITIMER_REAL, self.interval, 0.0)
        self.last_signal_time = now

    def _call_stack_for_frame(self, frame):
        result_list = deque()

        while frame is not None:
            result_list.appendleft(self._identifier_for_frame(frame))
            frame = frame.f_back

        return tuple(result_list)

    def root_frame(self):
        """
        Returns the parsed results in the form of a tree of Frame objects
        """
        if not hasattr(self, '_root_frame'):
            self._root_frame = Frame()

            # define a recursive function that builds the heirarchy of frames given the
            # stack of frame identifiers
            def frame_for_stack(stack):
                if len(stack) == 0:
                    return self._root_frame

                parent = frame_for_stack(stack[:-1])
                frame_name = stack[-1]

                if not frame_name in parent.children:
                    parent.children[frame_name] = Frame(frame_name, parent)

                return parent.children[frame_name]

            for stack, self_time in self.stack_self_time.iteritems():
                frame_for_stack(stack).self_time = self_time

        return self._root_frame

    def _identifier_for_frame(self, frame):
        return '%s\t%s:%i' % (frame.f_code.co_name, frame.f_code.co_filename, frame.f_code.co_firstlineno)

    def first_interesting_frame(self):
        """ 
        Traverse down the frame heirarchy until a frame is found with more than one child
        """
        frame = self.root_frame()

        while len(frame.children.values()) <= 1:
            frame = frame.children.values()[0]

        return frame

    def starting_frame(self, root=False):
        if root:
            return self.root_frame()
        else:
            return self.first_interesting_frame()

    def output_text(self, root=False, unicode=False):
        return self.starting_frame(root=root).as_text(unicode=unicode)

    def output_html(self, root=False):
        resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/')

        with open(os.path.join(resources_dir, 'style.css')) as f:
            css = f.read()

        with open(os.path.join(resources_dir, 'profile.js')) as f:
            js = f.read()

        with open(os.path.join(resources_dir, 'jquery-1.11.0.min.js')) as f:
            jquery_js = f.read()

        body = self.starting_frame(root).as_html()

        page = '''
            <html>
            <head>
                <style>{css}</style>
                <script>{jquery_js}</script>
            </head>
            <body>
                {body}
                <script>{js}</script>
            </body>
            </html>'''.format(css=css, js=js, jquery_js=jquery_js, body=body)

        return page


class Frame(object):
    """
    Object that represents a stack frame in the parsed tree
    """
    def __init__(self, description="", parent=None):
        self.description = description
        self.parent = parent
        self.children = {}
        self.self_time = 0

    def function(self):
        if self.description:
            return self.description.split('\t')[0]

    def code_position(self):
        if self.description:
            return self.description.split('\t')[1]

    def file_path(self):
        if self.description:
            return self.code_position().split(':')[0]

    def line_no(self):
        if self.description:
            return int(self.code_position().split(':')[1])

    def file_path_short(self):
        """ Return the path resolved against the closest entry in sys.path """
        file_path = self.file_path()

        if not file_path:
            return None

        result = None

        for path in sys.path:
            candidate = os.path.relpath(file_path, path)
            if not result or (len(candidate.split('/')) < len(result.split('/'))):
                result = candidate

        return result

    def code_position_short(self):
        if self.description:
            return '%s:%i' % (self.file_path_short(), self.line_no())

    def __repr__(self):
        return 'Frame(description=%s, time=%f, children=%r)' % (self.description, self.time, self.children)

    @property
    def time(self):
        if not hasattr(self, '_time'):
            self._time = sum(child.time for child in self.children.values()) + self.self_time
        return self._time

    def proportion_of_parent(self):
        if self.parent and self.time:
            try:
                return self.time / self.parent.time
            except ZeroDivisionError:
                return float('nan')
        else:
            return 1.0

    def proportion_of_total(self):
        if not hasattr(self, '_proportion_of_total'):
            if not self.parent:
                return 1.0

            self._proportion_of_total = self.parent.proportion_of_total() * self.proportion_of_parent()

        return self._proportion_of_total

    def sorted_children(self):
        return sorted(self.children.values(), key=attrgetter('time'), reverse=True)

    def as_text(self, indent=u'', child_indent=u'', unicode=False):
        result = u'%s%.3f %s \t%s\n' % (indent, self.time, self.function(), self.code_position_short())

        sorted_children = self.sorted_children()
        last_child = sorted_children[-1] if sorted_children else None

        for child in sorted_children:
            if child is not last_child:
                c_indent = child_indent + (u'├─ ' if unicode else '|- ')
                cc_indent = child_indent + (u'│  ' if unicode else '|  ')
            else:
                c_indent = child_indent + (u'└─ ' if unicode else '`- ')
                cc_indent = child_indent + u'   '
            result += child.as_text(indent=c_indent, child_indent=cc_indent, unicode=unicode)

        return result

    def as_html(self):
        parent_proportion = self.proportion_of_parent()
        total_proportion = self.proportion_of_total()
        start_collapsed = True;
        sorted_children = self.sorted_children()
        has_children = len(sorted_children) > 0

        for child in sorted_children:
            if child.proportion_of_total() > 0.1:
                start_collapsed = False

        extra_class = ''
        extra_class += 'collapse ' if start_collapsed else ''
        extra_class += 'no_children ' if not has_children else ''

        result = '''<div class="frame {extra_class}" data-time="{time}" date-parent-time="{parent_time}">
            <div class="frame-info">
                <span class="time">{time:.3f}s</span>
                <span class="total-percent">{total_percent:.1f}%</span>
                <!--<span class="parent-percent">{parent_percent:.1f}%</span>-->
                <span class="function">{function}</span>
                <span class="code-position">{code_position}</span>
            </div>'''.format(
                time=self.time,
                function=self.function(),
                code_position=self.code_position_short(),
                parent_time=parent_proportion, 
                parent_percent=parent_proportion * 100,
                total_percent=total_proportion * 100,
                extra_class=extra_class)

        result += '<div class="frame-children">'

        for child in sorted_children:
            result += child.as_html()

        result += '</div></div>'

        return result
