# Author: Noé Pigret
# Date: 11/15/2024
# Description: This program will help the user to generate a 3D map featuring perlin noise,
# from a set of parameters given in the constructor of a dedicated class. Different options are
# available as well as 2D/3D outputs and mesh exportation.


# Edited by Jose Martinez-Ponce
# Date: 12/6/2024
# Purpose: Allow it to function within the Dash App
=======



from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
import random as rd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import trimesh
import os


# This dictionary lists all possible options for choosing map density.
# The floating numbers are offsets used in a call of the int() function. 
denstags = {"sparse":0.2, "medium":0.3, "dense":0.4}


def normalize(rawMap):
    maxima = [max(row) for row in rawMap]
    minima = [min(row) for row in rawMap]
    M, m = max(maxima), min(minima)
    norMap = []
    for row in rawMap:
        norMap += [[(val-m)/(M-m) for val in row],]
    return norMap


def exponentiate(norMap):
    expMap = []
    for row in norMap:
        expMap += [[(1+np.tanh(10*val-5))/2 for val in row],]
    return expMap


def binarize(norMap, dens, filt = None):
    binMap = []
    if filt == None:
        for row in norMap:
            binMap += [[int(val + dens) for val in row],]
    else:
        for i in range(len(norMap)):
            row = []
            for j in range(len(norMap[i])):
                val, fil = norMap[i][j], filt[i][j]
                row += [int((val + dens)*fil),]
            binMap += [row,]        
    return binMap


def formalize(norMap, dens, filt = None):
    forMap = []
    resize = 1/(3*(1-dens))  # Height difference of accessible surface equals to one third of total height.
    if filt == None:
        for row in norMap:
            forMap += [[int(val + dens) + resize*(1 - int(val + dens))*val for val in row],]
    else:
        for i in range(len(norMap)):
            row = []
            for j in range(len(norMap[i])):
                val, fil = norMap[i][j], filt[i][j]
                level = (val + dens)*fil
                row += [int(level) + resize*(1 - int(level))*val,]
            forMap += [row,] 
    return forMap


