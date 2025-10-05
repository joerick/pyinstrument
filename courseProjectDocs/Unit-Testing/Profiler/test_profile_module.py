from unittest.mock import patch
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
