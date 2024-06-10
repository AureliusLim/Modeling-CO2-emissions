# import os
# import sys
# if 'SUMO_HOME' in os.environ:
#     print(os.environ['SUMO_HOME'])
#     sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
# else:
#     sys.exit("Environment variable 'SUMO_HOME' not found")

# import traci
# import logging

# sumoBinary = "sumo-gui"
# sumoCmd  = [sumoBinary, 
#             "-c", "config.sumo.cfg",
#             "-d", "200"]

# logging.basicConfig(level=logging.DEBUG)

# try:
    
   
#     traci.start(sumoCmd)
#     step = 0
#     while step < 10000: 
#         traci.simulationStep()  

      
#         sim_time = traci.simulation.getTime()

   
#         vehicle_ids = traci.vehicle.getIDList()

       
#         for vehicle_id in vehicle_ids:
#             position = traci.vehicle.getPosition(vehicle_id)
#             print(f"Vehicle {vehicle_id} is at position {position} at time {sim_time}")

#         step += 1
# finally:
   
#     traci.close()
