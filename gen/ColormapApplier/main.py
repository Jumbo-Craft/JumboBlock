import json
import os
import numpy as np

from PIL import Image


def main():
    apply_natural_color('grass')
    apply_natural_color('foliage')
    apply_natural_color('dry_foliage')
    #apply_badlands()
    #apply_swamp()
    #apply_mangrove_swamp()
    #apply_dark_forest()

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

def apply_natural_color(group):
    except_keys = {
        'grass': ['grass_color_modifier', 'grass_color'],
        'foliage': ['foliage_color_modifier', 'foliage_color'],
        'dry_foliage': ['dry_foliage_color'],
    }
    colormap = Image.open(f'./input/colormap/{group}.png').convert('RGBA')

    for biome in os.listdir('./input/biome'):
        json_open = open(f'./input/biome/{biome}', 'r')
        json_read = json.load(json_open)

        if set(except_keys[group]).isdisjoint(json_read['effects']):
            temperature = json_read['temperature']
            downfall = json_read['downfall']

            #clamp
            if temperature > 1.0:
                temperature = 1.0
            elif temperature < 0.0:
                temperature = 0.0

            rgba = get_natural_color(temperature, downfall, colormap)
            biome_name = os.path.splitext(biome)[0]
            apply_color(rgba, biome_name, group)
        else:
            print(f'skipped: {biome} (group: {group})')

def apply_badlands(group):
    hex_code = '90814d'
    r,g,b = [int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)]
    apply_color((r,g,b,255), 'badlands', group)

def apply_swamp(group):
    hex_code = '6a7039'
    r,g,b = [int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)]
    apply_color((r,g,b,255), 'swamp', group)

def apply_mangrove_swamp(group):
    hex_code = '6a7039'
    r,g,b = [int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)]
    apply_color((r,g,b,255), 'mangrove_swamp', group)

def apply_dark_forest(group):
    temperature = 0.7
    downfall = 0.8

    hex_code = '28340a'
    r1,g1,b1 = np.array([int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)])
    r2, g2, b2, a = get_natural_color(temperature, downfall)
    rgba = ((r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2, a)

    apply_color(rgba, 'dark_forest', group)


if __name__ == '__main__':
    main()
