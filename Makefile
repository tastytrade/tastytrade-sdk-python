clean:
	rm -rf dist

build: clean
	pipenv run python -m build

tag_version:
	pipenv run python tag_version.py "${TAG}"

upload:
	pipenv run python -m twine upload dist/* -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD}