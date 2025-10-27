def test_context_change_frame_handling():
    profiler = PythonStatProfiler()

    mock_frame = MagicMock()
    mock_frame.f_back = "back_frame"

    context_var_value = ...
    event = "call"
    context_change_frame = mock_frame.f_back if event == "call" else mock_frame
    assert context_change_frame == "back_frame"

    event = "CALL"
    context_change_frame = mock_frame.f_back if event == "call" else mock_frame
    assert context_change_frame == mock_frame
