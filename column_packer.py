import random
import logging

from data_structures import Column, Grid, Drid


def normalize_io_biases(column):
    total_input_bias = sum(drid.grid.input_bias for drid in column.drids)
    total_output_bias = sum(drid.grid.output_bias for drid in column.drids)
    logging.debug(total_input_bias, total_output_bias)
    total_io_bias = total_input_bias + total_output_bias
    normalization_factor = 1 / total_io_bias

    for drid in column.drids:
        drid.grid.input_bias *= normalization_factor
        drid.grid.output_bias *= normalization_factor


def populate_column(column):
    cell_roles = ['nascent', 'signaller', 'receiver', 'radio']
    cell_codes = [(0, 0), (0, 1), (1, 0), (1, 1)]

    for drid in column.drids:
        # Calculate the number of cells for each role based on input and output biases
        num_cells = drid.grid.array.size
        num_signaller = int(num_cells * drid.grid.input_bias)
        num_receiver = int(num_cells * drid.grid.output_bias)
        num_nascent = num_cells - num_signaller - num_receiver - column.num_radio
        num_radio = column.num_radio

        cell_counts = [num_nascent, num_signaller, num_receiver, num_radio]
        available_roles = [
            role for role, count in zip(cell_roles, cell_counts)
            for _ in range(count)
        ]

        for cell_key, cell_info in drid.cell_dict.items():
            # Assign a random role to the cell and remove it from the available_roles list
            role = random.choice(available_roles)
            available_roles.remove(role)

            # Update the cell's dictionary entry with its role and connection code
            code = cell_codes[cell_roles.index(role)]
            cell_index, local_neighbors = cell_info
            drid.cell_dict[cell_key] = (cell_index, local_neighbors, role, code)


def establish_connections(column):
    # Collect all the cells with their drid index and cell key
    all_cells = [(drid_idx, cell_key, drid.cell_dict[cell_key])
                 for drid_idx, drid in enumerate(column.drids)
                 for cell_key in drid.cell_dict]

    for drid_idx, drid in enumerate(column.drids):
        for cell_key, cell_info in drid.cell_dict.items():
            cell_index, local_neighbors, role, code = cell_info[:4]

            # Find input and output cells
            input_cells = [
                cell for cell in all_cells
                if cell[2][-1] == (0, 1) or cell[2][-1] == (1, 1)
            ]
            output_cells = [
                cell for cell in all_cells
                if cell[2][-1] == (1, 0) or cell[2][-1] == (1, 1)
            ]

            # Connect cells randomly
            input_non_local = random.sample(input_cells, code[0])
            output_non_local = random.sample(output_cells, code[1])

            # Update the cell's dictionary entry with input_non_local and output_non_local lists
            drid.cell_dict[cell_key] = (cell_index, local_neighbors, role, code,
                                        input_non_local, output_non_local)


def create_random_column(io_number, ro_number, number_of_drids, grid_dimension,
                         grid_size):
    # Create an empty Column instance
    column = Column(io_number, ro_number)

    # Loop through the range of number_of_drids
    for _ in range(number_of_drids):
        # Generate random values for grid parameters
        decay_value = random.uniform(0, 0.3)
        lower_tresh = random.uniform(0, 0.35)
        upper_tresh = random.uniform(0.5, 1)
        density = random.uniform(0, 1)
        input_bias = random.uniform(0, 1)
        output_bias = random.uniform(0, 1)
        radio_bias = random.uniform(0, 1)

        # Create a Grid instance
        grid = Grid(grid_dimension, grid_size, decay_value, lower_tresh,
                    upper_tresh, density, input_bias, output_bias, radio_bias)
        drid = Drid(grid)
        # Add the GridWithDict instance to the Column
        column.add_drid(drid)

    # Normalize input and output biases
    normalize_io_biases(column)

    # Populate the Column with cell roles
    populate_column(column)

    # Establish connections between cells
    establish_connections(column)

    return column
