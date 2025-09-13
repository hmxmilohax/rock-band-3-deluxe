#!/usr/bin/bash
for file in ./game_origins_source/*
do
    magick $file -filter catrom -resize 64x64 "./game_origins/$(basename $file)"
    magick $file -filter catrom -resize 128x128 "./game_origins_128/$(basename $file)"
done