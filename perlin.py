import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from random import randint

noct = 10  # A higher number of octaves will generate smaller patterns.
nseed = randint(1,100)
xpix, ypix = 400, 400

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
