test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

clean:
	rm -rf dist *.egg-info site

build_and_serve_docs:
	poetry run mkdocs build
	poetry run python -m http.server 8000 --directory site

serve_docs:
	poetry run watchmedo auto-restart -R -d src -d docs -d mkdocs.yml --no-restart-on-command-exit make -- build_and_serve_docs