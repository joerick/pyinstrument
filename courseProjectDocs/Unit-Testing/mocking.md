# MOCKING & STUBBING

## PROFILER
### Test folder
The mock tests of this module can be found in the follow folder ```Profiler``` 

### New Test Cases & Rationale
The tests implemented are to verify that the ```run_and_save_profile``` function correctly calls the ```save_profile_to_db``` method. This isolate external side effects and focuses on correct interactions.

The rationale is to ensure that changes in external depedenies won't break the core profiling logic enabling safer refactors.

### Mocking Strategy
The use of ```unittest.mock.patch``` to replace ```save_profile_to_db``` with a mock during tests.

This allows to:
- Confirm the function was called exactly once
- Check the argument passed to it is a string

### Coverage Improvement Analysis
The overall test coverage is still 75%. Mocks help improve test reliability and make it easier to test external calls. To increase coverage beyond this, more tests for other parts of the code are needed.

## PROFILER - Heavy Task 

### New Test Cases & Rationale
New test cases were added to verify that the run_profiler_and_report function interacts correctly with the pyinstrument.Profiler class.
These tests focus on ensuring that Profiler.start(), Profiler.stop(), and Profiler.output_text() are called exactly once, and that run_profiler_and_report() correctly returns the generated report string.

The rationale behind this is to confirm that profiling is initialized and terminated in a controlled, predictable manner. In a performance monitoring context, calling start() or stop() multiple times or failing to call them at all could corrupt profiling data, cause overlapping sessions, or produce inaccurate performance results. By verifying that these methods execute exactly once, the tests ensure that the profiling session wraps only the intended computation (run_heavy_task()), maintaining both timing accuracy and system stability. I chose a heavy task because it provides a realistic workload that would have a higher chance of errors.

### Mocking Strategy
unittest.mock.patch was used to replace the Profiler class with a mock object.
This approach isolates the logic flow from the underlying profiling implementation and avoids unnecessary CPU-intensive profiling runs

### Coverage Improvement Analysis
The overall test coverage is still 75%. To increase coverage beyond this, more tests for other parts of the code are needed.