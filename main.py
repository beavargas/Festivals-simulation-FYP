# Main file 
import json
import pandas as pandas
import random
import simpy
from Festival import Festival
from Festival import go_to_festival
from Festival import run_festival



# The following function loads the config.json file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def main():

    # Loading the configuration file
    config = load_config('config.json')

    # Creating a list that stores dictionaries for each simulation run
    simulation_data = []

    for servers in config["server_values"]:

        server_i_data = []

        random.seed(42)

        # Creating a simulation enviroment
        env = simpy.Enviroment()

        # Creating a Festival instance
        festival = Festival(env, servers, config["mean_scan_time"], config["std_scan_time"])

        # Running the festival simulation process
        env.process(run_festival(env, servers, config['mean_interarrival'], config['std_interarrival'],  config["total festival goers"], festival))
    
        # Running the simulation until a specified duration
        env.run(until=config['simulation_duration'])


    return

if __name__ == '__main__':
    main()