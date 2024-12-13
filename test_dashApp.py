# Author: Jose Martinez-Ponce
# Purpose: To test the functions of the program

import pytest
from perlinMapGen import PerlinMap
from FileProcess import PerlinFile


# Test 1: File I/O
def test_file_reading():
    file_content = """seed1:11
    seed2: 21
    oct1: 1
    oct2: 14
    size: 300"""

    processor = PerlinFile(file_content)
    params = processor.read_file()
    assert params == {
        "seed1": 11,
        "seed2": 21,
        "oct1": 1,
        "oct2": 14,
        "size": 300
    }


# Test 2: Perlin Map Generation
def test_perlin_map_generation():
    perlin_map = PerlinMap(size=300, seed1=11, seed2=21, oct1=1, oct2=14)
    perlin_noise, seed = perlin_map.generate_perlin()
    assert perlin_noise is not None
    assert isinstance(seed, str)


# Test 3: 2D Map Generation
def test_display_2d_map():
    perlin_map = PerlinMap(size=300, seed1=11, seed2=21, oct1=1, oct2=14)
    perlin_map.generate_perlin()
    fig = perlin_map.display_2d()
    assert fig is not None


# Test 4: Verify upload process
def test_upload_process():
    file_content = """seed1: 15
    seed2: 25
    oct1: 2
    oct2: 16
    size: 400"""

    processor = PerlinFile(file_content)
    params = processor.read_file()
    # check first two params
    assert params["seed1"] == 15
    assert params["seed2"] == 25


# Test 5: Map export
def test_map_export():
    perlin_map = PerlinMap(size=300, seed1=11, seed2=21, oct1=1, oct2=14)
    perlin_map.generate_perlin()
    # export map
    try:
        perlin_map.exportmesh(len_side=60)
        successful_export = True
    except Exception as e:
        print(f"Export failed: {e}")
        successful_export = False
    assert successful_export
