import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
else:
    sys.exit("Environment variable 'SUMO_HOME' not found")

import traci
import logging

sumoBinary = "sumo-gui"
logFile = "sumo.log"
sumoCmd  = [sumoBinary, 
            "-c", "config.sumo.cfg",
            "--log", logFile]

#logging.basicConfig(level=logging.DEBUG)

try:
    # Start SUMO as a subprocess and connect to it with TRACI
   
    traci.start(sumoCmd)
    step = 0
    while step < 10000:  # Number of simulation steps
        traci.simulationStep()  # Advance the simulation by one step

        # Get the current simulation time
        sim_time = traci.simulation.getTime()

        # Example: Get the list of vehicle IDs currently in the simulation
        vehicle_ids = traci.vehicle.getIDList()

        # Example: Print vehicle IDs and their positions
        for vehicle_id in vehicle_ids:
            position = traci.vehicle.getPosition(vehicle_id)
            print(f"Vehicle {vehicle_id} is at position {position} at time {sim_time}")

        step += 1
finally:
    # Close the connection to SUMO
    traci.close()
