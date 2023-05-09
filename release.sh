#!/bin/zsh

if [[ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]]; then
  echo 'Release should be run on master. Exiting.';
  exit 1;
fi

if [[ -n $(git status -s) ]]; then
  echo "There are uncommitted changes. Exiting."
  exit 1;
fi

if [[ $(git rev-parse HEAD) != $(git rev-parse master@{upstream}) ]]; then
  echo 'Local master is not in sync with remote. Exiting.';
  exit 1;
fi

export NEW_VERSION="$(poetry version patch --short)"
git add pyproject.toml
git commit -m "Release ${NEW_VERSION}"
git tag -f ${NEW_VERSION}
git tag -f latest
git push -f ${NEW_VERSION} latest