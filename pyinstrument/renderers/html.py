import os
from pyinstrument.renderers.base import Renderer
from pyinstrument import processors
try:
    from html import escape as html_escape
except ImportError:
    from cgi import escape as html_escape


class HTMLRenderer(Renderer):
    def render(self, session):
        frame = self.preprocess(session.root_frame())

        resources_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'html_resources/')

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
        children = frame.children
        start_collapsed = all(child.proportion_of_total < 0.1 for child in children)

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
                function=html_escape(frame.function),  # pylint: disable=W1505
                code_position=html_escape(frame.code_position_short),  # pylint: disable=W1505
                parent_proportion=frame.proportion_of_parent,
                total_proportion=frame.proportion_of_total,
                extra_class=extra_class)

        result += '<div class="frame-children">'

        # add this filter to prevent the output file getting too large
        children = [f for f in children if f.proportion_of_total > 0.005]

        for child in children:
            result += self.render_frame(child)

        result += '</div></div>'

        return result

    def default_processors(self):
        return processors.default_time_aggregate_processors()
