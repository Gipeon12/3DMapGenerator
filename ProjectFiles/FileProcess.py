# Author: Jose Martinez-Ponce
# Purpose: To take in a file input and allow that to generate a perlin map
from perlinMapGen import PerlinMap


class PerlinFile:
    def __init__(self, file_content):

        self.file_content = file_content
        self.parameters = self.read_file()

    def read_file(self):
        required_keys = ["seed1", "seed2", "oct1", "oct2", "size"]
        params = {}

        # Split lines and read key-value pairs
        lines = self.file_content.strip().split("\n")
        # print(f"File lines: {lines}") # debug
        for line in lines:
            if ":" in line:
                key, value = line.split(":")
                key, value = key.strip(), value.strip()
                params[key] = int(value)
                # print(f"Read key-value: {key} = {value}")  # debug

        # Check for missing keys
        for key in required_keys:
            if key not in params:
                # print(f"Missing key: {key}")  # debug
                raise ValueError(f"Missing required parameter! : {key}")

        # print(f"Successfully read parameters: {params}")  # debug
        return params

    def create_perlin_map(self):
        params = self.parameters
        perlin_map = PerlinMap(
            size=params["size"],
            seed1=params["seed1"],
            seed2=params["seed2"],
            oct1=params["oct1"],
            oct2=params["oct2"],
        )
        return perlin_map
