import re

# Function to read and parse emissions data from a text file
def read_emissions_file(filename):
    emissions_data = []
    with open(filename, 'r') as file:
        current_step = None
        for line in file:
            # Match "Step" line to get the simulation step
            step_match = re.match(r"Step\s+([0-9\.]+):", line)
            if step_match:
                current_step = int(step_match.group(1))  # Ensure it's an integer
            
            # Match "Vehicle" line to get the vehicle id and CO2 emissions
            vehicle_match = re.match(r"\s*Vehicle\s+(\S+):\s+CO2 emissions\s+=\s+([0-9\.]+)\s+g", line)
            if vehicle_match:
                vehicle_id = vehicle_match.group(1)
                co2_emission = float(vehicle_match.group(2))
                emissions_data.append({
                    'step': current_step,
                    'vehicle_id': vehicle_id,
                    'CO2': co2_emission
                })
    return emissions_data

# Function to calculate average CO2 emissions per 5-minute interval (300 steps)
def calculate_avg_co2_emissions(emissions_data, step_interval=300):
    co2_per_interval = []
    current_time = 0
    total_co2 = 0
    step_count = 0

    for entry in emissions_data:
        step_time = entry['step']
        co2 = entry['CO2']

        # Check if we're still within the current interval
        if step_time < current_time + step_interval:
            total_co2 += co2
            step_count += 1  # Increment the step count
        else:
            # Calculate the average CO2 for the previous interval
            avg_co2 = total_co2 / step_count if step_count > 0 else 0
            co2_per_interval.append({'Interval': current_time // step_interval, 'Average_CO2': avg_co2})
            
            # Move to the next interval
            current_time += step_interval
            total_co2 = co2  # Start new interval with the current CO2
            step_count = 1  # Reset step count

    # Add the last interval if there's remaining data
    if step_count > 0:
        avg_co2 = total_co2 / step_count
        co2_per_interval.append({'Interval': current_time // step_interval, 'Average_CO2': avg_co2})

    return co2_per_interval

# Example usage:
filename = "Emission Output/emissions.txt"  # The file where your emissions data is stored
emissions_data = read_emissions_file(filename)
co2_by_minute = calculate_avg_co2_emissions(emissions_data)

# Output the results
for minute_data in co2_by_minute:
    print(f"Interval {minute_data['Interval']}: Average CO2 = {minute_data['Average_CO2']} mg")
