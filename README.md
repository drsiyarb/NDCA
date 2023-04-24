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

A cortical column is a proposed as "most basic unit of computation" in human brain, with this program, I aim to model a cortical column as a representative volume element, and then simulate 150.000 of them together connected together with a human connectivity graph, and get a "surface" and "depth" recordings of the "simulated cortex".

### How can NDCA be useful in understanding cortical information processing?

Below you will find an example 3D grid automata created with NDCA. Notice how the patterns on the surface and in the depths of the column is not the same. 
With NDCA, it is possible to observe/simulate these kind of phenomena, which might help with decoding the surface electrode recordings.

This kind of data can be used for generating fake data for surface electrode signal analysis researchers, and try generating algorithms to interpolate what is going on in the depths of the piece of cortex that we listen to.

![cortical_colum_modified](https://user-images.githubusercontent.com/16266287/232747029-a1363f37-04b9-4790-809c-9cbe1f3252be.png)

![Slayt1](https://user-images.githubusercontent.com/16266287/232742394-78934107-c92e-4e7d-a3fc-a88446f6a2a7.PNG)
![Slayt2](https://user-images.githubusercontent.com/16266287/232742418-11114eca-355c-4ca0-bc9f-bfc0779b2522.PNG)
![Slayt3](https://user-images.githubusercontent.com/16266287/232742437-22a71054-a84d-4b7d-85c5-150abf673b50.PNG)


# Cortical Column Simulation

This project aims to simulate the behavior of a cortical column in the human cortex, which can be used as a representative volume element for constructing a whole-brain simulation. By connecting 150,000 of these columns based on the human connectome data, we can study the emergent properties and potential applications of realistic large-scale brain networks.

## Overview

A cortical column is an intricate structure made up of interconnected cells that work together to process information within the brain. In this project, we represent cortical columns as stacks of multi-dimensional grid structures called Drids. Each Drid serves as a layer within the column, containing cells with various roles, connections to local and non-local neighbors, and dynamic properties like activation state and excitability.

The core functionality of the code includes:

1. Defining Grid and Drid classes to create multi-dimensional grid structures.
2. Generating cells with random initial states and assigning them to Drids.
3. Populating a Column object by stacking Drids as layers.
4. Establishing connections between cells within the same Drid or across different Drids in a Column.
5. Running cellular automata simulations using different worker classes (Worker and classical_CA_worker), which update cell states based on their own criteria.


## Grid Class

The Grid class represents a multi-dimensional grid on which cellular automata can be run. It has several properties:

- decay_value: The rate at which cell voltage decreases after sending an impulse.
- lower_tresh: The lower threshold for a cell's voltage needed for it to become excitable again after activation.
- upper_tresh: The upper threshold for a cell's voltage needed for it to activate (akin to neuron firing).
- density: A property related to how crowded the grid is with connections.
- input_bias: A factor for determining the number of input connections a Drid will have when packed into a Column.
- output_bias: A factor for determining the number of output connections a Drid will have when packed into a Column.
- radio_bias: A factor for determining the number of radio connections (both input and output) a Drid will have when packed into a Column.

These properties play crucial roles in calculating cell activation, similar to how neurons fire in the brain.

## Drid Class

The Drid class acts as a container for a Grid object and its associated cell dictionary. It simplifies handling the grid and its cells during simulations.

## Cell Dictionary and Drid Setup

Creating a cell dictionary is an essential step in setting up the simulation. The cell dictionary holds information about each cell within a Drid, which will be used during calculations, connections establishment, and updating states. By associating cells with keys (e.g., 'cell1', 'cell2', etc.), we can quickly access specific cells when needed.

The `create_cell_dict` function generates a cell dictionary for a given Grid object. It iterates through all indices in the Grid and assigns unique keys to each corresponding cell index. This initial setup only includes the cell's location, but we'll soon expand it with additional properties such as local neighbors and connection information.

Once we have created the cell dictionary, we pass it to the Drid class constructor along with its associated Grid object. This way, every Drid contains both the grid structure and the data necessary to connect cells and run simulations on them.

In order for the cells to interact with their surroundings, we need to identify their local neighbors. Using the `get_local_neighbors` function, we find adjacent cell indices for any given cell within a Drid's array. However, simply having a list of neighbor indices isn't enough – we also need to link this information back into our cell dictionary.

That's where `add_local_neighbors` comes into play. This function takes a Drid object containing a grid array and the accompanying cell dictionary (created earlier) and updates every entry in that dictionary by appending local neighbors' indices. With this updated representation of cells in our Drids, we now have complete knowledge of each cell's immediate environment.

Think of these additions like giving your Lego occupants little contact books filled with phone numbers of their neighboring friends. Now they're ready to talk to each other!

By systematically creating multi-dimensional grids (Grid objects), generating dictionaries containing cellular properties (using create_cell_dict), finding local neighbors (get_local_neighbors), and updating the cell dictionaries (add_local_neighbors), we establish a solid foundation for simulating complex interactions within and between Drids that form our cortical columns.

The cell dictionary of a Drid contains the following information for each cell:

1. **cell**: An instance of the Cell class, holding properties like voltage, activation_state, and excitability.
2. **cell_index**: The index (position) of the cell within the Drid's multi-dimensional grid array.
3. **local_neighbors**: A list of adjacent cell indices that are considered local neighbors to the current cell in the same Drid.
4. **role**: A string representing the role of the cell (e.g., 'nascent', 'signaller', 'receiver', or 'radio').
5. **code**: A tuple representing the input/output connection code for that specific role (e.g., (0, 0), (0, 1), (1, 0), or (1, 1)).
6. **input_non_local**: A list of non-local input connections to other cells in different Drids within the same Column.
7. **output_non_local**: A list of non-local output connections from this cell to other cells in different Drids within the same Column.

Each entry in the cell dictionary is associated with a unique key such as 'cell1', 'cell2', etc., making it easy to access and update specific cells as needed during simulations.
## Cell Generation and Initialization

Each cell within a Drid is represented by an instance of the Cell class, which has three main properties:

- voltage: The cell's current voltage level.
- activation_state: The activation state of the cell (0 - inactive or 1 - active).
- excitability: Indicates whether the cell can receive impulses or not (0 - unexcitable or 1 - excitable).

We randomly generate initial values for these properties using `random_cell_generator`. We then use `initialize_cells` to create instances of Cell objects and assign them to each cell location in every Drid in a Column.

## Establishing Connections

While stacking up Drids to form columns, we need to establish their relationships based on input/output biases. Connections between cells play a crucial role in propagating the signals within and across Drids. The `populate_column` function assigns random roles to each cell in the Drids, which include:

- Nascent: A cell that only considers local neighbors during calculations.
- Signaller: A cell that can send signals to non-local neighbors.
- Receiver: A cell that can receive signals from non-local neighbors.
- Radio: A cell that can both send and receive signals to/from non-local neighbors.

These roles determine how a cell behaves within its Drid, as well as its interactions with other cells in different Drids packed into the same Column. Each role is associated with a connection code (input/output) for easy identification of input and output connections.

The `establish_connections` function creates random connections between cells based on their respective input/output codes. When making calculations for cellular automata, these connected cells act as if they're local neighbors even if they are in different Drids within the same Column.

## Running Simulations using Worker Classes

We have defined two types of worker classes to run simulations on columns:

1. **Worker**: This class processes the column by updating cell activation states and excitability based on their voltage, activation state, and other properties.

2. **classical_CA_worker**: This class processes the column like a classical cellular automaton, updating cell states solely based on the number of active (alive) neighbors surrounding each cell.

Both worker classes follow different rules to update the state of the cells within the column during simulation runs.

## Simulation Execution

The `run_simulation` function executes the cellular automata simulation for a specified number of frames using classical_CA_worker. It takes three parameters:

- column: The Column object containing stacked Drids.
- num_frames: Total number of frames (iterations) for which the simulation will run.
- max/min: Minimum and maximum limits for the number of active neighbors to determine cell activation state.

During the simulation, a cell survives if its number of active neighbors falls within the min-max range. Otherwise, it dies due to overpopulation or underpopulation.

The function updates the cell states for each frame and stores the voltage and activation grids in a ResultColumn object, which can later be used for analysis or visualization purposes.

## Wrapping Up

Imagine our cortical columns as skyscrapers built with Lego blocks (Drids) stacked on top of one another. Each block has its own set of tiny occupants (cells) with unique jobs, connections to other occupants in different blocks, and even their own power supply (voltage). By simulating how these occupants work together across multiple skyscrapers, we can better understand how our brains process information at a larger scale.

You now have a grasp on how to simulate cortical columns using cellular automata algorithms. Enjoy exploring brain dynamics and remember: keep calm and cortex on!
