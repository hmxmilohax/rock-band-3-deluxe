if [ -d ~/.config/rpcs3/dev_hdd0/game/BLUS30463 ]; then
	echo "~/.config/rpcs3/dev_hdd0/game/BLUS30463 already exists, not symlinking"
else
	mkdir -p ~/.config/rpcs3/dev_hdd0/game
	ln -s "$PWD/_build/ps3" ~/.config/rpcs3/dev_hdd0/game/BLUS30463
	echo "Symlinked _build/ps3/ to ~/.config/rpcs3/dev_hdd0/game/BLUS30463"
fi
