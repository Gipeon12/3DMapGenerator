# Author: Noé Pigret
# Date: 11/19/2024
# Description: This program is designed to generate a random map from Perlin noise,
# featuring a wide disparity in the distribution of motives.

import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
import random as rd
import numpy as np

def normalMap(rawmap):
    maxima = [max(row) for row in rawmap]
    minima = [min(row) for row in rawmap]
    M, m = max(maxima), min(minima)
    normalmap = []
    for row in rawmap:
        normalrow = [(row[i]-m)/(M-m) for i in range(len(row))]
        normalmap += [normalrow,]
    return normalmap

def exponMap(normap):
    expmap = []
    for row in normap:
        exprow = [(1+np.tanh(10*val-5))/2 for val in row]
        expmap += [exprow,]
    return expmap

def divBinMap(main, div, dens):
    divbin = []
    for i in range(len(main)):
        divbinrow = []
        for j in range(len(main[i])):
            divbinrow += [int((main[i][j]+dens)*div[i][j]),]
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
expdiv = exponMap(normdiv)
divbmap = divBinMap(normperlin,expdiv,0.4)

fig, axs = plt.subplots(2, 2)

axs[0,0].imshow(normperlin, cmap='gray')
axs[0,0].set_title(f"Perlin map of seed {s1}t{s2}.")
axs[0,1].imshow(normdiv, cmap='gray')
axs[0,1].set_title(f"Density filter map of seed {s3}.")
axs[1,0].imshow(expdiv, cmap='gray')
axs[1,0].set_title("Filter map with exponentiated values.")
axs[1,1].imshow(divbmap, cmap='gray')
axs[1,1].set_title("Binarized map with density disparities.")

plt.show()