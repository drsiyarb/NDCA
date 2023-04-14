import random
class Cell:
    def __init__(self, voltage, activation_state, excitability):
        self.voltage = min(voltage, 1)  # Ensure voltage is never over 1
        self.activation_state = activation_state
        self.excitability = excitability

    def __str__(self):
        return f"Voltage: {self.voltage}, Activation State: {self.activation_state}, Excitability: {self.excitability}"

def random_cell_generator():
    voltage = random.uniform(0.5, 1)  # Random voltage between 0 and 1
    activation_state = random.choice([0, 1])  # Random activation state (0 or 1)
    if activation_state==1:
        excitability = 0
    else:
        excitability = 1

    return voltage, activation_state, excitability

def initialize_cells(column):
    for drid in column.drids:
        for cell_key, cell_info in drid.cell_dict.items():
            cell_index, local_neighbors, role, code, input_non_local, output_non_local = cell_info[:6]

            # Initialize cell properties
            voltage, activation_state, excitability = random_cell_generator()

            # Create a Cell instance and update the cell's dictionary entry
            cell = Cell(voltage, activation_state, excitability)
            drid.cell_dict[cell_key] = (cell, cell_index, local_neighbors, role, code, input_non_local, output_non_local)
