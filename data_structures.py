import numpy as np
import logging


class Grid:

    def __init__(self, ndim, size, decay_value, lower_tresh, upper_tresh,
                 density, input_bias, output_bias, radio_bias):
        self.array = np.zeros([size] * ndim)
        self.decay_value = decay_value
        self.lower_tresh = lower_tresh
        self.upper_tresh = upper_tresh
        self.density = density
        self.input_bias = input_bias
        self.output_bias = output_bias
        self.radio_bias = radio_bias


class Drid:

    def __init__(self, grid):
        self.grid = grid
        self.cell_dict = {}

        cell_count = 0
        for i in np.ndindex(grid.array.shape):
            self.cell_dict[f'cell{cell_count}'] = i
            cell_count += 1

        self.add_local_neighbors()


    def get_local_neighbors(self, index):
        neighbors = []
        shape = self.grid.array.shape
        # FIXME: don't hardcode the dimensions here:
        # for offset in np.ndindex(*([3] * array.ndim)):
        for offset in np.ndindex(shape):
            neighbor_index = tuple(i + o - 1 for i, o in zip(index, offset))
            # throw out > boundary conditions
            if any(i < 0 or i >= s for i, s in zip(neighbor_index, shape)):
                continue
            if neighbor_index == index:
                continue
            neighbors.append(neighbor_index)
        return neighbors


    def add_local_neighbors(self):
        for cell_key, cell_index in self.cell_dict.items():
            local_neighbors = self.get_local_neighbors(cell_index)
            # this overwrites the cell_index with a tuple containing neighbors
            self.cell_dict[cell_key] = (cell_index, local_neighbors)


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
            logging.debug(f"Processed {drid}")
