import re


log_file_path = 'Emission Output/emissions.txt'

def extract_emissions(log_file_path, vehicle_ids):
    total_emissions = {vehicle_id: 0 for vehicle_id in vehicle_ids}
    
    with open(log_file_path, 'r') as file:
        for line in file:

            match = re.search(r'Vehicle (jeepney_1|modernjeepney_1): CO2 emissions = ([\d\.]+) g', line)
            if match:
                vehicle_id, emission_str = match.groups()
                print("match")
                emission = float(emission_str)
                
                if vehicle_id in total_emissions:
                    total_emissions[vehicle_id] += emission
    
    return total_emissions


vehicle_ids = ["jeepney_1", "modernjeepney_1"]


total_emissions = extract_emissions(log_file_path, vehicle_ids)
for vehicle_id, total in total_emissions.items():
    print(f"Total CO2 emissions for {vehicle_id}: {total:.2f} g")

