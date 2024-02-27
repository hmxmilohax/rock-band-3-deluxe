import os
import struct
import sys

class Headers:
    wii_64x64 = bytes([0x01, 0x04, 0x48, 0x00, 0x00, 0x00, 0x02, 0x80, 0x00, 0x40, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    wii_128x128 = bytes([0x01, 0x04, 0x48, 0x00, 0x00, 0x00, 0x03, 0x80, 0x00, 0x80, 0x00, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    wii_128x256 = bytes([0x01, 0x04, 0x48, 0x00, 0x00, 0x00, 0x00, 0x80, 0x00, 0x00, 0x01, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    wii_256x256 = bytes([0x01, 0x04, 0x48, 0x00, 0x00, 0x00, 0x04, 0x00, 0x01, 0x00, 0x01, 0x80, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

def Main():
    if len(sys.argv) < 3:
        print("Usage: tpl_to_png_wii <input path> <output path>")
        return

    Convert(sys.argv[1], sys.argv[2])

def Convert(pathIn, pathOut):
    with open(pathIn, "rb") as binaryReader:
        width, height = GetImageDimensions(binaryReader)
        header = GetHeader(width, height)
        if header:
            # Jump to Image Data Address
            binaryReader.seek(0x08)  # Image Data Address in Image Header
            image_data_address = struct.unpack(">I", binaryReader.read(4))[0]  # u32 int
            binaryReader.seek(image_data_address)  # Go to Image Data Address

            # Read image data by its length
            image_data = binaryReader.read(width * height * 4)  # Assuming RGBA format

            with open(pathOut, "wb") as binaryWriter:
                # Write the header
                binaryWriter.write(header)
                # Write the image data
                binaryWriter.write(image_data)
        else:
            print("Unsupported image size.")
            exit()
            return


def GetImageDimensions(file):
    file.seek(0x0C)  # Skip to Image Offset Table
    image_header_offset = struct.unpack(">I", file.read(4))[0]  # u32 int
    file.seek(image_header_offset)  # Go to Image Header
    height = struct.unpack(">H", file.read(2))[0]  # u16 int
    width = struct.unpack(">H", file.read(2))[0]   # u16 int
    print("Width:", width)
    print("Height:", height)
    return width, height


def GetHeader(width, height):
    if width == 64 and height == 64:
        return Headers.wii_64x64
    elif width == 128 and height == 128:
        return Headers.wii_128x128
    elif width == 128 and height == 256:
        return Headers.wii_128x256
    elif width == 256 and height == 256:
        return Headers.wii_256x256
    else:
        return None

if __name__ == '__main__':
    Main()