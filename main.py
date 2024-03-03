# Main file 
import json
#import pandas as pd
import random
import simpy
import numpy as np
from Normal_Festival import Festival
from Normal_Festival import go_to_festival
from Normal_Festival import run_festival
#from Simple_Festival import Festival
#from Simple_Festival import go_to_festival
#from Simple_Festival import run_festival



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

        server_i_data = []

        random.seed(42)

        # Creating a simulation enviroment
        env = simpy.Environment()

        # Creating a Festival instance
        festival = Festival(env, servers, config["mean_scan_time"], config["std_scan_time"], server_i_data, config["total_festival_goers"])

        # Running the festival simulation process
        env.process(run_festival(env, servers, config['mean_interarrival'], config['std_interarrival'],  config["total_festival_goers"], festival))
    
        # Running the simulation until a specified duration
        env.run(until=config['simulation_duration'])

        # Accessing the waiting times array for each festival goer
        waiting_time_i_servers = festival.get_waiting_times_per_server()

        # Adding the array for i number of servers to the simulation data matrix
        simulation_data = np.vstack((simulation_data, waiting_time_i_servers))

    
    simulation_data = simulation_data[1:] # to remove first row of zeros
    print(simulation_data)

    # Store simulation data in a json file
    with open('simulation_data.json', 'w') as file:
        json.dump(simulation_data.tolist(), file, indent=1)

if __name__ == '__main__':
    main()
    