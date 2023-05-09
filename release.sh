#!/bin/zsh

if [[ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]]; then
  echo 'Release should be run on master. Exiting.';
  exit 1;
fi

if [[ $(git rev-parse HEAD) != $(git rev-parse master@{upstream}) ]]; then
  echo 'Local master is not in sync with remote. Exiting.';
  exit 1;
fi