# cmhlims_py

## Create a virtual environment
python -m venv myenv
source myenv/bin/activate

## install the dependencies
pip install -r requirements.txt

## building a package
pip install wheel
python setup.py sdist bdist_wheel
