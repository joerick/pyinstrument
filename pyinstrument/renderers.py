# -*- coding: utf-8 -*-
import abc
import os
from . import six

class Renderer(object):
    preferred_recorder = ''

    def render(self, frame):
        ''' 
        Return a string that contains the rendered form of `frame`
        '''
        raise NotImplementedError()


class ConsoleRenderer(Renderer):
    preferred_recorder = 'time_aggregating'

    def __init__(self, unicode=False, color=False, **kwargs):
        self.unicode = unicode
        self.color = color
        super(ConsoleRenderer, self).__init__(**kwargs)

    def render(self, frame, indent=u'', child_indent=u''):
        colors = colors_enabled if self.color else colors_disabled
        time_str = '{:.3f}'.format(frame.time())

        if self.color:
            time_str = self._ansi_color_for_frame(frame) + time_str + colors.end

        result = u'{indent}{time_str} {function}  {c.faint}{code_position}{c.end}\n'.format(
            indent=indent,
            time_str=time_str,
            function=frame.function,
            code_position=frame.code_position_short,
            c=colors)

        children = [f for f in frame.children if f.proportion_of_total > 0.01]

        if children:
            last_child = children[-1]

        for child in children:
            if child is not last_child:
                c_indent = child_indent + (u'├─ ' if self.unicode else '|- ')
                cc_indent = child_indent + (u'│  ' if self.unicode else '|  ')
            else:
                c_indent = child_indent + (u'└─ ' if self.unicode else '`- ')
                cc_indent = child_indent + u'   '
            result += self.render(child, indent=c_indent, child_indent=cc_indent)

        return result

    def _ansi_color_for_frame(self, frame):
        colors = colors_enabled
        if frame.proportion_of_total > 0.6:
            return colors.red
        elif frame.proportion_of_total > 0.2:
            return colors.yellow
        elif frame.proportion_of_total > 0.05:
            return colors.green
        else:
            return colors.bright_green + colors.faint


class HTMLRenderer(Renderer):
    preferred_recorder = 'time_aggregating'

    def render(self, frame):
        resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources/')

        with open(os.path.join(resources_dir, 'style.css')) as f:
            css = f.read()

        with open(os.path.join(resources_dir, 'profile.js')) as f:
            js = f.read()

        with open(os.path.join(resources_dir, 'jquery-1.11.0.min.js')) as f:
            jquery_js = f.read()

        body = self.render_frame(frame)

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

    def render_frame(self, frame):
        start_collapsed = all(child.proportion_of_total < 0.1 for child in frame.children)

        extra_class = ''
        extra_class += 'collapse ' if start_collapsed else ''
        extra_class += 'no_children ' if not frame.children else ''
        extra_class += 'application ' if frame.is_application_code else ''

        result = '''<div class="frame {extra_class}" data-time="{time}" date-parent-time="{parent_proportion}">
            <div class="frame-info">
                <span class="time">{time:.3f}s</span>
                <span class="total-percent">{total_proportion:.1%}</span>
                <!--<span class="parent-percent">{parent_proportion:.1%}</span>-->
                <span class="function">{function}</span>
                <span class="code-position">{code_position}</span>
            </div>'''.format(
                time=frame.time(),
                function=frame.function,
                code_position=frame.code_position_short,
                parent_proportion=frame.proportion_of_parent,
                total_proportion=frame.proportion_of_total,
                extra_class=extra_class)

        result += '<div class="frame-children">'

        # add this filter to prevent the output file getting too large
        children = [f for f in frame.children if f.proportion_of_total > 0.005]

        for child in children:
            result += self.render_frame(child)

        result += '</div></div>'

        return result


class colors_enabled:
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    blue = '\033[34m'
    cyan = '\033[36m'
    bright_green = '\033[92m'

    bold = '\033[1m'
    faint = '\033[2m'

    end = '\033[0m'


class colors_disabled:
    def __getattr__(self, key):
        return ''

colors_disabled = colors_disabled()
