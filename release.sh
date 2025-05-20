#!/bin/zsh

export RELEASE_TYPE="$1"

export ERROR_MESSAGE="Usage: './release.sh (patch|minor|major)'"
if [ -z "${RELEASE_TYPE}" ]; then
  echo "${ERROR_MESSAGE}"
  exit 1
fi
if ! [[ "${RELEASE_TYPE}" =~ (patch|minor|major) ]]; then
  echo "${ERROR_MESSAGE}"
  exit 1
fi

if [[ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]]; then
  echo 'Release should be run on master. Exiting.'
  exit 1
fi

if [[ -n $(git status -s) ]]; then
  echo "There are uncommitted changes. Exiting."
  exit 1
fi

if [[ $(git rev-parse HEAD) != $(git rev-parse origin/master) ]]; then
  echo 'Local master is not in sync with remote. Exiting.'
  exit 1
fi

export NEW_VERSION="$(poetry version ${RELEASE_TYPE} --short)"
git checkout -b "release-${NEW_VERSION}"
git add pyproject.toml
git commit -m "Release ${NEW_VERSION}"
git tag -f ${NEW_VERSION}
git tag -f latest
git push --set-upstream origin -f ${NEW_VERSION}
git push --set-upstream origin -f latest

export NEW_PREPATCH_VERSION="$(poetry version prepatch --short)"
git add pyproject.toml
git commit -m "Bumping to next pre-patch version ${NEW_PREPATCH_VERSION}"
git push

hub pull-request -m "Release ${NEW_VERSION}"