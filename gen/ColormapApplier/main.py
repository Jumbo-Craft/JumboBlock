import json
import os
from asyncio.windows_events import NULL

import numpy as np

from PIL import Image


def main():
    apply_natural_color('grass')
    apply_natural_color('foliage')
    apply_natural_color('dry_foliage')
    apply_swamp_grass1()
    apply_dark_forest_grass()
    apply_birch_leaves()
    apply_spruce_leaves()

def apply_color(rgba, biome, group):
    r,g,b,a = rgba

    for img in os.listdir(f'./input/block/{group}'):
        output = get_color_applied_img(Image.open(f'./input/block/{group}/{img}').convert('RGBA'), (r, g, b, 255))
        if img == 'grass_block_side_overlay.png':
            output = merge_grass_block_side(Image.open(f'./input/grass_block_side.png').convert('RGBA'), output)

        parent_path = f'./output/{biome}/{group}'
        path = f'{parent_path}/{img}'
        os.makedirs(parent_path, exist_ok=True)
        output.save(path)
        print(f'saved: {path}')


def get_natural_color(temperature, downfall, colormap):
    x = 255.0 * (1.0 - temperature)
    y = 255.0 * (1.0 - downfall * temperature)
    return colormap.getpixel((int(x), int(y)))

def get_color_applied_img(img, base_color):
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r,g,b,a = img.getpixel((x, y))
            r *= base_color[0] / 255.0
            g *= base_color[1] / 255.0
            b *= base_color[2] / 255.0

            img.putpixel((x, y), (int(r), int(g), int(b), a))
    return img

def merge_grass_block_side(img, overlay):
    for x in range(overlay.size[0]):
        for y in range(overlay.size[1]):
            rgba = overlay.getpixel((x, y))
            if rgba[3] == 255:
                img.putpixel((x, y), rgba)
    return img

except_keys = {
        'grass': ['grass_color_modifier', 'grass_color'],
        'foliage': ['foliage_color_modifier', 'foliage_color'],
        'dry_foliage': ['dry_foliage_color'],
    }

def apply_natural_color(group):
    ex_keyset = set(except_keys[group])
    colormap = Image.open(f'./input/colormap/{group}.png').convert('RGBA')

    for biome in os.listdir('./input/biome'):
        json_open = open(f'./input/biome/{biome}', 'r')
        json_read = json.load(json_open)
        biome_name = os.path.splitext(biome)[0]

        if ex_keyset.isdisjoint(json_read['effects']):
            temperature = json_read['temperature']
            downfall = json_read['downfall']

            #clamp
            if temperature > 1.0:
                temperature = 1.0
            elif temperature < 0.0:
                temperature = 0.0

            rgba = get_natural_color(temperature, downfall, colormap)
            apply_color(rgba, biome_name, group)
        else:
            ex_key = (set(json_read['effects']) & ex_keyset).pop()
            hex_code = json_read['effects'][ex_key]

            if not hex_code.startswith('#'):
                print(f'skipped: {biome_name} (group: {group})')
                continue

            hex_code = hex_code.split('#')[1]
            r, g, b = hex2rgb(hex_code)
            apply_color((r,g,b,255), biome_name, group)

def hex2rgb(hex_code):
    return [int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)]

def apply_birch_leaves():
    r, g, b = hex2rgb('80a755')
    apply_color((r,g,b,255), 'birch_leaves', 'birch_leaves')

def apply_spruce_leaves():
    r, g, b = hex2rgb('619961')
    apply_color((r,g,b,255), 'spruce_leaves', 'spruce_leaves')

def apply_swamp_grass1():
    r, g, b = hex2rgb('4c763c')
    apply_color((r,g,b,255), 'swamp', 'grass')

def apply_swamp_grass2():
    r, g, b = hex2rgb('6a7039')
    apply_color((r,g,b,255), 'swamp', 'grass')

def apply_dark_forest_grass():
    temperature = 0.7
    downfall = 0.8
    colormap = Image.open(f'./input/colormap/grass.png').convert('RGBA')

    r1, g1, b1 = hex2rgb('28340a')
    r2, g2, b2, a = get_natural_color(temperature, downfall, colormap)
    rgba = ((r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2, a)

    apply_color(rgba, 'dark_forest', 'grass')


if __name__ == '__main__':
    main()
