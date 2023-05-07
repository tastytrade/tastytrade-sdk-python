test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

clean:
	rm -rf dist *.egg-info