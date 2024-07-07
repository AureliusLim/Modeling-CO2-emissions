import traci
import sumolib
import random
import math

# Start SUMO and connect to TraCI
sumoBinary = "sumo-gui"  # or "sumo" for command line interface
sumoCmd = [sumoBinary, "-c", "config.sumo.cfg"]
traci.start(sumoCmd)

step = 0

# Get list of all jeepneys in the simulation

while step < 10000:
    traci.simulationStep()

    # Check if a jeepney should stop
    if random.random() < 0.01:  # Adjust probability as needed
        jeepney_ids = traci.vehicle.getIDList()

        for vehicle_id in jeepney_ids:
            if traci.vehicle.getTypeID(vehicle_id) == "traditional_jeepney":
                current_edge = traci.vehicle.getRoadID(vehicle_id)
                
                try:
                    # Set a temporary stop on the current lane
                    traci.vehicle.setStop(vehicle_id, edgeID=current_edge, laneIndex=1, duration=60.0)
                    print(f"Stopped {vehicle_id} on edge {current_edge} for 60 seconds.")
                except traci.exceptions.TraCIException as e:
                    print(f"Error setting stop for {vehicle_id}: {e}")

    step += 1

# End SUMO simulation
traci.close()