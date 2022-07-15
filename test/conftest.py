import sys

import pytest

from pyinstrument import stack_sampler


def pytest_addoption(parser) -> None:
    # IPython tests seem to pollute the test environment, so they're run in a
    # separate process.

    parser.addoption(
        "--only-ipython-magic",
        action="store_true",
        default=False,
        help="run only ipython magic tests",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "ipythonmagic: test requires --only-ipython-magic flag to run"
    )


def pytest_collection_modifyitems(config, items) -> None:
    flag_was_passed = config.getoption("--only-ipython-magic")

    skip_not_ipython = pytest.mark.skip(reason="not an ipython test")
    skip_ipython = pytest.mark.skip(reason="requires --only-ipython-magic option to run")

    for item in items:
        if "ipythonmagic" in item.keywords:
            if not flag_was_passed:
                item.add_marker(skip_ipython)
        else:
            if flag_was_passed:
                item.add_marker(skip_not_ipython)


@pytest.fixture(autouse=True)
def check_sampler_state():
    assert sys.getprofile() is None
    assert len(stack_sampler.get_stack_sampler().subscribers) == 0

    try:
        yield
        assert sys.getprofile() is None
        assert len(stack_sampler.get_stack_sampler().subscribers) == 0
    finally:
        sys.setprofile(None)
        stack_sampler.thread_locals.__dict__.clear()
