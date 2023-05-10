check: checkstyle test

checkstyle:
	poetry run pylint src tests

test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

build_serve_docs:
	cd docs && poetry run $(MAKE) html
	poetry run python -m http.server 8000 --directory docs/_build/html

watch_docs:
	poetry run watchmedo auto-restart \
		-d src -d docs -i 'docs/_build' \
		--recursive \
		--no-restart-on-command-exit \
		-q --timeout 5 \
		make -- build_serve_docs

release_patch:
	./release.sh patch

release_minor:
	./release.sh minor

release_major:
	./release.sh major