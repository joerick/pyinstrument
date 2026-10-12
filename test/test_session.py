import itertools
import math

import pytest

from pyinstrument.session import Session


@pytest.mark.parametrize(
    "durations, expected_indices, expected_durations",
    [
        ([0.006] * 4, [1, 3], [0.01, 0.01]),
        ([0.006] * 5, [1, 3, 4], [0.01] * 3),
        ([0.002, 0.007, 0.003, 0.004, 0.009], [2, 4], [0.01, 0.01]),
        ([0.009, 0.004, 0.006], [1], [0.01]),
        ([0.004, 0.002], [], []),
        ([0.015, 0.002], [0], [0.01]),
        ([0.035, 0.006], [0, 1], [0.03, 0.01]),
        ([0.01] * 3, [0, 1, 2], [0.01] * 3),
        ([0.0, 0.006, 0.0, 0.006, 0.0], [3], [0.01]),
        ([0.0] * 3, [], []),
        ([], [], []),
    ],
)
def test_resample_quantizes_recorded_time(durations, expected_indices, expected_durations):
    frame_records = [
        (["root\x00example.py\x001", f"sample{index}\x00example.py\x002"], duration)
        for index, duration in enumerate(durations)
    ]
    session = Session(
        frame_records=frame_records,
        start_time=123,
        duration=sum(durations),
        min_interval=0.001,
        max_interval=0.035,
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
    assert sum(duration for _, duration in resampled.frame_records) == pytest.approx(
        sum(expected_durations)
    )
    assert resampled.sample_count == len(expected_indices)
    assert resampled.duration == session.duration
    assert resampled.cpu_time == session.cpu_time
    assert resampled.min_interval == resampled.max_interval == 0.01
    assert session.frame_records == frame_records
    assert [duration for _, duration in frame_records] == durations

    root = resampled.root_frame()
    if expected_indices:
        assert root is not None
        assert root.time == pytest.approx(sum(expected_durations))
    else:
        assert root is None


def test_resample_carries_remainder_across_records():
    # Binary-exact durations provide an independent integer-arithmetic oracle.
    # Check every prefix, including zero durations and multiple-interval samples.
    for ticks in itertools.product([0, 1, 3, 4, 9], repeat=4):
        records = [([str(index)], tick / 32) for index, tick in enumerate(ticks)]
        for length in range(1, len(records) + 1):
            result = Session._resample_frame_records(records[:length], interval=4 / 32)
            expected_ticks = sum(ticks[:length]) // 4 * 4
            assert sum(duration for _, duration in result) == expected_ticks / 32
            assert all(duration > 0 and duration % (4 / 32) == 0 for _, duration in result)


@pytest.mark.parametrize(
    "duration, expected",
    [(0.375 - 2**-54, 0.25), (0.375, 0.375), (0.375 + 2**-54, 0.375)],
)
def test_resample_near_interval_multiple(duration, expected):
    # Retain the existing floating-point boundary semantics: a value just below
    # a multiple rounds down, while the exact multiple and the next float do not.
    result = Session._resample_frame_records([(["sample"], duration)], interval=0.125)
    assert result == [(["sample"], expected)]


def test_resample_rounding_error_does_not_accumulate():
    interval = 0.01
    records = [(["sample"], duration) for duration in [0.006, 0.017, 0.002] * 1001]
    result = Session._resample_frame_records(records, interval)
    error = math.fsum(duration for _, duration in records) - math.fsum(
        duration for _, duration in result
    )
    # Only the final partial interval is omitted, rather than one per sample.
    # A small tolerance allows for binary floating-point arithmetic.
    assert -1e-12 <= error < interval + 1e-12
    assert all(
        duration / interval == pytest.approx(round(duration / interval)) for _, duration in result
    )
