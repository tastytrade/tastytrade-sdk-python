clean:
	rm -rf dist

build: clean
	pipenv run python -m build

set_dev_version_tag:
	pipenv run python set_dev_version_tag.py ${DEV_TAG}

upload:
	pipenv run python -m twine upload dist/* -u ${TEST_PYPI_USERNAME} -p ${TEST_PYPI_PASSWORD} -r testpypi