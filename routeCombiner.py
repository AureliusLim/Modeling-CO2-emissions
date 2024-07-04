import xml.etree.ElementTree as ET

# Define the mapping of file names to prefixes
file_prefixes = {
    "randomTrips_car.rou.xml": "car",
    "randomTrips_bus.rou.xml": "bus",
    "randomTrips_truck.rou.xml": "truck",
    "randomTrips_motorcycle.rou.xml": "motorcycle",
    "randomTrips_bicycle.rou.xml": "bicycle"
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
