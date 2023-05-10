test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

dox:
	cd docs && poetry run $(MAKE) html
	poetry run python -m http.server 8000 --directory docs/_build/html

release_patch:
	./release.sh patch

release_minor:
	./release.sh minor

release_major:
	./release.sh major