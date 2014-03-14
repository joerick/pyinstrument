import sys
import os
import time
import inspect
from operator import attrgetter


class Frame(object):
    def __init__(self, description="", parent=None, time=None, children=None):
        self.description = description
        self.time = time or 0
        self.children = children or {}
        self.parent = parent

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

    def as_text(self, depth=0):
        result = '%s%.3f %s\n' % ('| ' * depth, self.time, self.description)

        for child in self.sorted_children():
            result += child.as_text(depth+1)

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


class Profiler(object):
    def __init__(self):
        self.stack_time = {}
        self.current_call_stack = []
        self.current_call_stack_start_times = []
        self.time_spent_in_profiler = 0

    def start(self):
        for frame_record in inspect.stack()[::-1]:
            # call the profile function as if we just entered all the frames on the stack
            self(frame_record[0], 'call', None)

        sys.setprofile(self)

    def stop(self):
        sys.setprofile(None)

        while len(self.current_call_stack) > 0:
            # call the profile function as if we just left all the frames on the stack
            self(None, 'return', None)

    def __call__(self, frame, event, arg):
        method_start = time.clock()

        if event == 'call':
            self.current_call_stack.append(self._identifier_for_frame(frame))
            self.current_call_stack_start_times.append(method_start - self.time_spent_in_profiler)
        elif event == 'return':
            stack = tuple(self.current_call_stack)
            frame_start = self.current_call_stack_start_times.pop()
            self.current_call_stack.pop()
            self.stack_time[stack] = self.stack_time.get(stack, 0) + method_start - frame_start - self.time_spent_in_profiler

        self.time_spent_in_profiler += time.clock() - method_start

    def root_frame(self):
        if not hasattr(self, '_root_frame'):
            self._root_frame = Frame()

            def frame_for_stack(stack):
                if len(stack) == 0:
                    return self._root_frame
                parent = frame_for_stack(stack[:-1])
                frame_name = stack[-1]

                parent.children[frame_name] = parent.children.get(frame_name, Frame(frame_name, parent))
                return parent.children[frame_name]

            for stack_frame in self.stack_time.iteritems():
                frame_for_stack(stack_frame[0]).time = stack_frame[1]

            # fix up root_frames's time so Frame's proportion_of_total works correctly
            for child_frame in self._root_frame.children.values():
                self._root_frame.time += child_frame.time

        return self._root_frame

    def _identifier_for_frame(self, frame):
        return '%s\t%s:%i' % (frame.f_code.co_name, frame.f_code.co_filename, frame.f_lineno)

    def output_text(self):
        return self.root_frame().as_text()

    def output_html(self):
        return self.root_frame().as_html()
