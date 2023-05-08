test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

clean:
	rm -rf dist *.egg-info

build_and_serve_docs:
	cd docs && $(MAKE) html
	poetry run python -m http.server 8000 --directory docs/_build/html

serve_docs:
	poetry run watchmedo auto-restart -R -d src -d docs --no-restart-on-command-exit make -- build_and_serve_docs