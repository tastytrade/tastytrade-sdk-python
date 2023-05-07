from sys import argv

from toml import load, dump

if len(argv) < 2 or not argv[1]:
    print('Dev tag must be provided')
    exit(1)

dev_tag = argv[1]
fname = 'pyproject.toml'
pyproject = load(fname)
pyproject['project']['version'] += f'dev{dev_tag}'
with open(fname, 'w') as out:
    dump(pyproject, out)
