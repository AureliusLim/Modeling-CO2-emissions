import numpy as np
import traci
import xml.etree.ElementTree as ET
import joblib
from rtree import index
import xml.etree.ElementTree as ET


# Load the trained HMM model
trad_model = joblib.load('trained_hmm_model.pkl')
modern_model = joblib.load('trained_hmm_model_modern.pkl')
# Define state mappings
hidden_state_map = {'Vehicle': 0, 'Passenger': 1, 'Stoplight': 2}
observed_state_map = {'Go': 0, '1 Lane Right': 1, 'Load': 2, 'Stop': 3, '1 Lane Left': 4, 'Unload': 5, 'Wait': 6, '2 Lane Left': 7, '2 Lane Right': 8}

# Define reverse mappings for easy lookup
reverse_hidden_state_map = {v: k for k, v in hidden_state_map.items()}
reverse_observed_state_map = {v: k for k, v in observed_state_map.items()}
# Initialize the spatial index
spatial_index = index.Index()

def populate_spatial_index():
    for passenger_id in traci.person.getIDList():
        passenger_edge = traci.person.getRoadID(passenger_id)
        if is_valid_road_edge(passenger_edge):
            passenger_position = traci.person.getPosition(passenger_id)
            spatial_index.insert(passenger_id, (*passenger_position, *passenger_position))

# Function to get nearby passengers using the spatial index
def get_nearby_passengers(vehicle_id):
    vehicle_position = traci.vehicle.getPosition(vehicle_id)
    x, y = vehicle_position
    # Define a bounding box around the vehicle for spatial query
    bbox = (x - 100, y - 100, x + 100, y + 100)  # Adjust the bounding box size as needed
    nearby_passengers = []
    for passenger_id in spatial_index.intersection(bbox):
        nearby_passengers.append(passenger_id)
# Function to check if there are passengers on the current edge
def get_passengers_on_edge(vehicle_edge):
    passenger_ids = []
    for passenger_id in traci.person.getIDList():
        passenger_edge = traci.person.getRoadID(passenger_id)
        if vehicle_edge == passenger_edge and is_valid_road_edge(passenger_edge):
            passenger_ids.append(passenger_id)
    return passenger_ids
    
    return nearby_passengers
# Function to sample the observed state for a given hidden state
def sample_observed_state(hidden_state, model):
    # Get the emission probabilities for the current hidden state
    emission_probs = model.emissionprob_[hidden_state]
    
    # Sample the observed state based on the emission probabilities
    observed_state = np.random.choice(len(emission_probs), p=emission_probs)
    
    return observed_state

def predict_next_state_with_observation(nearby_passengers):
    # Manually set the state to "Passenger" or "Stoplight" if conditions are met

    if nearby_passengers:
        return hidden_state_map['Passenger']  # Set to Passenger state if passengers are nearby
    # elif stoplight_present:
    #     return hidden_state_map['Stoplight']  # Set to Stoplight state if a stoplight is detected
    else:
        return hidden_state_map['Vehicle']  # Default to Vehicle (Go) state




# Global counter for passenger IDs
passenger_counter = 0

# Dictionary to track which jeepneys are assigned stops for which passengers
jeepney_stop_assignments = {}
traditional_id_list = []
modern_id_list = []
passenger_destinations = {}

# Parse the XML file
tree = ET.parse('person_flows.rou.xml')
root = tree.getroot()



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

nearby_passengers = []
# Main simulation loop

