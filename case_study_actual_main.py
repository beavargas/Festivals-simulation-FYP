import simpy
import numpy as np
import json
from case_study_festival import Festival, run_festival, generate_bimodal_interarrival

def main():
    # The following function loads the config.json file
    def load_config(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
        
    # Loading the configuration file
    config = load_config('case_study_config.json')

    # Function to run the simulation and collect results
    def simulate_festival(total_festival_goers, simulation_duration, servers, mean_arrival_high, std_arrival_high, weight_arrival_high, mean_arrival_low, std_arrival_low, weight_arrival_low, mean_group_size, std_group_size, mean_security_time_short, std_security_time_short, mean_security_time_long, std_security_time_long, mean_scan_time, std_scan_time, initial_waiting):
        all_waiting_times = np.zeros(config["total_festival_goers"])  # List to store results for each server value
        
        for server in servers:
            print("New servers round...")
            server_i_data = []
            # Create environment
            env = simpy.Environment()

            # Create festival instance
            festival = Festival(env, server, mean_security_time_short, std_security_time_short, mean_security_time_long, std_security_time_long, mean_scan_time, std_scan_time, [], total_festival_goers)

            # Run festival simulation
            env.process(run_festival(env, server, mean_arrival_high, std_arrival_high, weight_arrival_high, mean_arrival_low, std_arrival_low, weight_arrival_low, total_festival_goers, mean_group_size, std_group_size, initial_waiting, festival))
            env.run(until=simulation_duration)

            # Store results
            waiting_times = festival.get_waiting_times_per_server()
            print("waiting_times:", waiting_times)
            print("len waiting times:", len(waiting_times))

            try:
                all_waiting_times = np.vstack((all_waiting_times, waiting_times))
            except ValueError:
                print("Error in vertical stacking. Ending simulation.")
                break
            # all_waiting_times[server] = waiting_times
            # print(all_waiting_times)
            # results = {"people_leaving_queue": festival.people_leaving_queue}
            # all_results[server] = results
            print("Shape of simulation_data:", all_waiting_times.shape)
            print("Shape of waiting_time_i_servers:", waiting_times.shape)
        
        print("FINISHED!")

        return all_waiting_times

    # Run simulation
    results = simulate_festival(config["total_festival_goers"], config["simulation_duration"], config["servers"], config["mean_arrival_high"], config["std_arrival_high"], config["weight_arrival_high"], config["mean_arrival_low"], config["std_arrival_low"], config["weight_arrival_low"], config["mean_group_size"], config["std_group_size"], config["mean_security_time_short"], config["std_security_time_short"], config["mean_security_time_long"], config["std_security_time_long"], config["mean_scan_time"], config["std_scan_time"], config["initial_waiting"])

    # Store results in a JSON file
    output_file = "case_study.json"
    with open(output_file, "w") as f:
        json.dump(results.tolist(), f)

    print("Simulation results saved to", output_file)

# If this file is executed directly, call the main function
if __name__ == "__main__":
    main()
