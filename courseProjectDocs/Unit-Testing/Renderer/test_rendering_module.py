from unittest.mock import patch
import renderer_module

def test_save_html_called_once():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        assert mock_save.call_count == 1

def test_saved_content_is_html():
    with patch('renderer_module.save_html_report') as mock_save:
        renderer_module.sleepyRender_html()
        args, _ = mock_save.call_args
        html_output = args[0]
        assert "<html" in html_output.lower()
