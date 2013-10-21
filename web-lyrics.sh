#!/bin/bash

artist="$(./urlencode <<< $1)"
title="$(./urlencode <<< $2)"

lyric="`curl -s "http://makeitpersonal.co/lyrics?artist=$artist&title=$title"`"

if [ -z "$lyric" -o $? -ne 0 -o "$lyric" == "artist is empty" -o "$lyric" == "title is empty" -o "$lyric" == "Sorry, We don't have lyrics for this song yet." ]
then
    exit 1
else
    echo -n "$lyric"
    exit 0
fi
