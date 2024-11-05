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
    'intersection1': {'bicycle': 28, 'bus': 0, 'car': 254, 'motorcycle': 705, 'truck': 44, 'traditional_jeepney': 64, 'modern_jeepney': 7},
    'intersection2': {'bicycle': 34, 'bus': 0, 'car': 150, 'motorcycle': 334, 'truck': 32, 'traditional_jeepney': 48, 'modern_jeepney': 6},
    'intersection3': {'bicycle': 16, 'bus': 9, 'car': 505, 'motorcycle': 723, 'truck': 77, 'traditional_jeepney': 26, 'modern_jeepney': 5},
}

# Define mappings of intersection start edges
intersection_edges = {
    'intersection1': intersection1_startedges,
    'intersection2': intersection2_startedges,
    'intersection3': intersection3_startedges
}

jeepney_startedges = {
    'intersection1': ['368461882#0', '-923261416'],
    'intersection2': ['1112806233-AddedOnRampEdge', '-4588647#0'],
    'intersection3': ['704746731#0', '119883577#7'],
}

# Function to choose a valid distant edge using route validation
def get_random_edges_with_validation(start_edge, network_edges):
    while True:
        end_edge = random.choice(network_edges)
        if end_edge != start_edge:  # Ensure end edge is not the same
            route = traci.simulation.findRoute(start_edge, end_edge)
            if len(route.edges) > 2:  # Ensure the route is valid and has more than two edges
                return " ".join(route.edges)

def get_distant_edge(start_edge):
    if start_edge in ["368461882#0", "-4588647#0", "119883577#7"]:
        return "16174062#0"
    else:
        return "-29377703#2"

# Start the TraCI server (necessary for traci functions)
sumo_binary = "sumo"  # or "sumo-gui" for visual debugging
traci.start([sumo_binary, "-n", "edited.net.xml"])

# Prepare to collect vehicles with their routes and departure times
vehicle_routes = []
jeepney_trips = []  # Separate list for jeepney trips
network_edges = [edge.getID() for edge in net.getEdges()]
trad_count = -1
modern_count = -1
# Create routes for each intersection
for intersection, counts in vehicle_counts.items():
    edges = intersection_edges[intersection]
    jeep_start = jeepney_startedges[intersection]
    for vehicle_type, count in counts.items():
        for i in range(count):
    
            if vehicle_type in ['traditional_jeepney', 'modern_jeepney']:
                # Use fixed end edge for jeepneys (for duarouter)
                if vehicle_type == 'traditional_jeepney':
                    name = "jeepney_"
                    trad_count += 1
                    number = trad_count
                elif vehicle_type == 'modern_jeepney':
                    name = 'modernjeepney_'
                    modern_count += 1
                    number = modern_count

                start_edge = random.choice(jeep_start)
                end_edge = get_distant_edge(start_edge)  # Define as appropriate for jeepney routes
                depart_time = random.randint(0, 850)
                jeepney_trips.append({
                    'id': f"{name}{number}",
                    'type': vehicle_type,
                    'depart': depart_time,
                    'from': start_edge,
                    'to': end_edge
                })
            else:
                start_edge = random.choice(edges)
                # For other vehicles, find a full route
                route_edges = get_random_edges_with_validation(start_edge, network_edges)
                depart_time = random.randint(0, 850)
                vehicle_routes.append({
                    'id': f"{vehicle_type}_{intersection}_{i}",
                    'type': vehicle_type,
                    'depart': depart_time,
                    'route': route_edges
                })

# Sort vehicles by departure time
vehicle_routes.sort(key=lambda v: v['depart'])
jeepney_trips.sort(key=lambda v: v['depart'])

# Generate XML route structure
routes = etree.Element(
    'routes',
    nsmap={
        'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
    }
)
# Set the schema location attribute
routes.set(
    '{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation',
    'http://sumo.dlr.de/xsd/routes_file.xsd'
)
for vehicle in vehicle_routes:
    # Define vehicle and route in XML with sorted order
    vehicle_elem = etree.SubElement(routes, 'vehicle', id=vehicle['id'], type=vehicle['type'],
                                    depart=str(vehicle['depart']))
    route_elem = etree.SubElement(vehicle_elem, 'route', edges=vehicle['route'])

# Write jeepney trips to a separate file
jeepney_trips_xml = etree.Element('routes')

for trip in jeepney_trips:
    trip_attributes = {
        'id': trip['id'],
        'type': trip['type'],
        'depart': str(trip['depart']),
        'from': trip['from'],
        'to': trip['to']
    }
    trip_elem = etree.SubElement(jeepney_trips_xml, 'trip', **trip_attributes)

# Close the TraCI connection
traci.close()

# Write to XML files
tree = etree.ElementTree(routes)
tree.write("vehicle_routes/randomRoutes11-1.xml", pretty_print=True, xml_declaration=True, encoding='UTF-8')

jeepney_tree = etree.ElementTree(jeepney_trips_xml)
jeepney_tree.write("vehicle_routes/jeepneyTrips11-1.rou.xml", pretty_print=True, xml_declaration=True, encoding='UTF-8')
