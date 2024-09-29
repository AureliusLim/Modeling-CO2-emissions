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

# Sample vehicle counts (replace with actual vehicle count data)
vehicle_counts_per_interval = {
    "car": [100, 80, 120, 150, 100],
    "bicycle": [10, 8, 12, 10, 7],
    "motorcycle": [50, 40, 60, 70, 45],
    "truck": [20, 15, 25, 30, 18],
    "bus": [5, 5, 8, 6, 4],
    "traditional_jeepney": [15, 12, 18, 20, 14],
    "modern_jeepney": [10, 9, 14, 15, 12],
}

# Define the time intervals (in seconds) for 15-minute intervals
time_intervals = [(i * 15 * 60, (i + 1) * 15 * 60) for i in range(5)]

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
trad_id= 0
modern_id = 0
for interval_index, (start_time, end_time) in enumerate(time_intervals):
    for vtype, counts in vehicle_counts_per_interval.items():
        vehicle_count = counts[interval_index]
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

with open("poisson3.rou.xml", "w") as f:
    f.write(formatted_xml)

# Close the SUMO instance
traci.close()

print("Routes file with sorted departures successfully written.")
