import numpy as np
import traci
import xml.etree.ElementTree as ET
import joblib

# Load the trained HMM model
trad_model = joblib.load('trained_hmm_model.pkl')
modern_model = joblib.load('trained_hmm_model_modern.pkl')
# Define state mappings
hidden_state_map = {'Vehicle': 0, 'Passenger': 1, 'Stoplight': 2}
observed_state_map = {'Go': 0, '1 Lane Right': 1, 'Load': 2, 'Stop': 3, '1 Lane Left': 4, 'Unload': 5, 'Wait': 6, '2 Lane Left': 7, '2 Lane Right': 8}

# Define reverse mappings for easy lookup
reverse_hidden_state_map = {v: k for k, v in hidden_state_map.items()}
reverse_observed_state_map = {v: k for k, v in observed_state_map.items()}

# # # Function to sample the observed state for a given hidden state
def sample_observed_state(hidden_state, model):
    means = model.means_[hidden_state]
    covars = model.covars_[hidden_state]
    
    # Ensure covars is a 2D square matrix
    if covars.ndim == 1:
        covars = np.diag(covars)  # Convert variances to a covariance matrix
    
    # Check covars is 2D and square
    if covars.ndim != 2 or covars.shape[0] != covars.shape[1]:
        raise ValueError("Covariance matrix must be 2 dimensional and square.")
    
    observed_state = np.random.multivariate_normal(means, covars).astype(int)
    observed_state = np.clip(observed_state, 0, len(observed_state_map) - 1)  # Ensure valid observed state
    return observed_state[0]

def predict_next_state_with_observation(model, current_hidden_state, observation):
    # Get the transition probabilities for the current hidden state
    trans_probs = model.transmat_[current_hidden_state]
    
    # Adjust transition probabilities based on the observation (e.g., passenger load)
    # This is a simplified example; you might need a more sophisticated adjustment
    passenger_load = observation[1]
    adjusted_probs = trans_probs * (1 + passenger_load / 10.0)  # Adjust based on load
    adjusted_probs /= np.sum(adjusted_probs)  # Normalize to ensure they sum to 1
    
    next_state = np.random.choice(len(adjusted_probs), p=adjusted_probs)
    return next_state




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

# Populate jeepney_id_list
for i in range(1, 6):
    traditional_id_list.append(f'jeepney_{i}')
    modern_id_list.append(f'modernjeepney_{i}')

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

