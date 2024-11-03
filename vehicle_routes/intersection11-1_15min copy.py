import random
import sumolib
from lxml import etree
import traci

# Initialize SUMO network
net = sumolib.net.readNet('edited.net.xml')

# Start edges for each intersection
intersection1_startedges = ['368461882#0', '176633481', '-923261416', '-29257171#0']
intersection2_startedges = ['1112806233-AddedOnRampEdge', '-4588647#0', '775437708', '136822578']
intersection3_startedges = ['704746731#0', '-5019469#5', '119883577#7']

# Vehicle counts by type at each intersection
vehicle_counts = {
    'intersection1': {'bicycle': 28, 'bus': 0, 'car': 254, 'motorcycle': 705, 'truck': 44},
    'intersection2': {'bicycle': 16, 'bus': 0, 'car': 505, 'motorcycle': 723, 'truck': 77},
    'intersection3': {'bicycle': 34, 'bus': 0, 'car': 150, 'motorcycle': 334, 'truck': 32},
}

# Define mappings of intersection start edges
intersection_edges = {
    'intersection1': intersection1_startedges,
    'intersection2': intersection2_startedges,
    'intersection3': intersection3_startedges
}

# Function to choose a valid distant edge using route validation
def get_random_edges_with_validation(start_edge, network_edges):
    while True:
        end_edge = random.choice(network_edges)
        if end_edge != start_edge:  # Ensure end edge is not the same
            route = traci.simulation.findRoute(start_edge, end_edge)
            if len(route.edges) > 2:  # Ensure the route is valid and has more than two edges
                return " ".join(route.edges)

# Start the TraCI server (necessary for traci functions)
sumo_binary = "sumo"  # or "sumo-gui" for visual debugging
traci.start([sumo_binary, "-n", "edited.net.xml"])

# Prepare to collect vehicles with their routes and departure times
vehicle_routes = []
network_edges = [edge.getID() for edge in net.getEdges()]

# Create routes for each intersection
for intersection, counts in vehicle_counts.items():
    edges = intersection_edges[intersection]

    for vehicle_type, count in counts.items():
        for i in range(count):
            # Select start edge and get a valid distant route
            start_edge = random.choice(edges)
            route_edges = get_random_edges_with_validation(start_edge, network_edges)
            depart_time = random.randint(0, 850)

            # Append vehicle details to the list for sorting
            vehicle_routes.append({
                'id': f"{vehicle_type}_{intersection}_{i}",
                'type': vehicle_type,
                'depart': depart_time,
                'route': route_edges
            })

# Sort vehicles by departure time
vehicle_routes.sort(key=lambda v: v['depart'])

# Generate XML route structure
routes = etree.Element('routes')
for vehicle in vehicle_routes:
    # Define vehicle and route in XML with sorted order
    vehicle_elem = etree.SubElement(routes, 'vehicle', id=vehicle['id'], type=vehicle['type'],
                                    depart=str(vehicle['depart']))
    route_elem = etree.SubElement(vehicle_elem, 'route', edges=vehicle['route'])

# Close the TraCI connection
traci.close()

# Write to XML file
tree = etree.ElementTree(routes)
tree.write("vehicle_routes/randomRoutes11-1.xml", pretty_print=True, xml_declaration=True, encoding='UTF-8')
