# Author: Noé Pigret
# Date: 12/2/2024
# Description: This program is designed to export a mesh file as STL and write
# a SDF file for a random map generated from Perlin noise.
# Inspired by https://github.com/heap-chist-era/stl2sdf

import os
import trimesh
import numpy as np


def WriteSDF(directory, object_name, model_stl_path, scale_factor = 1.0):
    scale_factor = str(round(scale_factor, 3))
    sdf_model_file_text = \
    f"""<?xml version='1.0'?>
            <sdf version="1.6">
                <model name="{object_name}">
                    <static>1</static>
                    <link name="link">
                        <visual name="visual">
                            <geometry>
                                <mesh>
                                    <uri>{model_stl_path}</uri>
                                    <scale>{scale_factor} {scale_factor} {scale_factor}</scale>
                                </mesh>
                            </geometry>
                        </visual>
                        <collision name="collision">
                            <geometry>
                                <mesh>
                                    <uri>{model_stl_path}</uri>
                                    <scale>{scale_factor} {scale_factor} {scale_factor}</scale>
                                </mesh>
                            </geometry>
                        </collision>
                    </link>
                </model>
            </sdf>"""
    with open(f"{directory}/{object_name}.sdf", "w") as f:
        f.write(sdf_model_file_text)



def exportMesh(pmap, seed, height = 20, scaling_factor = 1.0):
    filename = f"mesh{seed}_h{height}"
    # Create a mesh.
    print(f"Generating mesh with name {filename}...")
    heightmap = np.array(pmap)*height
    size = heightmap.shape[0]
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
    currentPathGlobal = os.getcwd()
    directory = currentPathGlobal + "/" + filename.split(".")[0]
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    print("\nApplying scale factor...")
    mesh.apply_scale(scaling = scaling_factor)
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
    
    print("\nGenerating the STL mesh file...")
    trimesh.exchange.export.export_mesh(
        mesh = mesh,
        file_obj = directory + f"/{filename}.stl",
        file_type = "stl")
    print("Generating the SDF file...")
    WriteSDF(
        directory = directory,
        object_name = filename,
        model_stl_path = directory + f"/{filename}.stl",
        scale_factor = 1.0)
