check: lint test

lint:
	poetry run pylint src tests

test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

.PHONY: docs
docs:
	poetry run mkdocs serve -f docs/mkdocs.yml

check_docs:
	poetry run mkdocs build -s -f docs/mkdocs.yml

release_patch:
	./release.sh patch

release_minor:
	./release.sh minor

release_major:
	./release.sh major