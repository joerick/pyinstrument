from pyinstrument import Profiler
from pyinstrument.renderers import HTMLRenderer

def run_and_render_html():
    profiler = Profiler()
    profiler.start()
    sum(range(1000))
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = profiler.output(renderer=renderer)
    save_html_report(html_output)

def save_html_report(html_content):
    # This could save to disk or a DB
    pass
