import traci
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import random
import numpy as np

# Connect to SUMO in headless mode
sumoBinary = "sumo"  # This runs SUMO without the GUI
sumoCmd = [sumoBinary, "-n", "intersection.net.xml"]  # Load only the network for validation
traci.start(sumoCmd)
network_edges = ["1174874706", "-917450542", "-4588647", "1112806233", "775437708", "4588647", "917450543", "160192389", "136822578", "1174874706"]
# Random edge generator with route validation
def get_random_route_jeep(route_1, route_2):
    """Assign route_1 or route_2 randomly to jeepneys"""
    return random.choice([route_1, route_2])
def get_random_route_other(other_routes):
    """Randomly choose a route from other_routes dictionary with lower probability for r_1 and r_2."""
    # Define weights for each route, lower weight for r_1 and r_2
    route_weights = {
        "r_1": 0.01, 
        "r_2": 0.01,  
        "r_3": 0.05,  
        "r_4": 0.05,  
        "r_5": 0.44, 
        "r_6": 0.44   
    }
    
    # Normalize weights and select a route based on probability
    routes = list(other_routes.values())
    keys = list(other_routes.keys())
    probabilities = [route_weights[key] for key in keys]
    probabilities = [p / sum(probabilities) for p in probabilities]  # Ensure probabilities sum to 1

    # Randomly choose a route based on weights
    selected_route = random.choices(routes, probabilities)[0]
    return selected_route

# (replace with actual vehicle count data)
vehicle_counts_per_interval = {
    "car": [32, 57, 50, 45, 48, 31, 36, 33, 31, 39, 36, 34, 45, 36, 33, 49, 51, 56, 49, 46, 60, 51, 57, 54],
    "motorcycle": [96, 80, 78, 82, 89, 95, 101, 99, 105, 78, 85, 60, 71, 73, 67, 68, 76, 77, 80, 87, 85, 88, 95, 99],
    "truck": [4, 2, 5, 4, 3, 5, 2, 5, 4, 3, 3, 3, 3, 3, 2, 3, 3, 4, 5, 3, 5, 3, 4, 4],
    "bus": [0, 1, 0, 0, 1, 0, 1, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
    "traditional_jeepney": [23, 18, 21, 21, 22, 26, 28, 24, 19, 22, 25, 20, 28, 29, 21, 26, 25, 26, 24, 29, 27, 24, 22, 23],
    "modern_jeepney": [4, 5, 2, 1, 4, 5, 5, 6, 4, 4, 5, 3, 5, 6, 5, 5, 4, 5, 5, 4, 5, 3, 5, 5],
    "bicycle": [16, 8, 11, 12, 15, 17, 18, 24, 16, 17, 14, 22, 29, 23, 24, 27, 24, 16, 14, 15, 11, 9, 8, 9]
}


# Define the time intervals (in seconds) for 15-minute intervals
time_intervals = [(i * 5 * 60, (i + 1) * 5 * 60) for i in range(24)]  

# Define the jeepney routes (r_1 and r_2)
jeepney_routes = {
    "r_1": "-4588647 -917450542 1174874706",
    "r_2": "1112806233 4588647"
}

other_routes = {
    "r_1": "-4588647 -917450542 1174874706",
    "r_2": "-4588647 160192389",
    "r_3": "1112806233 160192389",
    "r_4": "1112806233 4588647",
    "r_5": "775437708 917450543",
    "r_6": "136822578 1174874706"

}

# Create the root element <routes>
root = ET.Element("routes", {
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsi:noNamespaceSchemaLocation": "http://sumo.dlr.de/xsd/routes_file.xsd"
})

# List to hold vehicles and departure times
vehicles_list = []

# Generate vehicles and routes for each time interval based on Poisson distribution
vehicle_id = 0
trad_id = 0
modern_id = 0
for interval_index, (start_time, end_time) in enumerate(time_intervals):
    for vtype, counts in vehicle_counts_per_interval.items():
        vehicle_count = counts[interval_index]
        
        if vehicle_count > 0:  # Check to ensure vehicle_count is greater than zero
            poisson_times = np.cumsum(np.random.poisson(lam=(end_time - start_time) / vehicle_count, size=vehicle_count))

            for t in poisson_times:
                if t + start_time < end_time:  # Only add vehicles within the time interval
                    depart_time = t + start_time
                    if vtype == "traditional_jeepney":
                        vehicle_data = {
                            "id": f"jeepney_{trad_id}",
                            "type": vtype,
                            "depart": str(depart_time)
                        }
                        trad_id += 1
                    elif vtype == "modern_jeepney":
                        vehicle_data = {
                            "id": f"modernjeepney_{modern_id}",
                            "type": vtype,
                            "depart": str(depart_time)
                        }
                        modern_id += 1
                    else:
                        vehicle_data = {
                            "id": f"veh_{vehicle_id}",
                            "type": vtype,
                            "depart": str(depart_time)
                        }
                    
                    # Assign a route
                    if vtype in ["traditional_jeepney", "modern_jeepney"]:
                        # Randomly assign route_1 or route_2 for jeepneys
                        route_edges = get_random_route_jeep(jeepney_routes["r_1"], jeepney_routes["r_2"])
                    else:
                        # For other vehicle types, assign random valid edges from the network
                        route_edges = get_random_route_other(other_routes)

                    vehicle_data["route"] = route_edges
                    vehicles_list.append(vehicle_data)
                    vehicle_id += 1
# Sort the vehicle list by departure time
vehicles_list.sort(key=lambda x: float(x["depart"]))

# Add sorted vehicles to the XML
for vehicle_data in vehicles_list:
    vehicle = ET.SubElement(root, "vehicle", {
        "id": vehicle_data["id"],
        "type": vehicle_data["type"],
        "depart": vehicle_data["depart"]
    })
    ET.SubElement(vehicle, "route", {"edges": vehicle_data["route"]})

# Write the XML file with proper formatting
xml_str = ET.tostring(root, encoding='utf-8').decode()
formatted_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")

with open("vehicle_routes/poisson1.rou.xml", "w") as f:
    f.write(formatted_xml)

# Close the SUMO instance
traci.close()
print(list(other_routes.values()))
print("Routes file with sorted departures successfully written.")