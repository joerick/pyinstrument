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

















## RENDERER
### New Testing Segment
I made new tests for the HTML Render component of the project to test its ability to produce reports with minimal values
Specifically testing the components of save_html_report(), HTMLRenderer() and profiler.output()

The rationale behind these tests is to document and examine the program's ability to render through data at a fixed rate to see where and what we can optimize.

### Mocking Strategy    
By using unittest's patch function, it was able to replace save_html_report
This approach allows us to check if the HTML Reports go through, along with small amounts of data

### Coverage Improvement Analysis
The overall testing coverage is still 75%. In order for the number to improve, a wider array of tests for other parts and components are necessary
