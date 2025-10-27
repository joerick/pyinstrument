from unittest.mock import patch, MagicMock
import profile_module

def test_save_profile_called_once():
    with patch("profile_module.save_profile_to_db") as mock_save:
        profile_module.run_and_save_profile()
        assert mock_save.call_count == 1

def test_save_profile_called_with_string():
    with patch("profile_module.save_profile_to_db") as mock_save:
        profile_module.run_and_save_profile()
        args, _ = mock_save.call_args
        assert isinstance(args[0], str)

def test_profiler_methods_called():
    with patch("profile_module.Profiler") as MockProfiler:
        mock_instance = MagicMock()
        MockProfiler.return_value = mock_instance
        mock_instance.output_text.return_value = "Mocked profiling report"

        report = profile_module.run_profiler_and_report()

        mock_instance.start.assert_called_once()
        mock_instance.stop.assert_called_once()
        mock_instance.output_text.assert_called_once_with(unicode=True, color=False)
        assert report == "Mocked profiling report"

def test_run_heavy_task_completes():
    result = profile_module.run_heavy_task()
    assert result > 0
    assert isinstance(result, int)