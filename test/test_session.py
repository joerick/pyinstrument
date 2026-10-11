import pytest

from pyinstrument.session import Session


@pytest.mark.parametrize(
    "durations, expected_indices, expected_durations",
    [
        ([0.006] * 4, [1, 3], [0.012, 0.012]),
        ([0.006] * 5, [1, 3, 4], [0.012, 0.012, 0.006]),
        ([0.002, 0.007, 0.003, 0.004, 0.009], [2, 4], [0.012, 0.013]),
        ([0.009, 0.004, 0.006], [1, 2], [0.013, 0.006]),
        ([0.004, 0.002], [1], [0.006]),
        ([0.015, 0.002], [0, 1], [0.015, 0.002]),
        ([0.01] * 3, [0, 1, 2], [0.01] * 3),
        ([], [], []),
    ],
)
def test_resample_preserves_recorded_time(durations, expected_indices, expected_durations):
    frame_records = [
        (["root\x00example.py\x001", f"sample{index}\x00example.py\x002"], duration)
        for index, duration in enumerate(durations)
    ]
    session = Session(
        frame_records=frame_records,
        start_time=123,
        duration=sum(durations),
        min_interval=0.001,
        max_interval=0.015,
        sample_count=len(frame_records),
        start_call_stack=[],
        target_description="resampling test",
        cpu_time=sum(durations),
        sys_path=[],
        sys_prefixes=[],
    )

    resampled = session.resample(0.01)

    assert [stack for stack, _ in resampled.frame_records] == [
        frame_records[index][0] for index in expected_indices
    ]
    assert [duration for _, duration in resampled.frame_records] == pytest.approx(
        expected_durations
    )
    assert sum(duration for _, duration in resampled.frame_records) == pytest.approx(sum(durations))
    assert resampled.sample_count == len(expected_indices)
    assert resampled.duration == session.duration
    assert resampled.cpu_time == session.cpu_time
    assert resampled.min_interval == resampled.max_interval == 0.01
    assert session.frame_records == frame_records
    assert [duration for _, duration in frame_records] == durations

    root = resampled.root_frame()
    if durations:
        assert root is not None
        assert root.time == pytest.approx(sum(durations))
    else:
        assert root is None
