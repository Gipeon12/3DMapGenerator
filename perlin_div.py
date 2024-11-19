# Author: Noé Pigret
# Date: 11/19/2024
# Description: This program is designed to generate a random map from Perlin noise,
# featuring a wide disparity in the distribution of motives.

import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import random as rd

def normalMap(rawmap):
    maxima = [max(row) for row in rawmap]
    minima = [min(row) for row in rawmap]
    M, m = max(maxima), min(minima)
    normalmap = []
    for row in rawmap:
        normalrow = [(row[i]-m)/(M-m) for i in range(len(row))]
        normalmap += [normalrow,]
    return normalmap

def diverMap(main, div):
    divmap = []
    for j in range(len(main)):
        divrow = []
        for i in range(len(main[j])):
            divrow += [main[j][i]*div[j][i],]
        divmap += [divrow,]
    return divmap

def binarMap(main, offset):
    binmap = []
    for row in main:
        binmap += [[round(val-offset) for val in row],]
    return binmap

def divBinMap(main, div):
    divbin = []
    for j in range(len(main)):
        divbinrow = []
        for i in range(len(main[j])):
            divbinrow += [int(main[j][i]-(div[j][i]-0.5)),]
        divbin += [divbinrow,]
    return divbin

size = 400

s1 = rd.randint(1, 1000)
s2 = rd.randint(1001, 2000)
s3 = rd.randint(2001,3000)
noise1 = PerlinNoise(octaves = 20, seed = s1)
noise2 = PerlinNoise(octaves = 20, seed = s2)
noise3 = PerlinNoise(octaves = 2, seed = s3)
subpic = [[noise1([i/size, j/size]) for j in range(size)] for i in range(size)]
suppic = [[noise2([i/size, j/size]) for j in range(size)] for i in range(size)]
divpic = [[noise3([i/size, j/size]) for j in range(size)] for i in range(size)]
perlin = [[subpic[i][j]+suppic[j][i] for j in range(size)] for i in range(size)]


normperlin = normalMap(perlin)
normdiv = normalMap(divpic)
#divmap = diverMap(normperlin,normdiv)
#binmap = binarMap(divmap,0)
divbin = divBinMap(normperlin,normdiv)

fig, axs = plt.subplots(1, 3)

axs[0].imshow(normperlin, cmap='gray')
axs[0].set_title(f"Perlin map of seed {s1}t{s2}.")
axs[1].imshow(normdiv, cmap='gray')
axs[1].set_title(f"Density divergence map of seed {s3}.")
axs[2].imshow(divbin, cmap='gray')
axs[2].set_title("Binarized map with density divergence.")
#axs[1,0].imshow(divmap, cmap='gray')
#axs[1,0].set_title("Perlin map with density divergence.")
#axs[1,1].imshow(binmap, cmap='gray')
#axs[1,1].set_title("Binarized map with density divergence.")

plt.show()