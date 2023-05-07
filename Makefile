test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

clean:
	rm -rf dist *.egg-info

set_dev_version_tag:
	pipenv run python set_dev_version_tag.py ${DEV_TAG}

build_upload:
	poetry -r testpypi -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD} --build