# Author: Noé Pigret
# Date: 11/13/2024
# Description: This program will generate a binary map from perlin noise,
# featuring obstacles (level = 1) and a flat floor (level = 0).


import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from random import randint

noct = 20  # A higher number of octaves will generate smaller patterns.
nseed = randint(1,1000)  # Random integer to define the seed.
# octaves (float) : number of sub rectangles in each [0, 1] range.
# seed : specific seed with which you want to initialize random generator.

xpix, ypix = 200, 200  # Definition in pixels of the perlin map.
# Square maps are preferred.

noise = PerlinNoise(octaves = noct, seed = nseed)
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

binarpic = []
for row in pic:  # Convert smooth map into binary map, using a threshold of 0.7.
    maxi, mini = max(row), min(row)
    binarow = [round((row[i]-mini)/(maxi-mini)-0.2) for i in range(len(row))]
    binarpic += [binarow,]

#plt.imshow(pic, cmap='gray')
#plt.title(f"Perlin noise generated with seed {nseed}")

plt.imshow(binarpic, cmap='gray')
plt.title(f"Binary map generated from perlin noise with seed {nseed}")

plt.show()

#print(f"Perlin noise generated with seed {nseed}")