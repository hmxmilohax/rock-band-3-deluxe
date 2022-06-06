git pull https://github.com/jnackmclain/rock-band-3-deluxe wii
cp ./_build/wii_rebuild_files/main_wii.hdr ./_build/wii
cp ./_build/wii_rebuild_files/main_wii_10.ark ./_build/wii
dependencies/arkhelper patchcreator -a ./_ark -o ./_build/wii ./_build/wii/main_wii.hdr
mv ./_build/wii/gen/main_wii.hdr ./_build/wii
mv ./_build/wii/gen/main_wii_10.ark ./_build/wii
rmdir ./_build/wii/gen