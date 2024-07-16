import xml.etree.ElementTree as ET

# Define the mapping of file names to prefixes
file_prefixes = {
    "randomTrips_car1.rou.xml": "car1",
    "randomTrips_bus1.rou.xml": "bus1",
    "randomTrips_truck1.rou.xml": "truck1",
    "randomTrips_motorcycle1.rou.xml": "motorcycle1",
    "randomTrips_bicycle1.rou.xml": "bicycle1",
    "randomTrips_car2.rou.xml": "car2",
    "randomTrips_bus2.rou.xml": "bus2",
    "randomTrips_truck2.rou.xml": "truck2",
    "randomTrips_motorcycle2.rou.xml": "motorcycle2",
    "randomTrips_bicycle2.rou.xml": "bicycle2",
    "randomTrips_car3.rou.xml": "car3",
    "randomTrips_bus3.rou.xml": "bus3",
    "randomTrips_truck3.rou.xml": "truck3",
    "randomTrips_motorcycle3.rou.xml": "motorcycle3",
    "randomTrips_bicycle3.rou.xml": "bicycle3",
}

# Function to modify IDs in a route file
def modify_ids(filename, prefix):
    tree = ET.parse(filename)
    root = tree.getroot()

    for vehicle in root.findall('vehicle'):
        vehicle_id = vehicle.get('id')
        new_vehicle_id = f"{prefix}_{vehicle_id}"
        vehicle.set('id', new_vehicle_id)

    for route in root.findall('route'):
        route_id = route.get('id')
        new_route_id = f"{prefix}_{route_id}"
        route.set('id', new_route_id)

    # Write back to the same file
    tree.write(filename, encoding='utf-8', xml_declaration=True)

# Process each file with its respective prefix
for filename, prefix in file_prefixes.items():
    modify_ids(filename, prefix)

print("Modified route files with unique IDs.")
