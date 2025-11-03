## Tool used
Ruff an static analysis tool for Python ```https://docs.astral.sh/ruff/```

Install ruff with ```pip install ruff```
To run ruff in the project do ```ruff check``` this need to be in the root of the project

## Key findings
Total issues detected: 77

Highlight identified issues:
- E731 - Lambda assigned to variable
Location: metrics/overhead.py:28:1
Issue: Lambda assigned to test_func; ruff recomend using def
Impact: Improves code readability and debuggability

- E722 - Bare except
Location: examples/context_api.py:26:21
Issue: Local variable time overwrote the imported time module
Impact: Could hide real runtime errors

- F841 - Variable assigned but never used
Location: pyinstrument/magic/magic.py:264:9
Issue: Local variable `html_config` is assigned to but never used
Impact: Improves code readability and memory

- E712 - Using equality comparison for truth check
Location: test/test_profiler.py:322:12
Issue: Avoid equality comparisons to `True`; use `profiler.is_running:` for truth checks
Impact: Improves code readability and efficiency

## Fix summary
- E731 - Lambda assigned to variable
Solution: Converted the lambda into a normal function using def test_func():

- E722 - Bare except
Solution: Replaced except with except OSError to catch only file related errors

- F841 - Variable assigned but never used
Solution: removed extraneous variable

- E712 - Using equality comparison for truth check
Solution: removed equality comparison and replaced with function

- E731 - Do not assign a `lambda` expression, use a `def`
Solution: rewrote `show_pyinstrument` as a `def`

* Simple issues were fixed with ```ruff check . --fix```

## Group contributions
- Jose: Set up the static analysis tool Ruff, fixes simple issues using ```ruff check . --fix``` which reduced the total number of issues from 77 to 35 and manually addressed other remaning errors. The most notable fixes were E731 and E722
- Ursula: Did the F841 and E712 fixes, and reduced issues from 25 to 23
- Michael: Tackled another bug within E731, changing the formatting of ```show_pyinstrument``` as a function, in lines 41-46
