# This is a sample Python script.
import json
import os
import numpy as np

from PIL import Image

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

colormap = Image.open('./input/grass.png').convert('RGBA')

def main():
    apply_natural_color()
    apply_badlands()
    apply_swamp()
    apply_mangrove_swamp()
    apply_dark_forest()

def apply_natural_color():
    for img in os.listdir('./input/block'):
        for biome in os.listdir('./input/biome'):
            json_open = open(f'./input/biome/{biome}', 'r')
            json_read = json.load(json_open)

            if 'grass_color_modifier' or 'grass_color' in json_read['effects']:
                print(f'skipped: {img} in {biome}')
            else:
                temperature = json_read['temperature']
                downfall = json_read['downfall']

                #clamp
                if temperature > 1.0:
                    temperature = 1.0
                elif temperature < 0.0:
                  temperature = 0.0

                rgba = get_natural_color(temperature, downfall)
                biome_name = os.path.splitext(biome)[0]
                apply_color(rgba, biome_name)

def apply_badlands():
    hex_code = '90814d'
    r,g,b = [int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)]
    apply_color((r,g,b,255), 'badlands')

def apply_swamp():
    hex_code = '6A7039'
    r,g,b = [int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)]
    apply_color((r,g,b,255), 'swamp')

def apply_mangrove_swamp():
    hex_code = '6A7039'
    r,g,b = [int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)]
    apply_color((r,g,b,255), 'mangrove_swamp')

def apply_dark_forest():
    temperature = 0.7
    downfall = 0.8

    hex_code = '28340A'
    r1,g1,b1 = np.array([int(hex_code[i:i + 2], 16) for i in range(0, 6, 2)])
    r2, g2, b2, a = get_natural_color(temperature, downfall)
    rgba = ((r1 + r2) // 2, (g1 + g2) // 2, (b1 + b2) // 2, a)

    apply_color(rgba, 'dark_forest')

def apply_color(rgba, biome):
    r,g,b,a = rgba

    for img in os.listdir('./input/block'):
        output = get_color_applied_img(Image.open(f'./input/block/{img}').convert('RGBA'), (r, g, b, 255))
        if img == 'grass_block_side_overlay.png':
            output = merge_grass_block_side(Image.open(f'./input/grass_block_side.png').convert('RGBA'), output)
        save(img, output, biome)

def get_natural_color(temperature, downfall):
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

def save(input_img, output_img, biome_name):
    os.makedirs(f'./output/{biome_name}', exist_ok=True)
    path = f'./output/{biome_name}/{input_img}'
    output_img.save(path)
    print(f'saved: {path}')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
