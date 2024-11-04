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
def get_random_edges_with_validation(network_edges):
    while True:
        start_edge, end_edge = random.sample(network_edges, 2)
        route = traci.simulation.findRoute(start_edge, end_edge)
        if len(route.edges) > 0:  # Ensure the route is valid
            return " ".join(route.edges)

# (replace with actual vehicle count data)
vehicle_counts_per_interval = {
    "car": [40, 49, 57, 50, 48, 33, 53, 59, 65, 62, 42, 68, 80, 65, 43, 59, 61, 75, 88, 92, 67, 56, 50, 69],
    "motorcycle": [85, 50, 75, 1, 27, 42, 65, 49, 46, 96, 37, 83, 81, 4, 56, 61, 91, 34, 78, 5, 76, 60, 48, 36],
    "truck": [4, 5, 5, 7, 6, 7, 12, 9, 3, 7, 7, 8, 4, 4, 8, 3, 1, 1, 13, 2, 1, 4, 3, 6],
    "bus": [2, 1, 3, 0, 1, 0, 0, 1, 2, 1, 2, 3, 1, 2, 0, 0, 1, 0, 3, 0, 0, 0, 1, 0],
    "traditional_jeepney": [5, 15, 17, 19, 18, 13, 26, 14, 17, 22, 16, 24, 26, 29, 24, 23, 24, 20, 23, 24, 28, 22, 27, 14],
    "modern_jeepney": [0, 1, 1, 8, 7, 7, 4, 5, 7, 2, 5, 6, 1, 6, 0, 3, 4, 6, 2, 3, 0, 6, 4, 6],
    "bicycle": [4, 33, 10, 12, 10, 0, 13, 21, 12, 12, 5, 8, 11, 45, 9, 5, 19, 17, 5, 14, 2, 23, 16, 11]
}


# Define the time intervals (in seconds) for 15-minute intervals
time_intervals = [(i * 5 * 60, (i + 1) * 5 * 60) for i in range(24)]  

# Define the jeepney routes (r_1 and r_2)
jeepney_routes = {
    "r_1": "-4588647 -917450542 1174874706",
    "r_2": "1112806233 4588647"
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
                        route_edges = get_random_edges_with_validation(network_edges)

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

with open("person_routes/poisson2.rou.xml", "w") as f:
    f.write(formatted_xml)

# Close the SUMO instance
traci.close()

print("Routes file with sorted departures successfully written.")