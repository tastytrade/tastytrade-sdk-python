#!/bin/zsh

read_release_type() {
  export ERROR_MESSAGE="Usage: './release.sh (patch|minor|major)'"
  if [ -z "$1" ]; then
    echo "${ERROR_MESSAGE}"
    exit 1
  fi
  if ! [[ $1 =~ (patch|minor|major) ]] ; then
    echo "${ERROR_MESSAGE}"
    exit 1
  fi
  echo "$1"
}

release_type="$(read_release_type $1)"

if [[ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]]; then
  echo 'Release should be run on master. Exiting.'
  exit 1
fi

if [[ -n $(git status -s) ]]; then
  echo "There are uncommitted changes. Exiting."
  exit 1
fi

if [[ $(git rev-parse HEAD) != $(git rev-parse master@{upstream}) ]]; then
  echo 'Local master is not in sync with remote. Exiting.'
  exit 1
fi

export NEW_VERSION="$(poetry version ${release_type} --short)"
git add pyproject.toml
git commit -m "Release ${NEW_VERSION}"
git tag ${NEW_VERSION}
git push origin ${NEW_VERSION}

export NEW_PREPATCH_VERSION="$(poetry version prepatch --short)"
git add pyproject.toml
git commit -m "Bumping to next pre-patch version ${NEW_PREPATCH_VERSION}"
git push