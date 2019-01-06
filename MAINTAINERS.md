# Releasing

```
bumpversion <patch/minor/major/num>
# or, bumpversion --new-version x.x.x <patch/minor/major/num>
rm -rf dist
rm -rf build
python setup.py sdist bdist_wheel
twine upload dist/<sdistfilename> dist/<wheelfilename>
```
