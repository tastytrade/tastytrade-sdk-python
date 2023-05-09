#!/bin/zsh

if [[ "$(git rev-parse --abbrev-ref HEAD)" != "master" ]]; then
  echo 'Release should be run on master. Exiting.';
  exit 1;
fi

