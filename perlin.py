from perlin_noise import PerlinNoise
from random import randint


def generatePerlin(seed=None, noct=None, xDim=100, yDim=100):

    # noct = 20  # A higher number of octaves will generate smaller patterns.
    # octaves (float) : number of sub rectangles in each [0, 1] range.
    # seed : specific seed with which you want to initialize random generator.

    # xpix, ypix = 200, 200  # Definition in pixels of the perlin map.
    # Square maps are preferred.


    if seed is None:
        seed = randint(1, 1000)
    if noct is None:
        noct = 20 # Default Num

    noise = PerlinNoise(octaves = noct, seed = seed)
    pic = [[noise([i/xDim, j/yDim]) for j in range(xDim)] for i in range(yDim)]

    binarpic = []
    for row in pic:  # Convert smooth map into binary map, using a threshold of 0.7.
        maxi, mini = max(row), min(row)
        binarow = [round((row[i]-mini)/(maxi-mini)-0.2) for i in range(len(row))]
        binarpic += [binarow,]

    return binarpic