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

## Fix summary
- E731 - Lambda assigned to variable
Solution: Converted the lambda into a normal function using def test_func():

- E722 - Bare except
Solution: Replaced except with except OSError to catch only file related errors

- E731 - Do not assign a `lambda` expression, use a `def`
Solution: rewrote `show_pyinstrument` as a `def`

* Simple issues were fixed with ```ruff check . --fix```

## Group contributions
- Jose: Set up the static analysis tool Ruff, fixes simple issues using ```ruff check . --fix``` which reduced the total number of issues from 77 to 35 and manually addressed other remaning errors. The most notable fixes were E731 and E722
- Ursula:
- Michael: Tackled another bug within E731, changing the formatting of ```show_pyinstrument``` as a function, in lines 41-46. 