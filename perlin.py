import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from random import randint

noct = 10
nseed = randint(1,100)
xpix, ypix = 200, 200

noise = PerlinNoise(octaves = noct, seed = nseed)
pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

plt.imshow(pic, cmap='gray')
plt.title(f"Perlin noise generated with seed {nseed}")
plt.show()

#print(f"Perlin noise generated with seed {nseed}")