def simulate():
    try:
        print("Starting simulation.")
        step = 0

        # Initialize the state for each jeepney
        jeepney_states = {
            f"jeepney_{jeepney_id}": {
                'hidden_state': hidden_state_map['Vehicle'], 
                'observed_state': observed_state_map['Go']
            } 
            for jeepney_id in range(highest_jeepney_id + 1)
        }

        # Initialize jeepney_states for modern jeepneys (modernjeepney_0 to modernjeepney_highest_modernjeepney_id)
        jeepney_states.update({
            f"modernjeepney_{jeepney_id}": {
                'hidden_state': hidden_state_map['Vehicle'], 
                'observed_state': observed_state_map['Go']
            } 
            for jeepney_id in range(highest_modernjeepney_id + 1)
        })
     
        while step <= 7200:  # Set a reasonable number of simulation steps
            traci.simulationStep()
            if step % 1 == 0:   
                co2_emissions = {}
                for veh_id in traci.vehicle.getIDList():
                   
                    co2_emissions[veh_id] = traci.vehicle.getCO2Emission(veh_id)
                    
                with open('Emission Output/emissions.txt', 'a') as f:
                    f.write(f"Step {step}:\n")
                    for vehicle_id, co2 in co2_emissions.items():
                        f.write(f"  Vehicle {vehicle_id}: CO2 emissions = {co2} g\n")
            for jeepney_id in traci.vehicle.getIDList():
              
                    
                    # Process or save CO2 emissions data as needed
                   

                if step % 5 == 0:
                # Check for jeepneys and passengers on the same edge
                  
                    if jeepney_id.startswith("jeepney_") or jeepney_id.startswith("modernjeepney_"):
                        
                        jeepney_edge = traci.vehicle.getRoadID(jeepney_id)
                        passengers_on_edge = []
                        if step % 1 == 0:
                            #nearby_passengers = get_nearby_passengers(jeepney_id)
                            # Get passengers on the same edge as the jeepney
                            passengers_on_edge = get_passengers_on_edge(jeepney_edge)

                        if not is_valid_road_edge(jeepney_edge):
                            continue

                        current_lane = traci.vehicle.getLaneIndex(jeepney_id)
                        num_lanes = traci.edge.getLaneNumber(jeepney_edge)
                        jeepney_capacity = traci.vehicle.getPersonCapacity(jeepney_id)
                        jeepney_passengers = traci.vehicle.getPersonNumber(jeepney_id)

                        current_state = jeepney_states[jeepney_id]['hidden_state']
                        current_obs = np.array([jeepney_states[jeepney_id]['observed_state'], jeepney_passengers])
                    
                        model = trad_model if jeepney_id in traditional_id_list else modern_model
                        
                        next_hidden_state = hidden_state_map['Vehicle']

                        # Sample the observed state for the next hidden state
                        next_observed_state = sample_observed_state(next_hidden_state, model)
                        

                        # Update the jeepney's state
                        jeepney_states[jeepney_id] = {'hidden_state': next_hidden_state, 'observed_state': next_observed_state}

                        # Execute actions based on the next observed state
                        observed_state_name = reverse_observed_state_map[next_observed_state]
                        hidden_state_name = reverse_hidden_state_map[next_hidden_state]
                        #print(f'{jeepney_id}: {observed_state_name} : {hidden_state_name}')
                        if observed_state_name == 'Go':
                            traci.vehicle.setSpeed(jeepney_id, traci.vehicle.getAllowedSpeed(jeepney_id))
                        elif observed_state_name in ['Stop', 'Load', 'Unload', 'Wait']:
                            
                            if step % 100 == 0:
                                try:
                                    traci.vehicle.setBusStop(jeepney_id, jeepney_edge, duration=5)
                                    #print(f"Jeepney {jeepney_id} set to wait at bus stop {jeepney_edge}")
                                except traci.exceptions.TraCIException as e:
                                            print(f"Error setting bus stop for jeepney {jeepney_id} at {jeepney_edge}: {e}")

                    
                        elif observed_state_name == '1 Lane Right':
                        
                            
                            if current_lane - 1 > 0:
                        
                                traci.vehicle.changeLaneRelative(jeepney_id, -1, 10.0)
                        elif observed_state_name == '1 Lane Left':
                        
                        
                            if current_lane + 1 < num_lanes - 1:
                            
                                traci.vehicle.changeLaneRelative(jeepney_id, 1, 10.0)
                        elif observed_state_name == '2 Lane Right':
                            
                            if current_lane - 1 > 1:
                        
                                traci.vehicle.changeLaneRelative(jeepney_id, -2, 10.0)
                        elif observed_state_name == '2 Lane Left' and step % 20 == 0:
                            
                            if current_lane + 1 < num_lanes - 2:
                        
                                traci.vehicle.changeLaneRelative(jeepney_id, 2, 10.0)

                        # Check if the jeepney can pick up passengers
                        if jeepney_passengers < jeepney_capacity:  # Check if jeepney is not full
                            for passenger_id in passengers_on_edge:
                                #print(passenger_id)
                                if passenger_id not in traci.person.getIDList():
                                    print(f"Passenger {passenger_id} has already been removed or is not found.")
                                    continue
                                passenger_edge = traci.person.getRoadID(passenger_id)
                                if not is_valid_road_edge(passenger_edge):
                                    continue

                                if jeepney_edge == passenger_edge:
                                    if jeepney_id not in jeepney_stop_assignments:
                                        jeepney_stop_assignments[jeepney_id] = []

                                    if passenger_id not in jeepney_stop_assignments[jeepney_id]:
                            
                                        try:
                                        
                                            traci.vehicle.setBusStop(jeepney_id, jeepney_edge, duration=10)
                                            jeepney_states[jeepney_id] =  {'hidden_state': hidden_state_map['Passenger'], 'observed_state': observed_state_map['Load']} 
                                            jeepney_stop_assignments[jeepney_id].append(passenger_id)
                                            print(f"Jeepney {jeepney_id} set to stop at bus stop {jeepney_edge} for passenger {passenger_id}.")
                                        except traci.exceptions.TraCIException as e:
                                            print(f"Error setting bus stop for jeepney {jeepney_id} at {jeepney_edge}: {e}")
            # Check for passengers reaching their destination
            for passenger_id in list(traci.person.getIDList()):
                current_edge = traci.person.getRoadID(passenger_id)
                if not is_valid_road_edge(current_edge):
                    continue

                if current_edge == passenger_destinations.get(passenger_id):
                    assigned_jeepney = None

                    # Find the jeepney assigned to this passenger
                    for jeepney_id, assigned_passengers in jeepney_stop_assignments.items():
                        if passenger_id in assigned_passengers:
                            assigned_jeepney = jeepney_id
                            break

                    if assigned_jeepney:
                        try:
                            # Remove the passenger from the jeepney's assignment
                            jeepney_stop_assignments[assigned_jeepney].remove(passenger_id)
                            if not jeepney_stop_assignments[assigned_jeepney]:
                                del jeepney_stop_assignments[assigned_jeepney]

                            # Set the bus stop and unload the passenger
                            # traci.vehicle.setBusStop(assigned_jeepney, current_edge, duration=10)
                            # print(f"Jeepney {assigned_jeepney} stopped at {current_edge} for passenger {passenger_id}.")
                            
                            # Check if the passenger still exists before removing
                            if passenger_id in traci.person.getIDList():
                                #traci.person.remove(passenger_id)
                                print(f"Passenger {passenger_id} has reached their destination and has been removed.")
                            else:
                                print(f"Passenger {passenger_id} has already been removed or is not found.")
                            
                            jeepney_states[assigned_jeepney] = {'hidden_state': hidden_state_map['Passenger'], 'observed_state': observed_state_map['Unload']}

                        except traci.exceptions.TraCIException as e:
                            print(f"passenger already removed {passenger_id}: {e}")
                        except ValueError as e:
                            print(f"Error removing passenger from jeepney's assignment: {e}")
                    

                    

            step += 1
        print("Simulation ended.")
    except traci.exceptions.TraCIException as e:
        print(f"Error in simulation loop: {e}")
    finally:
        traci.close()

