#!/usr/bin/env python3
"""
Release script for version management.
Usage: python release.py [patch|minor|major]
"""

import sys
import subprocess
import argparse


def run_command(command):
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Command failed with exit code {e.returncode}")
        return e.returncode


def release(version_type):
    print(f"Starting {version_type} release...")

    # Example release commands - customize as needed
    commands = [
        f"poetry version {version_type}",
        "git add pyproject.toml",
        f'git commit -m "Bump {version_type} version"',
        # Uncomment and modify as needed:
        # "poetry build",
        # "poetry publish",
        # "git tag v$(poetry version -s)",
        # "git push origin main --tags",
    ]

    for command in commands:
        result = run_command(command)
        if result != 0:
            print(f"Release failed at step: {command}")
            return result

    print(f"{version_type} release completed successfully!")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Release script for version management")
    parser.add_argument(
        "version_type",
        choices=["patch", "minor", "major"],
        help="Type of version bump to perform"
    )

    args = parser.parse_args()

    return release(args.version_type)


if __name__ == "__main__":
    sys.exit(main())