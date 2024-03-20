# Main file 
import json
#import pandas as pd
import random
import simpy
import numpy as np
#from Simple_Festival import Festival, go_to_festival, run_festival
#from Normal_Festival import Festival, go_to_festival, run_festival
#from Poisson_Festival import Festival, go_to_festival, run_festival
from Multimodal_Festival import Festival, go_to_festival, run_festival


# The following function loads the config.json file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():

    # Loading the configuration file
    config = load_config('config.json')

    # Creating a list that stores dictionaries for each simulation run
    simulation_data = np.zeros(config["total_festival_goers"])
    
    for servers in config["server_values"]:
        print("new servers round")
        server_i_data = []

        random.seed(42)

        # Creating a simulation enviroment
        env = simpy.Environment()

        # Creating a Festival instance
        #festival = Festival(env, servers, server_i_data, config["total_festival_goers"])
        #festival = Festival(env, servers, config["mean_security_time"], config["std_security_time"], config["mean_scan_time"], config["std_scan_time"], server_i_data, config["total_festival_goers"])
        festival = Festival(env, servers, config["mean_security_time"], config["std_security_time"], config["mean_scan_time"], config["std_scan_time"], server_i_data, config["total_festival_goers"])        
        
        # Running the festival simulation process
        #env.process(run_festival(env, servers, config["total_festival_goers"], festival))
        #env.process(run_festival(env, servers, config['mean_interarrival'], config['std_interarrival'],  config["total_festival_goers"], config["mean_group_size"], config["std_group_size"], festival))
        env.process(run_festival(env, servers, config["lamda_interarrival"], config["total_festival_goers"], config["mean_group_size"], config["std_group_size"], festival))
        
        # Running the simulation until a specified duration
        env.run(until=config['simulation_duration'])

        # Accessing the waiting times array for each festival goer
        waiting_time_i_servers = festival.get_waiting_times_per_server()
        #print("waiting_time_i_servers")
        #print(waiting_time_i_servers)
        
        # Adding the array for i number of servers to the simulation data matrix
        try:
            simulation_data = np.vstack((simulation_data, waiting_time_i_servers))
        except ValueError:
            print("Error in vertical stacking. Ending simulation.")
            break
        #simulation_data = np.vstack((simulation_data, waiting_time_i_servers))
        #print("simualtion data")
        #print(simulation_data)

    
    simulation_data = simulation_data[1:] # to remove first row of zeros
    #print(simulation_data)

    # Store simulation data in a json file
    with open('simulation_data.json', 'w') as file:
        json.dump(simulation_data.tolist(), file, indent=1)

if __name__ == '__main__':
    main()
    