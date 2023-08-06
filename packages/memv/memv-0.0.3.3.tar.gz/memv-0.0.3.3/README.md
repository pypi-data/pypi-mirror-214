# ENV
- Python 2.7
```
sudo apt-get install python-tk
```

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