midtrip_edge = '615456195'
endtrip_edge = '16174062#0'
# Main simulation loop
def simulate():
    try:
        print("Starting simulation.")
        step = 0

        # Initialize the state for each jeepney
        jeepney_states = {jeepney_id: {'hidden_state': hidden_state_map['Vehicle'], 'observed_state': observed_state_map['Go']} for jeepney_id in traditional_id_list + modern_id_list}
        
        while step >= 0:  # Set a reasonable number of simulation steps
            traci.simulationStep()
            if step % 1 == 0:
                co2_emissions = {}
                
                # Retrieve CO2 emissions for traditional jeepneys
                for jeepney_id in traditional_id_list:
                    co2_emissions[jeepney_id] = traci.vehicle.getCO2Emission(jeepney_id)
                
                # Retrieve CO2 emissions for modern jeepneys
                for jeepney_id in modern_id_list:
                    co2_emissions[jeepney_id] = traci.vehicle.getCO2Emission(jeepney_id)
                
                # Process or save CO2 emissions data as needed
                with open('Emission Output/co2_emissions.txt', 'a') as f:
                    f.write(f"Step {step}:\n")
                    for vehicle_id, co2 in co2_emissions.items():
                        f.write(f"  Vehicle {vehicle_id}: CO2 emissions = {co2} g\n")
            if step % 10 == 0:
                # Check for jeepneys and passengers on the same edge
                for jeepney_id in traditional_id_list + modern_id_list:
                    jeepney_edge = traci.vehicle.getRoadID(jeepney_id)
                    

                    if jeepney_edge == '-29377703#1' and step > 3000:
                        print(f"Jeepney {jeepney_id} reached the last edge in its route.")
                        if jeepney_id in traditional_id_list:
                            traditional_id_list.remove(jeepney_id)
                        elif jeepney_id in modern_id_list:
                            modern_id_list.remove(jeepney_id)
                    if not is_valid_road_edge(jeepney_edge):
                        continue


                    if jeepney_edge == midtrip_edge:
                        traci.vehicle.setMaxSpeed(jeepney_id, 22.22)
                    elif jeepney_edge == endtrip_edge:
                        traci.vehicle.setMaxSpeed(jeepney_id, 11.11)
                    else:
                        traci.vehicle.setMaxSpeed(jeepney_id, 11.11)

                    current_lane = traci.vehicle.getLaneIndex(jeepney_id)
                    num_lanes = traci.edge.getLaneNumber(jeepney_edge)
                    jeepney_capacity = traci.vehicle.getPersonCapacity(jeepney_id)
                    jeepney_passengers = traci.vehicle.getPersonNumber(jeepney_id)

                    current_state = jeepney_states[jeepney_id]['hidden_state']
                    current_obs = np.array([jeepney_states[jeepney_id]['observed_state'], jeepney_passengers])
                    # Select the appropriate model based on jeepney type
                    model = trad_model if jeepney_id in traditional_id_list else modern_model
                    # Predict the next hidden state using the current hidden state and observation
                    next_hidden_state = predict_next_state_with_observation(model, current_state, current_obs)

                    # Sample the observed state for the next hidden state
                    next_observed_state = sample_observed_state(next_hidden_state, model)

                    # Update the jeepney's state
                    jeepney_states[jeepney_id] = {'hidden_state': next_hidden_state, 'observed_state': next_observed_state}

                    # Execute actions based on the next observed state
                    observed_state_name = reverse_observed_state_map[next_observed_state]
                  
                    print(f'{jeepney_id} for {observed_state_name}')
                    if observed_state_name == 'Go':
                        traci.vehicle.setSpeed(jeepney_id, traci.vehicle.getAllowedSpeed(jeepney_id))
                    elif observed_state_name in ['Stop', 'Load', 'Unload', 'Wait']:
                        print(f'{jeepney_id} state stopped')
                        if step % 20 == 0:
                            try:
                                traci.vehicle.setBusStop(jeepney_id, jeepney_edge, duration=5)
                            
                            except traci.exceptions.TraCIException as e:
                                        print(f"Error setting bus stop for jeepney {jeepney_id} at {jeepney_edge}: {e}")

                   
                    # elif observed_state_name == '1 Lane Right':
                       
                        
                    #     if current_lane > 0:
                    #         #print(f'{jeepney_id} lane right')
                    #         traci.vehicle.changeLaneRelative(jeepney_id, -1, 10.0)
                    # elif observed_state_name == '1 Lane Left':
                     
                    #     print(f'{jeepney_id} current_lane: {current_lane}, num_lanes: {num_lanes}')
                    #     if current_lane + 1 < num_lanes - 1:
                    #         print(f'{jeepney_id} lane left')
                    #         traci.vehicle.changeLaneRelative(jeepney_id, 1, 10.0)
                    # elif observed_state_name == '2 Lane Right':
                        
                    #     if current_lane > 1:
                    #         #print(f'{jeepney_id} 2 lane right')
                    #         traci.vehicle.changeLaneRelative(jeepney_id, -2, 10.0)
                    # elif observed_state_name == '2 Lane Left' and step % 20 == 0:
                        
                    #     if current_lane + 1 < num_lanes - 2:
                    #         print(f'{jeepney_id} 2 lane left')
                    #         traci.vehicle.changeLaneRelative(jeepney_id, 2, 10.0)

                    # Check if the jeepney can pick up passengers
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
                                       
                                        traci.vehicle.setBusStop(jeepney_id, jeepney_edge, duration=15)
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
                    traci.person.remove(passenger_id)
                    print(f"Passenger {passenger_id} has reached their destination and has been removed.")

                    for jeepney_id, assigned_passengers in list(jeepney_stop_assignments.items()):
                        if passenger_id in assigned_passengers and traci.vehicle.getRoadID(jeepney_id) == current_edge:
                    
                            traci.vehicle.setBusStop(jeepney_id, current_edge, duration=15)
                            jeepney_states[jeepney_id] =  {'hidden_state': hidden_state_map['Passenger'], 'observed_state': observed_state_map['Unload']} 
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

print("[1] 6AM - 9AM\n[2] 11AM - 2PM\n[3] 3PM - 6PM")
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
    # Proceed with SUMO initialization and other operations
    
    print(f"Selected mode {mode}. Using configuration file: {configFile}")
else:
    print("Invalid mode selection. Please choose between 1, 2, or 3.")

sumoCmd = [sumoBinary, "-c", configFile]
traci.start(sumoCmd)
simulate()
