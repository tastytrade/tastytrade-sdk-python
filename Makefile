test:
	pipenv run python -m unittest discover -s 'tests' -p '*.py'

clean:
	rm -rf dist *.egg-info

set_dependencies:
	pipenv requirements > requirements.txt
	pipenv run python set_dependencies.py

set_dev_version_tag:
	pipenv run python set_dev_version_tag.py ${DEV_TAG}

build: clean
	pipenv run python -m build

upload:
	pipenv run python -m twine upload dist/* -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD} -r testpypi