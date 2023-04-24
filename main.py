import logging

from cell import initialize_cells
from column_packer import (create_random_column, establish_connections,
                           normalize_io_biases, populate_column)
from data_structures import Column, Grid, add_local_neighbors, create_cell_dict
from simulation_voltage import (are_grids_different, run_simulation,
                                save_combined_vti_files)


LOG_FILE_STR = 'ndca.log.txt'

logging.basicConfig(filename=LOG_FILE_STR, level=logging.DEBUG, format='%(message)s')
logging.info("\n----------------\n" + "filename: " + FILENAME_STR)
logging.info("Run at: %s", datetime.datetime.now())


def Main():
    io_number = 1200
    ro_number = 600
    number_of_drids = 6
    grid_dimension = 3
    grid_size = 10

    random_column = create_random_column(io_number, ro_number, number_of_drids, grid_dimension, grid_size)

    initialize_cells(random_column)

    ########################################

    num_frames = 100
    result_column = run_simulation(random_column, num_frames)

    # Example usage:
    frame1 = result_column.voltage_grids[0][24]
    frame2 = result_column.voltage_grids[0][26]
    threshold = 0.001

    if are_grids_different(frame1, frame2, threshold):
        print("The arrays are significantly different.")
    else:
        print("The arrays are equal, there is a problem with simulation.")

    # print(frame2)

    ########################################

    save_combined_vti_files(
        result_column,
        num_frames=100,
        output_folder="output",
        offset=10,
    )

    ########################################

    # drid1_features = [3, 4, 0.3, 0.1, 0.6, 0.5, 0.3, 0.6, 0.2]
    # drid2_features = [3, 4, 0.2, 0.12, 0.7, 0.6, 0.2, 0.8, 0.1]
    # drid3_features = [3, 4, 0.2, 0.16, 0.3, 0.4, 0.5, 0.5, 0.2]
    # drid4_features = [3, 4, 0.4, 0.05, 0.7, 0.5, 0.6, 0.4, 0.3]
    # drid5_features = [3, 4, 0.2, 0.2, 0.7, 0.5, 0.2, 0.8, 0.1]
    # drid6_features = [3, 4, 0.3, 0.2, 0.6, 0.5, 0.4, 0.6, 0.2]

    # feature_list = [
    #     drid1_features,
    #     drid2_features,
    #     drid3_features,
    #     drid4_features,
    #     drid5_features,
    #     drid6_features,
    # ]

    # manual_column = Column(50000, 25000)

    # for feature in feature_list:
    #     grid = Grid(
    #         n=feature[0],
    #         x=feature[1],
    #         decay_value=feature[2],
    #         lower_tresh=feature[3],
    #         upper_tresh=feature[4],
    #         density=feature[5],
    #         input_bias=feature[6],
    #         output_bias=feature[7],
    #         radio_bias=feature[8],
    #     )

    #     grid_with_dict = create_cell_dict(grid)
    #     add_local_neighbors(grid_with_dict)
    #     manual_column.add_drid(grid_with_dict)

    # normalize_io_biases(manual_column)

    # # Populate the Column with cell roles
    # populate_column(manual_column)

    # # Establish connections between cells
    # establish_connections(manual_column)

    # initialize_cells(manual_column)

    # # for drid_idx, drid in enumerate(random_column.drids):
    # #     print(f"Drid {drid_idx + 1}:")
    # #     for cell_key, cell_info in drid.cell_dict.items():
    # #         (
    # #             cell,
    # #             cell_index,
    # #             local_neighbors,
    # #             role,
    # #             code,
    # #             input_non_local,
    # #             output_non_local,
    # #         ) = cell_info
    # #         print(f"{cell_key}: {cell}")
    # #     print()



if __name__ == '__main__':
    Main()
