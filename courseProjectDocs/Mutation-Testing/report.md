## Setup
For setting up mutmut, we needed to edit the setup.cfg file. We added to following code:

```
[mutmut]
runner = pytest
paths_to_mutate =
    pyinstrument
tests_dir =
    test
do_not_mutate =
    pyinstrument/__main__.py
    pyinstrument/__init__.py
    pyinstrument/profiler.py
    pyinstrument/stack_sampler.py
    pyinstrument/renderers/*
    pyinstrument/context_manager.py
    pyinstrument/util.py
    pyinstrument/vendor/*
    pyinstrument/processors.py
mutate_only_covered_lines = true
```

## Mutation Tests
Initially, we had 376 mutations that survived. After our added tests, we had 373. 

## Analysis
- We fixed the issue inside of shorten path where mutating a list to "none" had no effect, by creating a test to ensure that the function could not return none, therefore killing the mutant.

## Group Contributions
To see the mutation tests use the following command ```mutmut show``` followed by the code of the tests ```mutmut show pyinstrument.low_level.stat_profile_python.xǁPythonStatProfilerǁprofile__mutmut_8```
- Jose: did setup of the mutmut library and the context change frame handling test (pyinstrument.low_level.stat_profile_python.xǁPythonStatProfilerǁprofile__mutmut_8)
- Ursula: helped with setup debugging and did the shorten path test (pyinstrument.session.xǁSessionǁshorten_path__mutmut_2)
- Michael: did the [] test
