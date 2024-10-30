import re
from collections import defaultdict

# Function to read and parse emissions data from a text file
def read_emissions_file(filename):
    emissions_data = defaultdict(float)  # Store total CO2 per step
    with open(filename, 'r') as file:
        current_step = None
        for line in file:
            # Match "Step" line to get the simulation step
            step_match = re.match(r"Step\s+([0-9\.]+):", line)
            if step_match:
                current_step = int(step_match.group(1))  # Ensure it's an integer
            
            # Match "Vehicle" line to get the vehicle id and CO2 emissions
            vehicle_match = re.match(r"\s*Vehicle\s+(\S+):\s+CO2 emissions\s+=\s+([0-9\.]+)\s+g", line)
            if vehicle_match and current_step is not None:
                co2_emission = float(vehicle_match.group(2))
                emissions_data[current_step] += co2_emission

    return emissions_data

# Function to calculate average CO2 emissions per 5-minute interval (300 steps)
def calculate_avg_co2_emissions(emissions_data, step_interval=300):
    co2_per_interval = []
    total_co2 = 0
    step_count = 0
    interval_number = 1  # Start interval numbering from 1

    # Process each step in order
    for step in sorted(emissions_data.keys()):
        total_co2 += emissions_data[step]
        step_count += 1

        # If the interval is complete, calculate the average
        if step_count == step_interval:
            avg_co2 = total_co2 / step_interval
            co2_per_interval.append({'Interval': interval_number, 'Average_CO2': avg_co2})
            
            # Reset for the next interval
            total_co2 = 0
            step_count = 0
            interval_number += 1  # Increment the interval number

    # Handle any remaining steps that didn't fit into a full interval
    if step_count > 0:
        avg_co2 = total_co2 / step_count
        co2_per_interval.append({'Interval': interval_number, 'Average_CO2': avg_co2})

    return co2_per_interval

# Example usage:
filename = "Emission Output/emissions.txt"  # The file where your emissions data is stored
emissions_data = read_emissions_file(filename)
co2_by_minute = calculate_avg_co2_emissions(emissions_data)

# Output the results
for minute_data in co2_by_minute:
    print(f"Interval {minute_data['Interval']}: Average CO2 = {minute_data['Average_CO2']} mg")
