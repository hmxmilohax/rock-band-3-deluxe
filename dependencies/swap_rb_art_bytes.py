import os
import struct
import sys

def Main():
    if len(sys.argv) < 2:
        print("Usage: swap_rb_art_bytes <input path> <output path>")
        return
    elif len(sys.argv) < 3:
        print("Expected three arguements.")
        return

    Swapper(sys.argv[1], sys.argv[2])
    print("Swapped Successfully!")

def Swapper(pathIn, pathOut):
    fin = open(pathIn, "rb")
    fout = open(pathOut, "wb")

    size = fin.seek(0,2)

    fin.seek(0,0)
    fout.seek(0,0)

    buffer = fin.read(32)
    fout.write(buffer)

    # Shuffles bytes after header.
    while (fin.tell() < size):
        buf1 = fin.read(1)
        buf2 = fin.read(1)

        fout.write(buf2)
        fout.write(buf1)

    fin.seek(0,0)
    fin.close()
    fout.close()
    pass

if __name__ == '__main__':
    Main()