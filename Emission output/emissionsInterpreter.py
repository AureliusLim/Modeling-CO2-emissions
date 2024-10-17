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
                current_step = float(step_match.group(1))
            
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

# Function to calculate total CO2 emissions every minute (60 steps)
def calculate_co2_emissions(emissions_data, step_interval=300):
    co2_per_interval = []
    current_time = 0
    co2_total = 0
    current_interval_emissions = {}

    for entry in emissions_data:
        step_time = entry['step']
        vehicle_id = entry['vehicle_id']
        co2 = entry['CO2']
        
        # If we are still within the current minute, sum the CO2 emissions
        if step_time < current_time + step_interval:
            if vehicle_id not in current_interval_emissions:
                current_interval_emissions[vehicle_id] = co2
            else:
                current_interval_emissions[vehicle_id] = max(current_interval_emissions[vehicle_id], co2)
        else:
            # Calculate the total CO2 for the current interval
            co2_total = sum(current_interval_emissions.values())
            co2_per_interval.append({'Interval': current_time // step_interval, 'CO2_total': co2_total})

        
            current_time += step_interval
            current_interval_emissions = {vehicle_id: co2}

    # Add the last interval if there is remaining data
    if current_interval_emissions:
        co2_total = sum(current_interval_emissions.values())
        co2_per_interval.append({'Interval': current_time // step_interval, 'CO2_total': co2_total})

    return co2_per_interval

# Example usage:
filename = "Emission Output/emissions.txt"  # The file where your emissions data is stored
emissions_data = read_emissions_file(filename)
co2_by_minute = calculate_co2_emissions(emissions_data)

# Output the results
for minute_data in co2_by_minute:
    print(f"Interval {minute_data['Interval']}: Total CO2 = {minute_data['CO2_total']} g")
