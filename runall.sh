#!/bin/bash

(
flock -x -w 5 200 || exit 1

~/.cmus/record-play.py "$@"
) 200>$HOME/.cmus/.cmus-runall.exclusivelock
