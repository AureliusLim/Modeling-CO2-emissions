import traci
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import random
import numpy as np

# Connect to SUMO in headless mode
sumoBinary = "sumo"  # This runs SUMO without the GUI
sumoCmd = [sumoBinary, "-n", "intersection.net.xml"]  # Load only the network for validation
traci.start(sumoCmd)

# Random edge generator with route validation
def get_random_edges_with_validation(network_edges):
    while True:
        start_edge, end_edge = random.sample(network_edges, 2)
        route = traci.simulation.findRoute(start_edge, end_edge)
        if len(route.edges) > 0:  # Ensure the route is valid
            return " ".join(route.edges)

# Sample vehicle counts (replace with actual vehicle count data)
vehicle_counts_per_interval = [200, 105, 250, 300, 180]

# Define the time intervals (in seconds) for 15-minute intervals
time_intervals = [(i * 15 * 60, (i + 1) * 15 * 60) for i in range(len(vehicle_counts_per_interval))]

# Define available edges in the network (replace with actual edges from your network)
network_edges = ["1174874706", "-917450542", "-4588647", "1112806233", "775437708", "4588647"]

# Create the root element <routes>
root = ET.Element("routes", {
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xsi:noNamespaceSchemaLocation": "http://sumo.dlr.de/xsd/routes_file.xsd"
})

# Define vehicle type
vType = ET.SubElement(root, "vType", {
    "id": "car",
    "length": "5.00",
    "minGap": "2.50",
    "maxSpeed": "33.33",
    "guiShape": "passenger",
    "color": "red",
    "accel": "1.0",
    "decel": "4.5",
    "sigma": "0.5"
})

# Generate vehicles and routes for each time interval based on Poisson distribution
vehicle_id = 0
for interval_index, (start_time, end_time) in enumerate(time_intervals):
    vehicle_count = vehicle_counts_per_interval[interval_index]
    poisson_times = np.cumsum(np.random.poisson(lam=(end_time - start_time) / vehicle_count, size=vehicle_count))

    for t in poisson_times:
        if t + start_time < end_time:  # Only add vehicles within the time interval
            vehicle = ET.SubElement(root, "vehicle", {
                "id": f"veh_{vehicle_id}",
                "type": "car",
                "depart": str(t + start_time)
            })
            # Validate the route before adding it
            route_edges = get_random_edges_with_validation(network_edges)
            route = ET.SubElement(vehicle, "route", {
                "edges": route_edges
            })
            vehicle_id += 1

# Write the XML file with proper formatting
xml_str = ET.tostring(root, encoding='utf-8').decode()
formatted_xml = minidom.parseString(xml_str).toprettyxml(indent="    ")

with open("output.rou.xml", "w") as f:
    f.write(formatted_xml)

# Close the SUMO instance
traci.close()

print("Routes file successfully written.")
