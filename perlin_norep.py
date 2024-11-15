# This program is designed to generate a larger random map without any spatial
# repetition. Two large perlin maps with different seeds are superposed by sum,
# with one of them being transposed.

import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import random as rd

s1 = rd.randint(1,1000)
s2 = rd.randint(1001,2000) # We ensure there is no chanche for the seeds to be the same.

xpix, ypix = 400, 400

noise = PerlinNoise(octaves=20, seed=s1)
filnoise = PerlinNoise(octaves=20, seed=s2)

pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
filpic = [[filnoise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]
tfilpic = [list(row) for row in zip(*filpic)]
crosspic = [[pic[i][j]*tfilpic[i][j] for j in range(xpix)] for i in range(ypix)]
sumpic = [[pic[i][j]+tfilpic[i][j] for j in range(xpix)] for i in range(ypix)]

fig, axs = plt.subplots(2, 2)

axs[0, 0].imshow(pic, cmap='gray')
axs[0, 0].set_title(f"Random map 1 with seed {s1}")
axs[0, 1].imshow(tfilpic, cmap='gray')
axs[0, 1].set_title(f"Transposed random map 2 with seed {s2}") 
axs[1, 0].imshow(crosspic, cmap='gray')
axs[1, 0].set_title("Superposition of both as a product")
axs[1, 1].imshow(sumpic, cmap='gray')
axs[1, 1].set_title("Superposition of both as a sum")

binarsum = []
for row in sumpic:  # Convert smooth map into binary map, using a threshold of 0.7.
    maxi, mini = max(row), min(row)
    binarow = [round((row[i]-mini)/(maxi-mini)-0.2) for i in range(len(row))]
    binarsum += [binarow,]

plt.figure(2)
plt.imshow(binarsum, cmap='gray')
plt.title("Binarized sum map")

plt.show()