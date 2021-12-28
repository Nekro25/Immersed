from PIL import Image
from CONSTANTS import *

file_name = "./pixil-frame-0.png"
map_list = []

im = Image.open(file_name)
pixels = im.load()
x, y = im.size

for i in range(x):
    layer = []
    for j in range(y):
        layer.append(BLOCKS[pixels[i, j]])
    map_list.append(layer)

print(map_list)