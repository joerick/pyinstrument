# Profiler tests
These tests focus on ensuring the functionality of the ```Profiler``` class from the pyinstrument package. They check that the profiler:

- Initializes correctly
- Starts and stops as expected
- Clears previously sessions when reset
- Works properly as a context manager
- Produces output with duration information

# Total test summary
The overall test coverage remains steady at 74% the same as before adding the 5 new tests. This means the new tests mainly reinforce existing code areas without expanding coverage to new paths of the codebase.

The stable coverage shows a consistent level of testing quality although additional tests help improve reliability.

# Edge Case tests
These tests focus on ensuring the robustness of the pyinstrument package in less common or boundary scenarios. They check that the profiler and session logic:

- Handles cases where no samples are collected without crashing
- Raises appropriate errors when invalid args are passed
- Fails gracefully when attempting to load a corrupted sesion file
- Enforces that there's a RuntimeError on a second stop() call
- Returns none for an empty session’s frame

# Total test summary
The overall test coverage has increased slightly to 75%, up from the previous 74%. This shows that these new tests touch a few additional lines of code that were previously untested. As all the tests passed, these added edge case tests show robustness around error handling and empty-state behavior.

# Session Testing
These tests focus on ensuring the functionality of the ```Frame``` class:

- Adding a Child to the Parent
- Length of the parent's array
- Child reference
- Testing the reference's str tag
- Adding multiple children to parents

# Total test summary
The overall test coverage remains steady at 74% the same as before adding the 5 new tests. This means the new tests mainly reinforce existing code areas without expanding coverage to new paths of the codebase.

The stable coverage shows a consistent level of testing quality although additional tests help improve reliability.

The overall test coverage of the project remains around the 74% range, despite adding 5 more additional tests. With this we can conclude that the newer tests mainly reinforce existing code and not trying to make new ground with newer developments

# Edge Case tests
These tests focus on ensuring the robustness of the pyinstrument package with it's base functions. THese tets cover
- Frame's range
- Child and Parent Relations
- References between classes

# Total test summary
The overall test coverage has made a small increase to 75%,  This shows that these new tests touch a few additional lines of code that were previously untested.
