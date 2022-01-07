from PIL import Image
from CONSTANTS import *


def picture_to_matrix():
    file_name = f"data/{MAP_NAME}"
    map_list = []

    im = Image.open(file_name)
    pixels = im.load()
    x, y = im.size

    for i in range(x):
        layer = []
        for j in range(y):
            layer.append(BLOCKS[pixels[i, j]])
        map_list.append(layer)

    return map_list
