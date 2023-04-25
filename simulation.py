import copy
import logging

import numpy as np
import vtk
from vtk.util import numpy_support

from cell import Cell


def calculate_neighborhood_activation_score(column, cell_info, drid_idx):
    cell, cell_index, local_neighbors, role, code, input_non_local, output_non_local = cell_info
    drid = column.drids[drid_idx]

    # Calculate the neighborhood activation score for local neighbors
    activation_score = 0
    for neighbor_index in local_neighbors:
        neighbor_key = f"cell{np.ravel_multi_index(neighbor_index, drid.grid.array.shape, order='C') + 1}"
        neighbor_cell = drid.cell_dict[neighbor_key][0]
        activation_score += neighbor_cell.activation_state

    # Calculate the neighborhood activation score for non-local input neighbors
    for non_local_info in input_non_local:
        non_local_drid_idx, non_local_cell_key, _ = non_local_info
        non_local_drid = column.drids[non_local_drid_idx]
        non_local_cell = non_local_drid.cell_dict[non_local_cell_key][0]
        activation_score += non_local_cell.activation_state

    # Calculate the neighborhoodactivation score as a factor of activated cells to the total number of neighbors
    total_neighbors = len(local_neighbors) + len(input_non_local)

    if total_neighbors == 0:
        neighborhood_activation_score = 0
    else:
        neighborhood_activation_score = activation_score / total_neighbors

    return neighborhood_activation_score


def count_active_inactive_neighbors(column, cell_info, drid_idx):
    cell, cell_index, local_neighbors, role, code, input_non_local, output_non_local = cell_info
    drid = column.drids[drid_idx]

    active_neighbors = 0
    inactive_neighbors = 0

    # Count active and inactive local neighbors
    for neighbor_index in local_neighbors:
        neighbor_key = f"cell{np.ravel_multi_index(neighbor_index, drid.grid.array.shape) + 1}"
        neighbor_cell = drid.cell_dict[neighbor_key][0]
        if neighbor_cell.activation_state:
            active_neighbors += 1
        else:
            inactive_neighbors += 1

    # Count active and inactive non-local input neighbors
    for non_local_info in input_non_local:
        non_local_drid_idx, non_local_cell_key, _ = non_local_info
        non_local_drid = column.drids[non_local_drid_idx]
        non_local_cell = non_local_drid.cell_dict[non_local_cell_key][0]
        if non_local_cell.activation_state:
            active_neighbors += 1
        else:
            inactive_neighbors += 1

    return active_neighbors, inactive_neighbors


class Worker:

    def __init__(self, column):
        self.column = column

    def process_column(self):
        for drid_idx, drid in enumerate(self.column.drids):
            updated_drid = copy.deepcopy(drid)

            for cell_key, cell_info in drid.cell_dict.items():
                cell, cell_index, local_neighbors, role, code, input_non_local, output_non_local = cell_info

                # Create a copy of the cell to store the updated state
                updated_cell = Cell(cell.voltage, cell.activation_state,
                                    cell.excitability)

                # Check the cell's excitability
                if cell.excitability == 1:
                    if cell.activation_state == 1:
                        updated_cell.excitability = 0
                    else:
                        if cell.voltage > drid.grid.upper_tresh:
                            updated_cell.activation_state = 1
                            updated_cell.voltage = 1
                            updated_cell.excitability = 0
                        else:
                            # Calculate the neighborhood activation score using the new function
                            activation_score = calculate_neighborhood_activation_score(
                                self.column, cell_info, drid_idx)
                            activation_score = activation_score

                            # Add the activation score to the voltage
                            updated_cell.voltage += activation_score

                # If excitability is 0
                if cell.excitability == 0:
                    # Always subtract decay value from the voltage
                    updated_cell.voltage -= drid.grid.decay_value

                    if cell.activation_state == 1:
                        if drid.grid.lower_tresh < cell.voltage <= drid.grid.upper_tresh:
                            updated_cell.activation_state = 0
                        elif cell.voltage <= drid.grid.lower_tresh:
                            updated_cell.excitability = 1

                # Update the cell's dictionary entry with the updated cell instance
                drid.cell_dict[cell_key] = (updated_cell, cell_index,
                                            local_neighbors, role, code,
                                            input_non_local, output_non_local)

            self.column.drids[drid_idx] = updated_drid


