from pyinstrument import Profiler
from pyinstrument.renderers import HTMLRenderer
import time

def sleepyRender_html():
    profiler = Profiler()
    profiler.start()
    time.sleep(1.5)
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = profiler.output(renderer=renderer)
    save_html_report(html_output)

def save_html_report(html_content):
    # This could save to disk or a DB
    pass
