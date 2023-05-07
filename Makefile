clean:
	rm -rf dist

build: clean
	pipenv run python -m build

set_alpha_version_tag:
	pipenv run python set_alpha_version_tag.py ${ALPHA_TAG}

upload:
	pipenv run python -m twine upload dist/* -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD}