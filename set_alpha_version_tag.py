from sys import argv

from toml import load, dump

if len(argv) < 2 or not argv[1]:
    print('Alpha tag must be provided')
    exit(1)

alpha_tag = argv[1]
fname = 'pyproject.toml'
pyproject = load(fname)
pyproject['project']['version'] += f'a{alpha_tag}'
with open(fname, 'w') as out:
    dump(pyproject, out)
