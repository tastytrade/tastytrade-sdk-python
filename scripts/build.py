"""
Poetry script commands for tastytrade-sdk
"""
import subprocess
import sys
import os

def run_cmd(cmd):
    return subprocess.run(cmd, shell=True).returncode == 0

def lint():
    return run_cmd("pylint src tests")

def test():
    print("Running tests...")
    return run_cmd('python -m unittest discover -s "tests" -p "*.py"')

def check():
    success = lint()
    if success:
        success = test()
    return success

def docs():
    return run_cmd("pdoc src/tastytrade_sdk --docformat numpy --no-show-source -t docs/users")

def release_patch():
    return run_cmd("./release.sh patch")

def release_minor():
    return run_cmd("./release.sh minor")

def release_major():
    return run_cmd("./release.sh major")

def run_experiment():
    env = os.environ.copy()
    env['PYTHONPATH'] = '.'
    return subprocess.run("python3 tests/market_data_experiment.py", shell=True, env=env).returncode == 0