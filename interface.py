import traci
import xml.etree.ElementTree as ET

# Start SUMO and connect to TraCI
sumoBinary = "sumo-gui"
sumoCmd = [sumoBinary, "-c", "config.sumo.cfg"]
traci.start(sumoCmd)

# Global counter for passenger IDs
passenger_counter = 0

# Dictionary to track which jeepneys are assigned stops for which passengers
jeepney_stop_assignments = {}
jeepney_id_list = []
passenger_destinations = {}

# Parse the XML file
tree = ET.parse('person_flows.rou.xml')
root = tree.getroot()

# Populate jeepney_id_list
for i in range(1, 10):
    jeepney_id_list.append(f'jeepney_{i}')

# Populate passenger_destinations from the XML file
for person_elem in root.findall('person'):
    person_id = person_elem.get('id')
    ride_elem = person_elem.find('ride')
    if ride_elem is not None:
        to_edge = ride_elem.get('to')
        passenger_destinations[person_id] = to_edge


for person_elem in root.findall('personFlow'):
    pflow_id = person_elem.get('id')
    ride_elem = person_elem.find('ride')
    for i in range(0, int(person_elem.get('number'))):
        to_edge = ride_elem.get('to')
        passenger_destinations[f'{pflow_id}.{i}'] = to_edge
       
print(passenger_destinations)

# Check if an edge ID is a valid road segment (not a cluster or special identifier)
def is_valid_road_edge(edge_id):
    return edge_id and not edge_id.startswith(':')

# Main simulation loop
def simulate():
    try:
        print("Starting simulation.")
        step = 0
        while step < 1000000000000000000000000000000000000000000000000000000000000000:
            traci.simulationStep()

            if step % 10 == 0:
                # Check for jeepneys and passengers on the same edge
                for jeepney_id in jeepney_id_list:
                    
                    jeepney_edge = traci.vehicle.getRoadID(jeepney_id)

                    if jeepney_edge == '-29377703#0':
                        print(f"Jeepney {jeepney_id} reached the last edge in its route.")
                        jeepney_id_list.remove(jeepney_id)
                    if not is_valid_road_edge(jeepney_edge):
                        continue

                    jeepney_capacity = traci.vehicle.getPersonCapacity(jeepney_id)
                    jeepney_passengers = traci.vehicle.getPersonNumber(jeepney_id)
                    
                    if jeepney_passengers < jeepney_capacity:  # Check if jeepney is not full
                        for passenger_id in traci.person.getIDList():
                            passenger_edge = traci.person.getRoadID(passenger_id)
                            if not is_valid_road_edge(passenger_edge):
                                continue

                            if jeepney_edge == passenger_edge:
                                if jeepney_id not in jeepney_stop_assignments:
                                    jeepney_stop_assignments[jeepney_id] = []

                                if passenger_id not in jeepney_stop_assignments[jeepney_id]:
                                    try:
                                        #stop on the spawn edge of the passenger
                                        traci.vehicle.setBusStop(vehID=jeepney_id, stopID=jeepney_edge, duration=15)
                                        jeepney_stop_assignments[jeepney_id].append(passenger_id)
                                       
                                        print(f"Jeepney {jeepney_id} set to stop at bus stop {jeepney_edge} for passenger {passenger_id}.")
                                    except traci.exceptions.TraCIException as e:
                                        print(f"Error setting bus stop for jeepney {jeepney_id} at {jeepney_edge}: {e}")
                                else:
                                    continue
                    else:
                        print(f"Jeepney {jeepney_id} is full. Not setting any stops.")
            
            # Check for passengers reaching their destination
            for passenger_id in list(traci.person.getIDList()):
                current_edge = traci.person.getRoadID(passenger_id)
                if not is_valid_road_edge(current_edge):
                    continue
                
                if current_edge == passenger_destinations.get(passenger_id):
                    traci.person.remove(passenger_id)
                    print(f"Passenger {passenger_id} has reached their destination and has been removed.")

                    for jeepney_id, assigned_passengers in list(jeepney_stop_assignments.items()):
                        if passenger_id in assigned_passengers and traci.vehicle.getRoadID(jeepney_id) == current_edge:
                            #stop on the destination edge of the passenger
                            traci.vehicle.setBusStop(vehID=jeepney_id, stopID=current_edge, duration=15)
                            print(f"Jeepney {jeepney_id} stopped at {jeepney_edge} for passenger {passenger_id}.")
                            jeepney_stop_assignments[jeepney_id].remove(passenger_id)
                            if not jeepney_stop_assignments[jeepney_id]:
                                del jeepney_stop_assignments[jeepney_id]

            step += 1
        print("Simulation ended.")
    except traci.exceptions.TraCIException as e:
        print(f"Error in simulation loop: {e}")
    finally:
        traci.close()

# Run the simulation
simulate()
