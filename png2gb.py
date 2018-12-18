#!/usr/bin/env python3

import sys
import argparse
from PIL import Image


def main():

    args = parse_arguments()

    img = Image.open(args.file, 'r')
    
    if img.width != DMG_WIDTH or img.height != DMG_HEIGHT:
        print("ERROR: Image is larger than 160x144")
        sys.exit(1)
    
    if len(img.getcolors()) > 4:
        print("ERROR: More than 4 colors found in image (including transparency)")
        sys.exit(1)

    tile_list = get_tile_list(list(img.getdata()))
    (tiles, tilemap) = generate_tilemap(tile_list)
    
    with open('tiles.c', 'w') as f:
        f.write("const unsigned char TileData[] = {\n%s\n};""" % ',\n'.join(tiles))
    with open('map.c', 'w') as f:
        f.write("const unsigned char MapData[] = {\n%s\n};" % ',\n'.join(tilemap))


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('file',
                        help='PNG image file to convert')

    return parser.parse_args()


def get_tile_list(image_data):

    tile_list = [[[] for i in range(0, int(DMG_WIDTH / TILE_SIZE))] for x in range(0, int(DMG_HEIGHT / TILE_SIZE))]

    for n, pixel in enumerate(image_data):
        screen_row = int(n / DMG_WIDTH)
        screen_col = n - (screen_row * DMG_WIDTH)

        tile_list[int(screen_row / TILE_SIZE)][int(screen_col / TILE_SIZE)].append(pixel)

    return tile_list

def generate_tilemap(tile_list):

    tiles = []
    tilemap = []

    for map_tile_row in tile_list:
        tilemap.append([])
        for map_tile in map_tile_row:
            tile = []

            for pixel_row in range(0, TILE_SIZE):
                row = map_tile[pixel_row * 8:(pixel_row * 8) + 8]
                byte1 = ""
                byte2 = ""

                for pixel in row:
                    if pixel == 3:
                        byte1 += '0'
                        byte2 += '0'
                    elif pixel == 2:
                        byte1 += '1'
                        byte2 += '0'
                    elif pixel == 1:
                        byte1 += '0'
                        byte2 += '1'
                    elif pixel == 0:
                        byte1 += '1'
                        byte2 += '1'

                # Convert these to hex
                byte1 = "0x%s" % hex(int(byte1, base=2))[2:].zfill(2)
                byte2 = "0x%s" % hex(int(byte2, base=2))[2:].zfill(2)

                tile.append(byte1)
                tile.append(byte2)

            tile = ','.join(tile)

            if tile in tiles:
                tilenum = tiles.index(tile)
            else:
                tilenum = len(tiles)
                tiles.append(tile)

            tilemap[-1].append("0x%s" % hex(tilenum)[2:].zfill(2))

        tilemap[-1] = ','.join(tilemap[-1])

    return (tiles, tilemap)

if __name__ == '__main__':
    (DMG_WIDTH, DMG_HEIGHT) = (160, 144)
    TILE_SIZE = 8

    main()
