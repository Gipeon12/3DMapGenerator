# Author: Noé Pigret
# Date: 12/2/2024
# Description: This program is designed to export a mesh file as DAE (Collada) and write
# a SDF file for a random map generated from Perlin noise.
# Inspired by https://github.com/heap-chist-era/stl2sdf

import os
import trimesh
import numpy as np


def WriteSDF(directory, object_name, model_path, length = 60, height = 2):
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