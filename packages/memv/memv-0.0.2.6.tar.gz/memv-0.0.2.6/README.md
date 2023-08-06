# To publish new version
- Update version in setup.py
- Run command below to rebuild project
```
python setup.py sdist
```
- Run command below to publish
```
twine upload dist/*
```