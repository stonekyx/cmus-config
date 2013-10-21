#!/bin/bash

artist=$1
title=$2

if [ "$artist" == '""' ]; then
    artist=""
fi

if [ "$title" == '""' ]; then
    title=""
fi

if [ -z "$artist" -a -z "$title" ]; then
    exit 1
fi

cd "$(dirname "$0")"

lyric="$(./web-lyrics.sh "$artist" "$title")"
if [ $? -eq 0 -a "$lyric" ]; then
    echo "$lyric"
    exit 0
fi

lyric="$(./anime-lyrics.py "$artist" "$title")"
if [ $? -eq 0 -a "$lyric" ]; then
    echo "$lyric"
    exit 0
fi

urxvt -e vim +set\ paste /tmp/lyrics.cmus &&
    cat /tmp/lyrics.cmus &&
    rm -f /tmp/lyrics.cmus
