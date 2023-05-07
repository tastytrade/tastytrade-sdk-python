clean:
	rm -rf dist

build:
	pipenv run python -m build

upload_test:
	pipenv run python -m twine upload dist/* -u ${TEST_PYPI_USERNAME} -p ${TEST_PYPI_PASSWORD} -r testpypi

upload:
	pipenv run python -m twine upload dist/* -u ${PYPI_USERNAME} -p ${PYPI_PASSWORD} --skip-existing