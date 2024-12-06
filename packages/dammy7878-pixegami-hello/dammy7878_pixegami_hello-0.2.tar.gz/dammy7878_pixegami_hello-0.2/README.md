## Publish to PYPI

To publish your python package to PYPI, you can use the twine tool.



```bash

python setup.py sdist bdist_wheel 

export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-XXXXXXXXX

twine upload dist/*
```