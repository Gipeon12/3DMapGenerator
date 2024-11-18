# Author: Noé Pigret
# Date: 11/13/2024
# Description: This program will generate a topographic map from perlin noise,
# featuring obstacles (level = 1) and an uneven ground (elevation differences).


import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from random import randint

noct = 20  # A higher number of octaves will generate smaller patterns.
nseed = randint(1,1000)  # Random integer to define the seed.
# octaves (float) : number of sub rectangles in each [0, 1] range.
# seed : specific seed with which you want to initialize random generator.

xpix, ypix = 600, 600  # Definition in pixels of the perlin map.
# Square maps are preferred.

noise = PerlinNoise(octaves = noct, seed = nseed)
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

topopic = []
for row in pic:  # Convert smooth map into topographic map, using a threshold of 0.65.
    maxi, mini = max(row), min(row)
    binarow = []
    for i in range(len(row)) :
        val = (row[i]-mini)/(maxi-mini)
        binarow += [max(val,int(val + 0.4)),]
    topopic += [binarow,]

plt.imshow(topopic, cmap='gray')
plt.title(f"Topographic map generated from perlin noise with seed {nseed}")

plt.show()