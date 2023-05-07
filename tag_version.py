from sys import argv

from toml import load, dump

if len(argv) < 2 or not argv[1]:
    print('Tag must be provided')
    exit(1)

tag = argv[1]
fname = 'pyproject.toml'
pyproject = load(fname)
pyproject['project']['version'] += f'-{tag}'
with open(fname, 'w') as out:
    dump(pyproject, out)
