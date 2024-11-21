import traci

# Start SUMO with TraCI
sumo_binary = "sumo-gui"  # Use "sumo" for GUI version
sumo_options = [
    sumo_binary,
    "-c", "configs/stationary.sumo.cfg",
]
traci.start(sumo_options)

# Simulation parameters
idle_time = 100  # Duration for idling
rev_time = 100  # Duration for revving
vehicle_states = {}  # To store idle/rev states for each vehicle

# Open the file for appending emissions data
with open('Emission Output/emissions.txt', 'a') as f:
    # Main simulation loop
    for step in range(400):  # Simulate for 200 timesteps
        traci.simulationStep()

        # Collect CO2 emissions for all vehicles
        co2_emissions = {
            vehicle_id: traci.vehicle.getCO2Emission(vehicle_id)
            for vehicle_id in traci.vehicle.getIDList()
        }

        # Write emissions data to the file
        f.write(f"Step {step}:\n")
        for vehicle_id, co2 in co2_emissions.items():
            f.write(f"  Vehicle {vehicle_id}: CO2 emissions = {co2} g\n")

        # Process vehicle states
        for vehicle_id in traci.vehicle.getIDList():
            # Initialize state for new vehicles
            if vehicle_id not in vehicle_states:
                vehicle_states[vehicle_id] = {
                    "state": "idle",
                    "end_time": step + idle_time,
                }

            # Get current state and end_time
            state_info = vehicle_states[vehicle_id]
            current_state = state_info["state"]
            end_time = state_info["end_time"]

            if current_state == "idle":
                # Idle phase
                traci.vehicle.setSpeed(vehicle_id, 0)  # Set speed to 0 for idling
                if step >= end_time:  # Transition to rev
                    vehicle_states[vehicle_id]["state"] = "rev"
                    vehicle_states[vehicle_id]["end_time"] = step + rev_time

            elif current_state == "rev":
                # Revving phase
                traci.vehicle.setSpeed(vehicle_id, 11.11)  # Simulate revving
                if step >= end_time:  # Transition to done
                    vehicle_states[vehicle_id]["state"] = "done"

            elif current_state == "done":
                # Resume normal operation (restore vehicle's default behavior)
                traci.vehicle.setSpeed(vehicle_id, -1)  # Reset to normal speed control

# Close TraCI
traci.close()
