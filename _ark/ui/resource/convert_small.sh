#!/usr/bin/bash
for file in ./game_origins/*
do
    magick $file -filter catrom -resize 64x64 "./game_origins_small/$(basename $file)"
done