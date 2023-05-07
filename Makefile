test:
	poetry run python -m unittest discover -s 'tests' -p '*.py'

clean:
	rm -rf dist *.egg-info

doc_server:
	cd docs && poetry run make livehtml