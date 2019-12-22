# coding: utf8
import time
import pyinstrument
from pyinstrument.renderers.base import Renderer
from pyinstrument.util import truncate
from pyinstrument import processors


class ConsoleRenderer(Renderer):
    def __init__(self, unicode=False, color=False, **kwargs):
        super(ConsoleRenderer, self).__init__(**kwargs)

        self.unicode = unicode
        self.color = color
        self.colors = self.colors_enabled if color else self.colors_disabled

    def render(self, session):
        result = self.render_preamble(session)

        self.root_frame = self.preprocess(session.root_frame())

        if self.root_frame is None:
            result += 'No samples were recorded.\n\n'
            return result

        result += self.render_frame(self.root_frame)
        result += '\n'

        return result

    # pylint: disable=W1401
    def render_preamble(self, session):
        lines = [
            r"",
            r"  _     ._   __/__   _ _  _  _ _/_  ",
            r" /_//_/// /_\ / //_// / //_'/ //    ",
            r"/   _/        {:>20}".format('v'+pyinstrument.__version__),
        ]

        lines[1] += " Recorded: {:<9}".format(time.strftime('%X', time.localtime(session.start_time)))
        lines[2] += " Duration: {:<9.3f}".format(session.duration)
        lines[1] += " Samples:  {}".format(session.sample_count)
        if session.cpu_time is not None:
            lines[2] += " CPU time: {:.3f}".format(session.cpu_time)

        lines.append('')
        lines.append('Program: %s' % session.program)
        lines.append('')
        lines.append('')

        return '\n'.join(lines)

    def render_frame(self, frame, indent=u'', child_indent=u''):
        if not frame.group or (frame.group.root == frame
                               or frame.total_self_time > 0.2*self.root_frame.time()
                               or frame in frame.group.exit_frames):
            time_str = (self._ansi_color_for_time(frame)
                        + '{:.3f}'.format(frame.time()) 
                        + self.colors.end)
            function_color = self._ansi_color_for_function(frame)
            result = u'{indent}{time_str} {function_color}{function}{c.end}  {c.faint}{code_position}{c.end}\n'.format(
                indent=indent,
                time_str=time_str,
                function_color=function_color,
                function=frame.function,
                code_position=frame.code_position_short,
                c=self.colors)
            if self.unicode:
                indents = {'├': u'├─ ', '│': u'│  ', '└': u'└─ ', ' ': u'   '}
            else:
                indents = {'├': u'|- ', '│': u'|  ', '└': u'`- ', ' ': u'   '}

            if frame.group and frame.group.root == frame:
                result += u'{indent}[{count} frames hidden]  {c.faint}{libraries}{c.end}\n'.format(
                    indent=child_indent+u'   ',
                    count=len(frame.group.frames),
                    libraries=truncate(', '.join(frame.group.libraries), 40),
                    c=self.colors)
                for key in indents:
                    indents[key] = u'      '
        else:
            result = ''
            indents = {'├': u'', '│': u'', '└': u'', ' ': u''}

        if frame.children:
            last_child = frame.children[-1]

        for child in frame.children:
            if child is not last_child:
                c_indent = child_indent + indents['├']
                cc_indent = child_indent + indents['│']
            else:
                c_indent = child_indent + indents['└']
                cc_indent = child_indent + indents[' ']
            result += self.render_frame(child, indent=c_indent, child_indent=cc_indent)

        return result

    def _ansi_color_for_time(self, frame):
        proportion_of_total = frame.time() / self.root_frame.time()
        
        if proportion_of_total > 0.6:
            return self.colors.red
        elif proportion_of_total > 0.2:
            return self.colors.yellow
        elif proportion_of_total > 0.05:
            return self.colors.green
        else:
            return self.colors.bright_green + self.colors.faint

    def _ansi_color_for_function(self, frame):
        if frame.is_application_code:
            return self.colors.bg_dark_blue_255+self.colors.white_255
        else:
            return ''

    def default_processors(self):
        return [
            processors.remove_importlib,
            processors.merge_consecutive_self_time,
            processors.aggregate_repeated_calls,
            processors.group_library_frames_processor,
            processors.remove_unnecessary_self_time_nodes,
            processors.remove_irrelevant_nodes,
        ]
     
    class colors_enabled:
        red = '\033[31m'
        green = '\033[32m'
        yellow = '\033[33m'
        blue = '\033[34m'
        cyan = '\033[36m'
        bright_green = '\033[92m'
        white = '\033[37m\033[97m'

        bg_dark_blue_255 = '\033[48;5;24m'
        white_255 = '\033[38;5;15m'

        bold = '\033[1m'
        faint = '\033[2m'

        end = '\033[0m'


    class colors_disabled:
        def __getattr__(self, key):
            return ''

    colors_disabled = colors_disabled()
