# NDCA
### Short for "N Dimensional Cellular Automata". 

NDCA is a handy tool for creating grids of arbitrary dimensions, and running a cellular automata in these grids.

You can create individual grids and run cellular automata based only on local rules for that n dimensional space,
or you can create non local neighbourhoods between n dimensional grids that you have created, and pack them as a
"column". 

This tool was created to simulate cortical colon dynamics in the brain, a cortical mini-colon is the "elementary
processing unit" of cortex, consisting of rougly 110 neurons. 


I aim to build a simulation environment, where it will be possible to simulate a giant ensemble of these "colons"
and see how they interact with each other; in the hopes of understanding the chaotic behaviour of neuronal dynamics
better.

Please e mail me at: siyarbahadir@gmail.com, if you have any questions regarding the tool and bug fixes.
### What is a cortical column?
![Cortical_Columns](https://user-images.githubusercontent.com/16266287/232743317-91e6c51e-089e-452a-9394-433b38fa5949.jpg)
![RUH_PMH](https://user-images.githubusercontent.com/16266287/232743356-b550cf02-42de-43b3-82a5-604f897e1aa3.jpg)

A cortical column is a proposed as "most basic unit of computation" in human brain, with this project, I aim to model a cortical column as a representative volume element, and then simulating 150.000 of them together connected together with a human connectivity graph, and get a "surface" and "depth" recordings of the "simulated cortex".

### How can NDCA be useful in understanding cortical information processing?

Below you will find an example 3D grid automata created with NDCA. Notice how the patterns on the surface and in the depths of the column is not the same. 
With NDCA, it is possible to observe/simulate these kind of phenomena, which might help with decoding the surface electrode recordings.

This kind of data can be used for generating fake data for surface electrode signal analysis researchers, and try generating algorithms to interpolate what is going on in the depths of the piece of cortex that we listen to.

![cortical_colum_modified](https://user-images.githubusercontent.com/16266287/232747029-a1363f37-04b9-4790-809c-9cbe1f3252be.png)

![Slayt1](https://user-images.githubusercontent.com/16266287/232742394-78934107-c92e-4e7d-a3fc-a88446f6a2a7.PNG)
![Slayt2](https://user-images.githubusercontent.com/16266287/232742418-11114eca-355c-4ca0-bc9f-bfc0779b2522.PNG)
![Slayt3](https://user-images.githubusercontent.com/16266287/232742437-22a71054-a84d-4b7d-85c5-150abf673b50.PNG)


### Documentation:

This codebase revolves around simulating a cellular automata model using a grid system. The main components of the codebase are classes, functions, and modules for creating, populating, and processing grids of cells with various properties.

The main classes and their hierarchy are as follows:

- Grid
  - Drid
    - Column
      - Worker
        - classical_CA_worker
      - ResultColumn

The main functions and their hierarchy are as follows:

- create_cell_dict
  - get_local_neighbors
- add_local_neighbors
- normalize_io_biases
- populate_column
- establish_connections
- create_random_column
  - run_simulation
    - calculate_neighborhood_activation_score
    - count_active_inactive_neighbors
  - save_combined_vti_files
  - display_volumetric_rendering
  - random_cell_generator
  - initialize_cells

Here is a brief description of the main classes and functions:

- Grid: Represents a grid of cells with various properties such as the decay value, input/output biases, and thresholds.
- Drid: A wrapper around a Grid object and its corresponding cell dictionary.
- Column: Represents a collection of Drids along with the number of input/output and radio cells.
- Worker: A class responsible for processing the columns in the simulation.
- classical_CA_worker: A subclass of Worker tailored for classical cellular automata.
- ResultColumn: A class responsible for storing the simulation results.

- create_cell_dict: Creates a cell dictionary for a given grid.
- get_local_neighbors: Returns the local neighbors of a given cell in the grid.
- add_local_neighbors: Adds the local neighbors to the cell dictionary of a given grid.
- normalize_io_biases: Normalizes the input and output biases in a column.
- populate_column: Assigns roles and connection codes to the cells in a column.
- establish_connections: Establishes connections between cells in a column.
- create_random_column: Creates a random column with specified parameters.
- run_simulation: Runs the simulation for a specified number of frames and returns the result.
- save_combined_vti_files: Saves the combined activation grids as VTI files.
- display_volumetric_rendering: Displays a 3D volumetric rendering of the vtkImageData.
- random_cell_generator: Generates random values for cell properties.
- initialize_cells: Initializes cell instances in a column with random properties.


