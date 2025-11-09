import pytest
from pyinstrument import Profiler
import asyncio

def test_sync_profiler_and_renderer():
    profiler = Profiler()

    def sample_workload():
        total = 0
        for i in range(1000):
            total += i
        return total

    profiler.start()
    result = sample_workload()
    profiler.stop()

    output = profiler.output_text()

    assert result == 499500
    assert "Recorded:" in output or "[self]" in output or __file__ in output
    assert "Profiler" not in output

@pytest.mark.asyncio
async def test_async_profiler_and_renderer():
    profiler = Profiler()

    async def async_task():
        await asyncio.sleep(0.1)
        return "done"

    profiler.start()
    task_result = await async_task()
    profiler.stop()

    output = profiler.output_text()

    assert task_result == "done"
    assert "[await]" in output or "asyncio" in output or __file__ in output

if __name__ == "__main__":
    pytest.main([__file__])
