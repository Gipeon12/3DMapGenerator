# Author: Noé Pigret
# Date: 11/15/2024
# Description: This program will help the user to generate a 3D map featuring perlin noise,
# from a set of parameters given in the constructor of a dedicated class. Different options are
# available as well as 2D and 3D outputs.


from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import plotly.graph_objects as go


# This dictionary lists all possible options for choosing map density.
# The floating numbers are offsets used in a call of the int() function. 
denstags = {"sparse":0.2, "medium":0.3, "dense":0.4}


def generPerlin(size = 600):
    """
    This function will generate a large perlin noise as a square map from a given size.
    To avoid any spatial repetition in larger maps, two perlin noise generated with 
    different seeds are superposed by sum, with one of them being transposed.

    Parameters
    ----------
    size : INTEGER, optional
        Size of the square map in pixels. The default value is 600.

    Returns
    -------
    perlin : LIST
        2D List of values of each pixel.
    seed : STRING
        Combined seed written from the seeds of the two superposed perlin noise,
        with special formatting "111t2222".
    """
    s1 = rd.randint(1, 1000)
    s2 = rd.randint(1001, 2000) # We ensure there is no chanche for the seeds to be the same.
    noise1 = PerlinNoise(octaves = 20, seed = s1)
    noise2 = PerlinNoise(octaves = 20, seed = s2)
    subpic = [[noise1([i/size, j/size]) for j in range(size)] for i in range(size)]
    suppic = [[noise2([i/size, j/size]) for j in range(size)] for i in range(size)]
    perlin = [[subpic[i][j]+suppic[j][i] for j in range(size)] for i in range(size)]
    seed = f"{s1}t{s2}"
    print(f"Perlin noise of size {size} generated with seed {seed}.")
    return perlin, seed


def perlin2map(perlin, topography = False, density = "medium"):
    """
    This function will convert a given perlin noise into a 2D map,
    taking into account topography (presence or not of irregular ground)
    and density (more or fewer obstacles).

    Parameters
    ----------
    perlin : LIST
        2D List of values of each pixel.
    topography : BOOLEAN, optional
        Boolean indicating whether the output should include uneven ground.
        The default value is False (binary map).
    density : STRING, optional
        Density option label (low = "sparse", "medium", high = "dense").
        The default option is "medium".

    Returns
    -------
    pmap : LIST
        2D List of values of each pixel after conversion and scaling between 0 and 1.
    """
    pmap = []
    dens = denstags[density]
    if topography:
        resize = 1/(3*(1-dens))  # Height difference of accessible surface equals to one third of total height.
        for row in perlin:
            maxi, mini = max(row), min(row)
            pmaprow = []
            for i in range(len(row)) :
                val = (row[i]-mini)/(maxi-mini)
                pmaprow += [int(val + dens) + resize*(1 - int(val + dens))*val,]
            pmap += [pmaprow,]
        print(f"Topographic map generated from perlin noise with density set on: {density}.")
    else:
        for row in perlin:
            maxi, mini = max(row), min(row)
            pmaprow = []
            for i in range(len(row)) :
                val = (row[i]-mini)/(maxi-mini)
                pmaprow += [int(val + dens),]
            pmap += [pmaprow,]
        print(f"Binary map generated from perlin noise with density set on: {density}.")
    return pmap


def disp2Dmap(pmap, seed):
    fig2D = plt.figure()
    plt.imshow(pmap, cmap='gray')
    plt.title(f"Map generated from perlin noise with seed {seed}.")
    plt.gca().invert_yaxis()
    plt.show()
    return fig2D


def disp3Dmap(pmap, seed, height = 20):
    Z = np.array(pmap)*height
    fig = go.Figure(data = [go.Surface(z = Z, colorscale = 'Viridis')])
    fig.update_layout(
        title = f"3D map generated from perlin noise with seed {seed}.",
        scene = dict(
            aspectmode = "cube",
            xaxis = dict(visible = False),
            yaxis = dict(visible = False),
            zaxis = dict(range = [0, len(pmap)], visible = False)
        )
    )
    fig.show(renderer = "browser")


class PerlinMap():
    
    def __init__(self, size = 600, topography = False, density = "medium", height = 20):
        """
        Calling the constructor will automatically generate a map based on perlin noise
        from all the given arguments.

        Parameters
        ----------
        size : INTEGER, optional
            Size of the square map in pixels. The default value is 600.
        topography : BOOLEAN, optional
            Boolean indicating whether the output should include uneven ground.
            The default value is False (binary map).
        density : STRING, optional
            Density option label (low = "sparse", "medium", high = "dense").
            The default option is "medium".
        height : INTEGER, optional
            Height of the 3D map in pixel units. The default value is 20.

        Returns
        -------
        None.
        """
        self.__size = size
        self.__height = height
        self.__zrat = height/size
        self.__denstag = density
        self.__topo = "ON" if topography else "OFF"
        (self.__perlin, self.__seed) = generPerlin(size)
        self.__pmap = perlin2map(self.__perlin, topography, density)
    
    def display(self):
        self.__fig2D = disp2Dmap(self.__pmap, self.__seed)
        disp3Dmap(self.__pmap, self.__seed, self.__height)
        
    def outperlin(self):
        fig = plt.figure()
        plt.imshow(self.__perlin, cmap = 'gray')
        plt.title(f"Perlin noise generated with seed {self.__seed}.")
        plt.gca().invert_yaxis()
        plt.show()
        return fig
        
    def __str__(self):
        return f"Map generated with seed {self.__seed}.\nSize (pixels): {self.__size}\nHeight (px-units): {self.__height}\nDensity: {self.__denstag}\nTopography: {self.__topo}"
    