# Croqueta

Deploying to PyPI
-----------------

```
python setup.py sdist bdist_wheel
twine upload dist/*
python setup.py clean --all
```
