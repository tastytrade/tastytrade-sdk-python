check: lint test

lint:
	poetry run pylint src tests

test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

.PHONY: docs
docs:
	poetry run pdoc src/tastytrade_sdk --docformat numpy --no-show-source -t docs/users

release_patch:
	./release.sh patch

release_minor:
	./release.sh minor

release_major:
	./release.sh major