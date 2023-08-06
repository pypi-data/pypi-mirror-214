# ENV
- Python 3.10.11
```
sudo apt-get install python-tk
```

# To publish new version
- Update version in setup.py
- Run command below to rebuild project and publish to PyPi
```
rm -rf dist && rm -rf memv.egg-info && python setup.py sdist && twine upload dist/*
```
