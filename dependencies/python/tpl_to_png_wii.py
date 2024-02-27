import os
import struct
import sys

wii_256x256 = bytes([0x01, 0x04, 0x48, 0x00, 0x00, 0x00, 0x04, 0x00, 0x01, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

def Main():
    if len(sys.argv) < 2:
        print("Usage: tpl_to_png_wii <input path> <output path>")
        return
    elif len(sys.argv) < 3:
        print("Expected three arguements.")
        return

    Convert(sys.argv[1], sys.argv[2])

def Convert(pathIn, pathOut):
    with open(pathIn, "rb") as binaryReader, open(pathOut, "wb") as binaryWriter:
       binaryReader.seek(64)
       binaryWriter.write(Headers.wii_256x256)
    buffer = bytearray(64)
    while True:
        num = binaryReader.readinto(buffer)
        if num > 0:
            binaryWriter.write(buffer[:num])
        else:
            break


if __name__ == '__main__':
    Main()