def generPerlin(userSeed1 = None, userSeed2 = None, userOct1 = 20, userOct2 = 20, size = 600):
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
        with special formatting "000t1111".
    """

    if userSeed1 is None:
        userSeed1 = rd.randint(1,1000)
    if userSeed2 is None:
        userSeed2 = rd.randint(1001, 2000)

   # s1 = rd.randint(1, 1000)
   # s2 = rd.randint(1001, 2000) # We ensure there is no chance for the seeds to be the same.
    noise1 = PerlinNoise(octaves = userOct1, seed = userSeed1)
    noise2 = PerlinNoise(octaves = userOct2, seed = userSeed2)
    subpic = [[noise1([i/size, j/size]) for j in range(size)] for i in range(size)]
    suppic = [[noise2([i/size, j/size]) for j in range(size)] for i in range(size)]
    perlin = [[subpic[i][j]+suppic[j][i] for j in range(size)] for i in range(size)]
    seed = f"{userSeed1}t{userSeed2}"
    print(f"Perlin noise of size {size} generated with seed {seed}.")
    return np.array(perlin), seed


def perlin2map(perlin, density = "medium", topography = False, disparity = False):
    """
    This function will convert a given perlin noise into a 2D map,
    taking into account density (more or fewer obstacles), topography (presence or not of irregular ground)
    and disparity (some areas are left without obstacles).

    Parameters
    ----------
    perlin : LIST
        2D List of values of each pixel.
    density : STRING (Default) or FLOAT, optional
        Density option label (low = "sparse", "medium", high = "dense").
        The default option is "medium".
    topography : BOOLEAN, optional
        Boolean indicating whether the output should include uneven ground.
        The default value is False (binary map).
    disparity : BOOLEAN, optional
        Boolean indicating whether the outputted map should feature spatial disparities.
        The default value is False (homogeneous distribution of motives).
    
    Returns
    -------
    pmap : LIST
        2D List of values of each pixel after conversion and scaling between 0 and 1.
    """
    dens = denstags[density] if density in denstags else density
    nper = normalize(perlin)
    fseed = None
    efil = None
    if disparity:
        size = len(perlin)
        s = rd.randint(2001,3000)
        noise = PerlinNoise(octaves = 2, seed = s)
        filt = [[noise([i/size, j/size]) for j in range(size)] for i in range(size)]
        fseed = f"f{s}"
        print(f"Density filter map generated with seed {fseed}.")
        nfil = normalize(filt)
        efil = exponentiate(nfil)
    if topography:
        pmap = formalize(nper, dens, efil)
        print(f"Topographic map generated from perlin noise with density set on: {density}.")
    else:
        pmap = binarize(nper, dens, efil)
        print(f"Binary map generated from perlin noise with density set on: {density}.")
    return pmap, fseed


def disp2Dmap(pmap, seed):
    fig = px.imshow(pmap, color_continuous_scale='gray')
    fig.update_layout(
        title={
            'text': f"Map generated from Perlin noise with seed {seed}.",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        coloraxis_showscale=False  # Hide color scale
    )
    return fig


def disp3Dmap(pmap, seed, height = 20):
    Z = np.array(pmap)*height
    fig = go.Figure(data = [go.Surface(z = Z, colorscale = 'Viridis')])
    fig.update_layout(
        title = f"3D map generated from Perlin noise with seed {seed}.",
        scene = dict(
            aspectmode = "cube",
            xaxis = dict(visible = False),
            yaxis = dict(visible = False),
            zaxis = dict(range = [0, len(pmap)], visible = False)
        )
    )
    return fig


def WriteSDF(directory, object_name, model_path, length = 60, height = 2):
    """
    This function is meant to write a basic SDF file for a given object.

    Parameters
    ----------
    directory : STRING
        DESCRIPTION.
    object_name : STRING
        Name used to save the exported object.
    model_path : STRING
        Path to find the STL file of the exported object.
    length : INTEGER, optional
        Side length in meters. The default value is 60.
    height : INTEGER, optional
        Map height in meters. The default value is 2.

    Returns
    -------
    None.


    """
=======
def WriteSDF(directory, object_name, model_path, length = 60, height = 2):
    """
    This function is meant to write a basic SDF file for a given object.

    Parameters
    ----------
    directory : STRING
        DESCRIPTION.
    object_name : STRING
        Name used to save the exported object.
    model_path : STRING
        Path to find the STL file of the exported object.
    length : INTEGER, optional
        Side length in meters. The default value is 60.
    height : INTEGER, optional
        Map height in meters. The default value is 2.

    Returns
    -------
    None.

    """

    sdf_model_file_text = \
    f"""<?xml version='1.0'?>
        <sdf version="1.6">
            <model name="{object_name}">
                <static>1</static>
                <link name="link">
                    <visual name="visual">
                        <geometry>
                            <mesh>
                                <uri>{model_path}</uri>
                                <size>{length} {length} {height}</size>
                            </mesh>
                        </geometry>
                    </visual>
                    <collision name="collision">
                        <geometry>
                            <mesh>
                                <uri>{model_path}</uri>
                                <size>{length} {length} {height}</size>
                            </mesh>
                        </geometry>
                    </collision>
                </link>
            </model>
        </sdf>"""
    # The <visual> component is for rendering graphics and does not affect physics.
    # The <collision> component determines the physical interaction in the simulation but is not rendered visually.
    with open(f"{directory}/{object_name}.sdf", "w") as f:
        f.write(sdf_model_file_text)


def exportMesh(pmap, seed, len_side = 60, zrat = 2/60):
    """
    This function will export the given map as a 3D object (COLLADA file), with a meaningful name inherited
    from the construction parameters. It will also write a SDF file.

    Parameters
    ----------
    pmap : LIST
        2D List of values of each pixel after conversion and scaling between 0 and 1.
    seed : STRING
        Combined seed written from the seeds of the two superposed perlin noise and
        the eventual density filter, with special formatting "000t1111f2222".
    len_side : INTEGER, optional
        Side length in meters. The default value is 60.
    zrat : FLOAT, optional
        Ratio between height and side length. The default value is 2/60.

    Returns
    -------
    None.

    """
    # Create a mesh.
    size = len(pmap)
    height = int(zrat*size)
    heightmap = np.array(pmap) * height
    filename = f"mesh{seed}_h{height}"
    print(f"Generating mesh with name {filename}...")
    x = np.linspace(0, size, size)
    y = np.linspace(0, size, size)
    x, y = np.meshgrid(x, y)
    vertices = np.column_stack((x.ravel(), y.ravel(), heightmap.ravel()))
    # Generate the faces of the grid.
    faces = []
    rows, cols = heightmap.shape
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Indices of vertices in the flattened matrix.
            idx1 = i * cols + j
            idx2 = i * cols + (j + 1)
            idx3 = (i + 1) * cols + j
            idx4 = (i + 1) * cols + (j + 1)
            # Two triangles per cell.
            faces.append([idx1, idx2, idx3])
            faces.append([idx2, idx4, idx3])
    faces = np.array(faces)
    mesh = trimesh.Trimesh(vertices = vertices, faces = faces)
    # Generate a folder to store the mesh.
    print("Generating a folder to save the files.")
    # Generate a folder with the same name as the input file, without its extension.
    current_path = os.getcwd()
    directory = os.path.join(current_path, filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    print("\nApplying scale factor...")
    mesh.apply_scale(scaling = 1.0)
    print("Merging vertices closer than a pre-set constant...")
    mesh.merge_vertices()
    print("Removing duplicate faces...")
    mesh.update_faces(mesh.unique_faces())
    print("Making the mesh watertight...")
    trimesh.repair.fill_holes(mesh)
    trimesh.repair.fix_normals(mesh)
    print("\nMesh volume: {}".format(mesh.volume))
    print("Mesh convex hull volume: {}".format(mesh.convex_hull.volume))
    print("Mesh bounding box volume: {}".format(mesh.bounding_box.volume))
    # Export the DAE file.
    print("\nGenerating the DAE mesh file...")
    dae_file_path = os.path.join(directory, f"{filename}.dae")
    try:    
        trimesh.exchange.export.export_mesh(
            mesh = mesh,
            file_obj = dae_file_path,
            file_type = "dae")
        print(f"Mesh exported successfully to {dae_file_path}")
        # Generate the SDF file.
        print("Generating the SDF file...")
        WriteSDF(
            directory = directory,
            object_name = filename,
            model_path = dae_file_path,
            length = len_side,
            height = int(zrat*len_side))
    except:
        print("\nUnable to export object.")


class PerlinMap():
    
    def __init__(self, size = 600, seed1 = None, seed2 = None, oct1 = 20, oct2 = 20, density = "medium", topography = False, disparity = False, height = 20):
        """
        Calling the constructor will automatically generate a map based on perlin noise
        from all the given arguments.

        Parameters
        ----------
        size : INTEGER, optional
            Size of the square map in pixels. The default value is 600.
        density : STRING (Default) or FLOAT, optional
            Density option label (low = "sparse", "medium", high = "dense").
            The default option is "medium".        
        topography : BOOLEAN, optional
            Boolean indicating whether the output should include uneven ground.
            The default value is False (binary map).
        disparity : BOOLEAN, optional
            Boolean indicating whether the outputted map should feature spatial disparities.
            The default value is False (homogeneous distribution of motives).
        height : INTEGER, optional
            Height of the 3D map in pixel units. The default value is 20.

        Returns
        -------
        None.
        """
        self.__size = size
        self.__seed1 = seed1
        self.__seed2 = seed2
        self.__oct1 = oct1
        self.__oct2 = oct2
        self.__height = height
        self.__zrat = height/size
        self.__dens = density
        self.__topo = topography
        self.__disp = disparity

    def generate_perlin(self, seed1 = None, seed2 = None, oct1 = 20, oct2 = 20, size = 500):
        (self.__perlin, self.__seed) = generPerlin(self.__seed1, self.__seed2, self.__oct1, self.__oct2, self.__size)
        (self.__pmap, self.__fseed) = perlin2map(self.__perlin, self.__dens, self.__topo, self.__disp)
        return self.__perlin, self.__seed
    
    def display_2d(self):
        seed = self.__seed if self.__fseed == None else self.__seed+self.__fseed
        seed += "T" if self.__topo else "F"
        return disp2Dmap(self.__pmap, seed)

    def display_3d(self):
        seed = self.__seed if self.__fseed is None else self.__seed + self.__fseed
        seed += "T" if self.__topo else "F"
        return disp3Dmap(self.__pmap, seed, self.__height)
    
    def exportmesh(self, len_side = 60):
        seed = self.__seed if self.__fseed == None else self.__seed+self.__fseed
        seed += "T" if self.__topo else "F"
        exportMesh(self.__pmap, seed, len_side, self.__zrat)
        
    def outperlin(self):
        fig = plt.figure()
        plt.imshow(self.__perlin, cmap = 'gray')
        plt.title(f"Perlin noise generated with seed {self.__seed}.")
        plt.gca().invert_yaxis()
        plt.show()
        return fig
    def get_seed(self):
        seed = f"{self.__seed1}t{self.__seed2}"
        return seed



        
    def __str__(self):
        topo = "ON" if self.__topo else "OFF"
        disp = "ON" if self.__disp else "OFF"
        return f"Map generated with seed {self.__seed}.\nSize (pixels): {self.__size}\nHeight (px-units): {self.__height}\nDensity: {self.__dens}\nTopography: {topo}\nDisparity: {disp}"
    