# Run the simulation

print("[1] 7AM - 9AM\n[2] 11AM - 1PM\n[3] 4PM - 6PM")
mode = int(input("Mode: "))
configFile = ""

# Validate input range
if mode in [1, 2, 3]:
    # Assign configFile based on mode
    if mode == 1:
        configFile = "config1.sumo.cfg"
    elif mode == 2:
        configFile = "config2.sumo.cfg"
    elif mode == 3:
        configFile = "config3.sumo.cfg"
    
    # Start SUMO and connect to TraCI (assuming your existing setup)
    sumoBinary = "sumo-gui"
    # Parse the XML file
    config = 'poisson' + str(mode) + '.rou.xml' 
    tree = ET.parse(config)
    root = tree.getroot()

    # Initialize variables to store the highest IDs
    highest_jeepney_id = -1
    highest_modernjeepney_id = -1

    # Loop through all vehicle elements
    for vehicle in root.findall('vehicle'):
        vehicle_id = vehicle.get('id')
        
        # Check if the vehicle ID starts with "jeepney_"
        if vehicle_id.startswith("jeepney_"):
            jeepney_num = int(vehicle_id.split('_')[1])
            if jeepney_num > highest_jeepney_id:
                highest_jeepney_id = jeepney_num
        
        # Check if the vehicle ID starts with "modernjeepney_"
        elif vehicle_id.startswith("modernjeepney_"):
            modernjeepney_num = int(vehicle_id.split('_')[1])
            if modernjeepney_num > highest_modernjeepney_id:
                highest_modernjeepney_id = modernjeepney_num
    # Proceed with SUMO initialization and other operations
    
    print(f"Selected mode {mode}. Using configuration file: {configFile}")
else:
    print("Invalid mode selection. Please choose between 1, 2, or 3.")

sumoCmd = [sumoBinary, "-c", configFile]
traci.start(sumoCmd)
simulate()
