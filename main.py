import click
from click_loglevel import LogLevel
import datetime
import logging

from cell import initialize_cells
from column_packer import (
    create_random_column,
    establish_connections,
    normalize_io_biases,
    populate_column
)
from data_structures import Column, Grid
from simulation_voltage import (
    are_grids_different,
    run_simulation,
    save_combined_vti_files
)


@click.command()
@click.option(
    "--io-number",
    "-i",
    default=10,
    show_default=True,
    help="number of unidirectional (input|output) connections to establish",
)
@click.option(
    "--ro-number",
    "-r",
    default=5,
    show_default=True,
    help="number of bidirectional connections to establish",
)
@click.option(
    "--drid-number",
    "-d",
    default=10,
    show_default=True,
    help="number of drids per column",
)
@click.option(
    "--grid-dimension",
    "-g",
    default=10,
    show_default=True,
    help="dimensionality of each grid",
)
@click.option(
    "--grid-size",
    "-s",
    default=10,
    show_default=True,
    help="range of each dimension within a grid",
)
@click.option(
    "--frame-number",
    "-f",
    default=100,
    show_default=True,
    help="number of frames to run the simulation",
)
@click.option(
    "--rendering-offset",
    "-o",
    default=10,
    show_default=True,
    help="size offset to use for rendering results to vti files",
)
@click.option(
    "--log-level",
    "-l",
    type=LogLevel(),
    default=logging.INFO
)
def main(io_number, ro_number, drid_number, grid_dimension, grid_size, frame_number, rendering_offset, log_level):
    logging.basicConfig(
        format="[%(levelname)-8s] %(message)s",
        level=log_level,
    )
    logging.info("Run at: %s", datetime.datetime.now())
    logging.info("Log level set to %r", log_level)

    random_column = create_random_column(
        io_number, ro_number, drid_number, grid_dimension, grid_size
    )

    initialize_cells(random_column)

    result_column = run_simulation(random_column, num_frames)

    save_combined_vti_files(
        result_column,
        frame_number,
        "output",
        rendering_offset
    )

if __name__ == "__main__":
    main()
