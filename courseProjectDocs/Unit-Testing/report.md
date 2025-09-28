# Unit Test for Pyinstrument

This folder contains unit tests developed for the pyinstrument to verify its core functionalities and ensure robustness.

## How to run these tests
Make sure you have ```pytest``` and ```pytest-cov``` installed in your enviroment (venv is recomended)
1. Position yourself in the root of the project
2. From the root run this:

```
pytest
```

# Profiler tests
These tests focus on ensuring the functionality of the ```Profiler``` class from the pyinstrument package. They check that the profiler:

- Initializes correctly
- Starts and stops as expected
- Clears previously sessions when reset
- Works properly as a context manager
- Produces output with duration information

# Total test summary
The overall test coverage remains steady at 74% the same as before adding the 15 new tests. This means the new tests mainly reinforce existing code areas without expanding coverage to new paths of the codebase.

The stable coverage shows a consistent level of testing quality although additional tests help improve reliability.
