test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

dox:
	cd docs && poetry run $(MAKE) html
	poetry run python -m http.server 8000 --directory docs/_build/html

release_patch: test
	./release.sh patch

release_minor: test
	./release.sh minor

release_major: test
	./release.sh major