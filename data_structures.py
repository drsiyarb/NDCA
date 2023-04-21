import numpy as np


class Grid:

    def __init__(self, n, x, decay_value, lower_tresh, upper_tresh, density,
                 input_bias, output_bias, radio_bias):
        self.array = np.zeros([x] * n)
        self.decay_value = decay_value
        self.lower_tresh = lower_tresh
        self.upper_tresh = upper_tresh
        self.density = density
        self.input_bias = input_bias
        self.output_bias = output_bias
        self.radio_bias = radio_bias


class Drid:

    def __init__(self, grid, cell_dict):
        self.grid = grid
        self.cell_dict = cell_dict


def create_cell_dict(grid):
    cell_dict = {}
    cell_count = 1

    for index in np.ndindex(grid.array.shape):
        cell_key = f'cell{cell_count}'
        cell_dict[cell_key] = index
        cell_count += 1

    return Drid(grid, cell_dict)


def get_local_neighbors(array, index):
    neighbors = []
    for offset in np.ndindex(*([3] * array.ndim)):
        neighbor_index = tuple(i + o - 1 for i, o in zip(index, offset))
        if any(i < 0 or i >= s for i, s in zip(neighbor_index, array.shape)):
            continue
        if neighbor_index == index:
            continue
        neighbors.append(neighbor_index)
    return neighbors


def add_local_neighbors(grid_with_dict):
    for cell_key, cell_index in grid_with_dict.cell_dict.items():
        local_neighbors = get_local_neighbors(grid_with_dict.grid.array,
                                              cell_index)
        grid_with_dict.cell_dict[cell_key] = (cell_index, local_neighbors)


class Column:

    def __init__(self, num_io, num_radio):
        self.drids = []
        self.num_io = num_io
        self.num_radio = num_radio

    def add_drid(self, drid):
        self.drids.append(drid)

    def process_drids_simultaneously(self, operation):
        for drid in self.drids:
            operation(drid)

    def process_drids_one_by_one(self, operation):
        for drid in self.drids:
            operation(drid)
            print(f"Processed {drid}")
