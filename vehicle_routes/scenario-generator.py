import csv
import traci
import random
from lxml import etree

# Specify SUMO binary
sumo_binary = "sumo"  # Use "sumo-gui" for visual debugging
traci.start([sumo_binary, "-n", "edited.net.xml"])

# Retrieve all edges from the SUMO network
all_edges = traci.edge.getIDList()

# XML root for trips with noNamespaceSchemaLocation attribute
root = etree.Element("routes")
root.set("{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation", "http://sumo.dlr.de/xsd/routes_file.xsd")

# Function to generate a valid end edge
def get_valid_end_edge(start_edge):
    attempts = 0
    while attempts < 10:  
        end_edge = random.choice(all_edges)
        if end_edge != start_edge:
            try:
                route = traci.simulation.findRoute(start_edge, end_edge)
                if len(route.edges) >= 5: 
                    return end_edge
            except traci.exceptions.TraCIException:
                pass  
        attempts += 1
    return None  


data = []
with open("vehicle_routes/validationtrad11-1.csv", mode="r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        entry = [
            int(row["Time"]),
            row["edge"],
            int(row["Car Count"] or 0),
            int(row["Truck Count"] or 0),
            int(row["Motorbike Count"] or 0),
            int(row["Bicycle Count"] or 0),
            int(row["Bus Count"] or 0)
        ]
        data.append(entry)


vehicle_id_counters = {
    "car": 0,
    "truck": 0,
    "motorcycle": 0,
    "bicycle": 0,
    "bus": 0
}


for entry in data:
    time, start_edge, car_count, truck_count, motorbike_count, bicycle_count, bus_count = entry


    for vehicle_type, count in zip(
        ["car", "truck", "motorcycle", "bicycle", "bus"],
        [car_count, truck_count, motorbike_count, bicycle_count, bus_count]
    ):
        for _ in range(count):
            end_edge = get_valid_end_edge(start_edge)
            if end_edge:
              
                trip_id = f"{vehicle_type}_{vehicle_id_counters[vehicle_type]}"
                vehicle_id_counters[vehicle_type] += 1
                
             
                trip_attributes = {
                    'id': trip_id,
                    'type': vehicle_type,
                    'depart': str(time),
                    'from': start_edge,
                    'to': end_edge
                }

                
                etree.SubElement(root, 'trip', **trip_attributes)


tree = etree.ElementTree(root)
tree.write("vehicle_routes/trips.xml", pretty_print=True, xml_declaration=True, encoding="UTF-8")


traci.close()
