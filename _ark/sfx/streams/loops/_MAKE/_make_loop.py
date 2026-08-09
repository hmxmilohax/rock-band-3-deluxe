# hai
# requires ffmpeg and makemogg
# this is incredibly barebones and only works when all 4 audio files are present

# MAPPINGS:
# 1.wav - Drums
# 2.wav - Bass
# 3.wav - Stereo Misc
# 4.wav - Mono Misc (render blank audio if none else)

# throw the outputted loop.ogg file into reaper and normalize it (ctrl+shift+n) to get the volume value for dta, remove it when done
# add loop and volume in dx/ui/dx_metamusic.dta
# add text in dx/locale/dx_locale_metamusic.dta

import subprocess
import os
import sys

def shittify():
	# automatically downmix and downsample input files
	# should proberly use a loop for this but i'm #lazy
	# vanilla rb3 does 28k so we follow
	subprocess.run([
		"ffmpeg", "-loglevel", "error",
		"-i", "1.wav",
		"-ar", "28000", "-af", "aresample=resampler=soxr:precision=33:cheby=1",
		"-ac", "2",
		"-c:a", "pcm_s16le",
		"1-temp.wav"
	])
	subprocess.run([
		"ffmpeg", "-loglevel", "error",
		"-i", "2.wav",
		"-ar", "28000", "-af", "aresample=resampler=soxr:precision=33:cheby=1",
		"-ac", "1",
		"-c:a", "pcm_s16le",
		"2-temp.wav"
	])
	subprocess.run([
		"ffmpeg", "-loglevel", "error",
		"-i", "3.wav",
		"-ar", "28000", "-af", "aresample=resampler=soxr:precision=33:cheby=1",
		"-ac", "2",
		"-c:a", "pcm_s16le",
		"3-temp.wav"
	])
	subprocess.run([
		"ffmpeg", "-loglevel", "error",
		"-i", "4.wav",
		"-ar", "28000", "-af", "aresample=resampler=soxr:precision=33:cheby=1",
		"-ac", "1",
		"-c:a", "pcm_s16le",
		"4-temp.wav"
	])

def encode():
	subprocess.run([
		"ffmpeg", "-loglevel", "error",
		"-i", "1-temp.wav", "-i", "2-temp.wav", "-i", "3-temp.wav", "-i", "4-temp.wav",            # vv     vv   bitch what the fuck
		"-filter_complex", ("[0:a][1:a][2:a][3:a]" "join=inputs=4:channel_layout=5.1:" "map=0.0-FL|1.0-FR|0.1-FC|2.0-BL|2.1-BR|3.0-LFE" "[aout]"), "-map", "[aout]",
		"-c:a", "libvorbis", "-q:a", "0",  # lmao
		"loop.ogg"
	])
	subprocess.run(["makemogg", "loop.ogg", "-m", "loop.mogg"])	

def main():

	shittify()

	encode()

	os.remove("1-temp.wav")
	os.remove("2-temp.wav")
	os.remove("3-temp.wav")
	os.remove("4-temp.wav")
	#os.remove("loop.ogg")  # keep this until i figure out automating getting the peak

main()
