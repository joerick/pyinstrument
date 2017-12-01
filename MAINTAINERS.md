# Releasing

```
bumpversion <patch/minor/major>
python setup.py sdist bdist_wheel
twine upload dist/<sdistfilename> dist/<wheelfilename>
```

