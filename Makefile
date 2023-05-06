clean:
	rm -rf dist

build: clean
	pipenv run python -m build

upload:
	pipenv run python -m twine upload dist/* -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD} --skip-existing