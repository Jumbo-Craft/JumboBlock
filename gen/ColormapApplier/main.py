# This is a sample Python script.
import json
import os

from PIL import Image

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def main():
    colormap = Image.open('./input/grass.png').convert('RGBA')

    for img in os.listdir('./input/block'):
        for biome in os.listdir('./input/biome'):
            json_open = open(f'./input/biome/{biome}', 'r')
            json_read = json.load(json_open)

            if 'grass_color_modifier' not in json_read['effects']:
                temperature = json_read['temperature']
                downfall = json_read['downfall']

                #clamp
                if temperature > 1.0:
                    temperature = 1.0
                elif temperature < 0.0:
                  temperature = 0.0

                x = 255.0 * (1.0 - temperature)
                y = 255.0 * (1.0 - downfall * temperature)

                r,g,b,a = colormap.getpixel((int(x), int(y)))
                output = apply_colors(Image.open(f'./input/block/{img}').convert('RGBA'), (r, g, b, a))

                if img == 'grass_block_side_overlay.png':
                    output = merge_grass_block_side(Image.open(f'./input/grass_block_side.png').convert('RGBA'), output)

                biome_name = os.path.splitext(biome)[0]
                os.makedirs(f'./output/{biome_name}', exist_ok=True)
                path = f'./output/{biome_name}/{img}'
                output.save(path)
                print(f'saved: {path}')


def apply_colors(img, base_color):
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
