import traci
import sumolib
import random
import math
import xml.etree.ElementTree as ET
# Start SUMO and connect to TraCI
sumoBinary = "sumo-gui"  # or "sumo" for command line interface
sumoCmd = [sumoBinary, "-c", "config.sumo.cfg"]
traci.start(sumoCmd)

# Global counter for passenger IDs
passenger_counter = 0

# Dictionary to track which jeepneys are assigned stops for which passengers
jeepney_stop_assignments = {}
passenger_destinations={
}
# Parse the XML file
tree = ET.parse('person_flows.rou.xml')
root = tree.getroot()

# Iterate over each <person> element in the XML
for person_elem in root.findall('person'):
    person_id = person_elem.get('id')
    ride_elem = person_elem.find('ride')
    if ride_elem is not None:
        to_edge = ride_elem.get('to')
        passenger_destinations[person_id] = to_edge
# Main simulation loop
def simulate():
    try:
        print("Starting simulation.")
        step = 0
        while step < 1000000000000000000000000000000000000000000000000000000000000000:
            traci.simulationStep()

            if step % 10 == 0:
                # Check for jeepneys and passengers on the same edge
                for jeepney_id in traci.vehicle.getIDList():
                    if "jeepney" in jeepney_id:
                        jeepney_edge = traci.vehicle.getRoadID(jeepney_id)
                        jeepney_capacity = traci.vehicle.getPersonCapacity(jeepney_id)
                        jeepney_passengers = traci.vehicle.getPersonNumber(jeepney_id)
                        
                        if jeepney_passengers < jeepney_capacity:  # Check if jeepney is not full
                            for passenger_id in traci.person.getIDList():
                                passenger_edge = traci.person.getRoadID(passenger_id)
                                if jeepney_edge == passenger_edge:
                                    # Check if the jeepney is already assigned to stop for this passenger
                                    if jeepney_id not in jeepney_stop_assignments:
                                        jeepney_stop_assignments[jeepney_id] = []

                                    if passenger_id not in jeepney_stop_assignments[jeepney_id]:
                                        traci.vehicle.setBusStop(vehID=jeepney_id, stopID=jeepney_edge, duration=15)
                                        jeepney_stop_assignments[jeepney_id].append(passenger_id)
                                        traci.vehicle.setBusStop(vehID=jeepney_id, stopID=passenger_destinations.get(passenger_id), duration=15)
                                        print(f"Jeepney {jeepney_id} set to stop at bus stop {jeepney_edge} for passenger {passenger_id}.")
                                    else:
                                        #print(f"Jeepney {jeepney_id} already assigned to stop for passenger {passenger_id}.")
                                        continue
                        else:
                            print(f"Jeepney {jeepney_id} is full. Not setting any stops.")
            
            # Check for passengers reaching their destination
            for passenger_id in list(traci.person.getIDList()):
                current_edge = traci.person.getRoadID(passenger_id)
                
                if current_edge == passenger_destinations.get(passenger_id):
                    # Passenger has reached their destination, remove them from the simulation
                    traci.person.remove(passenger_id)
                    print(f"Passenger {passenger_id} has reached their destination and has been removed.")

                    # Clean up any bus stop assignments related to this passenger
                    for jeepney_id, assigned_passengers in list(jeepney_stop_assignments.items()):
                        if passenger_id in assigned_passengers:
                            
                            assigned_passengers.remove(passenger_id)
                            if not assigned_passengers:
                                del jeepney_stop_assignments[jeepney_id]

            step += 1
        print("Simulation ended.")
    except traci.exceptions.TraCIException as e:
        print(f"Error in simulation loop: {e}")
    finally:
        traci.close()

# Run the simulation
simulate()