class classical_CA_worker:

    def __init__(self, column, max, min):
        self.column = column
        self.max = max
        self.min = min

    def process_column_CA_worker(self):
        for drid_idx, drid in enumerate(self.column.drids):
            logging.debug("drid_idx, drid:", drid_idx, drid)
            updated_drid = copy.deepcopy(drid)
            for cell_key, cell_info in drid.cell_dict.items():
                cell, cell_index, local_neighbors, role, code, input_non_local, output_non_local = cell_info

                # Create a copy of the cell to store the updated state
                updated_cell = Cell(cell.voltage, cell.activation_state,
                                    cell.excitability)
                a_n, i_n = count_active_inactive_neighbors(
                    self.column, cell_info, drid_idx)

                if a_n > self.min and a_n < self.max:
                    updated_cell.activation_state = 1
                else:
                    updated_cell.activation_state = 0

                # Update the cell's dictionary entry with the updated cell instance
                updated_drid.cell_dict[cell_key] = (updated_cell, cell_index,
                                                    local_neighbors, role, code,
                                                    input_non_local,
                                                    output_non_local)

            self.column.drids[drid_idx] = updated_drid


class ResultColumn:

    def __init__(self):
        self.voltage_grids = {}
        self.activation_grids = {}

    def add_voltage_grid(self, drid_idx, grid):
        if drid_idx not in self.voltage_grids:
            self.voltage_grids[drid_idx] = []
        self.voltage_grids[drid_idx].append(grid)

    def add_activation_grid(self, drid_idx, grid):
        if drid_idx not in self.activation_grids:
            self.activation_grids[drid_idx] = []
        self.activation_grids[drid_idx].append(grid)


def run_simulation(column, num_frames, max, min):
    # Initialize the Worker and ResultColumn instances
    worker = classical_CA_worker(column, max, min)
    result_column = ResultColumn()

    # Run the simulation for the specified number of frames
    for frame in range(num_frames):
        # Process the column to update cell states
        worker.process_column_CA_worker()

        # Loop through all drids
        for drid_idx, drid in enumerate(column.drids):
            # Create new grids to store voltage and activation states for this frame
            voltage_grid = np.zeros(drid.grid.array.shape)
            activation_grid = np.zeros(drid.grid.array.shape)

            # Populate the voltage and activation grids with values from the cells
            for cell_key, cell_info in drid.cell_dict.items():
                cell, cell_index = cell_info[0], cell_info[1]
                voltage_grid[cell_index] = cell.voltage
                activation_grid[cell_index] = cell.activation_state

            # Add the new grids to the ResultColumn
            result_column.add_voltage_grid(drid_idx, voltage_grid)
            result_column.add_activation_grid(drid_idx, activation_grid)

    return result_column


def are_grids_different(grid1, grid2, threshold=0.001):
    diff = np.abs(grid1 - grid2)
    max_diff = np.max(diff)
    return max_diff > threshold


def numpy_to_vtk_image_data(numpy_array):
    vtk_image_data = vtk.vtkImageData()
    vtk_image_data.SetDimensions(numpy_array.shape)
    vtk_image_data.SetSpacing(1, 1, 1)
    vtk_image_data.SetOrigin(0, 0, 0)

    vtk_array = numpy_support.numpy_to_vtk(numpy_array.ravel(order='F'),
                                           deep=True,
                                           array_type=vtk.VTK_FLOAT)
    vtk_image_data.GetPointData().SetScalars(vtk_array)

    return vtk_image_data


def save_combined_vti_files(result_column,
                            num_frames,
                            output_folder,
                            offset=10):
    num_drids = len(result_column.activation_grids)
    first_grid_shape = result_column.activation_grids[0][0].shape

    for frame_idx in range(num_frames):
        # Initialize a combined 3D array with zeros, adding extra space for the offsets
        combined_shape = (first_grid_shape[0] + (num_drids - 1) * offset,
                          first_grid_shape[1], first_grid_shape[2])
        combined_array = np.zeros(combined_shape)

        for drid_idx, activation_grids in result_column.activation_grids.items(
        ):
            activation_grid = activation_grids[frame_idx]
            x_start = drid_idx * offset
            x_end = x_start + first_grid_shape[0]

            combined_array[x_start:x_end, :, :] = activation_grid

        # Convert the combined array to a vtkImageData object
        vtk_image_data = vtk.vtkImageData()
        vtk_image_data.SetDimensions(combined_shape[0], combined_shape[1],
                                     combined_shape[2])
        vtk_image_data.SetSpacing(1, 1, 1)

        vtk_array = numpy_support.numpy_to_vtk(combined_array.ravel(),
                                               deep=True,
                                               array_type=vtk.VTK_FLOAT)
        vtk_array.SetName("Activation")
        vtk_image_data.GetPointData().SetScalars(vtk_array)

        # Save the vtkImageData object as a VTI file
        output_file_name = f"{output_folder}/combined_drids_frame_{frame_idx:04d}.vti"
        writer = vtk.vtkXMLImageDataWriter()
        writer.SetFileName(output_file_name)
        writer.SetInputData(vtk_image_data)
        writer.Write()
