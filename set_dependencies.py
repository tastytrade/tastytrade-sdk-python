from toml import load, dump

with open('requirements.txt', 'r') as requirements:
    dependencies = [x for x in requirements.readlines() if x and not x.startswith('-')]

fname = 'pyproject.toml'
pyproject = load(fname)
pyproject['project']['dependencies'] = dependencies
with open(fname, 'w') as out:
    dump(pyproject, out)
