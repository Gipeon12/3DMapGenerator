import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from random import randint
import numpy as np
import plotly.graph_objects as go

noct = 20  # A higher number of octaves will generate smaller patterns.
nseed = randint(1,1000)  # Random integer to define the seed.
# octaves (float) : number of sub rectangles in each [0, 1] range.
# seed : specific seed with which you want to initialize random generator.

pix = 600
xpix, ypix = pix, pix  # Definition in pixels of the perlin map.
# Square maps are preferred.

zrat = 1/30  # Vertical dimension of the map in relation to the horizontal dimension.
dens = 0.3  # Density ratio of the map. The lower the density, the fewer the obstacles.
# 0.2:Sparse ; 0.3:Medium ; 0.4:Dense
resize = 1/(3*(1-dens))  # The height difference of the accessible surface will always be equal to one third of the total height of the card.

noise = PerlinNoise(octaves = noct, seed = nseed)
#pic = [[noise([i/xpix, j/ypix]) for j in range(xpix)] for i in range(ypix)]

pic = []
for i in range(ypix):
    row = [noise([i/xpix, j/ypix]) for j in range(xpix)]
    maxi, mini = max(row), min(row)
    maprow = []
    for k in range(len(row)) :
        val = (row[k]-mini)/(maxi-mini)
        maprow += [int(val + dens) + resize*(1 - int(val + dens))*val,]
    pic += [maprow,]

Z = np.array(pic)*pix*zrat

fig = go.Figure(data = [go.Surface(z = Z, colorscale = 'Viridis')])

fig.update_layout(
    title = f"Topographic map generated from perlin noise with seed {nseed}",
    scene = dict(
        aspectmode="cube",
        xaxis = dict(visible = False),
        yaxis = dict(visible = False),
        zaxis = dict(range = [0, pix], visible = False)
    )
)

fig.show(renderer="browser")