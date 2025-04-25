# gen_song_update_hash.py
import hashlib
from pathlib import Path
import sys

path = sys.argv[1]

song_hash = hashlib.new("md5")

f = open(Path("_ark", "dx", "song_updates", "songs_updates.dta"), "rb")

while chunk := f.read(8192):
    song_hash.update(chunk)

f.close()

f = open(path, "w")

f.write(f'{{set $dx_song_update_hash "{song_hash.hexdigest()}"}}\n')

f.close()