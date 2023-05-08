test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

clean:
	rm -rf dist *.egg-info

dox:
	cd docs && $(MAKE) html
	poetry run python -m http.server 8000 --directory docs/_build/html