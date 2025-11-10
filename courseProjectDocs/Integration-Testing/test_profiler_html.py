import pytest
from pyinstrument import Profiler
from pyinstrument.renderers.html import HTMLRenderer

def test_profiler_and_html_renderer_interaction():
    profiler = Profiler()

    def quick_task():
        total = 0
        for i in range(200):
            total += i
        return total

    profiler.start()
    profiler.stop()

    renderer = HTMLRenderer()
    html_output = renderer.render(profiler.last_session)

    assert isinstance(html_output, str)
    assert "<html" in html_output
    assert "quick_task" in html_output or "pyinstrument" in html_output

if __name__ == "__main__":
    pytest.main([__file__])
