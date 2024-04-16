import simpy
import numpy as np
import json
from case_study_festival import Festival, run_festival, generate_bimodal_interarrival

# The following function loads the config.json file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
    
# Loading the configuration file
config = load_config('case_study_config.json')

# Function to run the simulation and collect results
def simulate_festival(total_festival_goers, simulation_duration, servers,  mean_arrival_high, std_arrival_high, weight_arrival_high, mean_arrival_low, std_arrival_low, weight_arrival_low, mean_group_size, std_group_size, mean_security_time_short, std_security_time_short, mean_security_time_long, std_security_time_long, mean_scan_time, std_scan_time, initial_waiting):
    # Create environment

    env = simpy.Environment()
    print("Creating environment...")

    # Create festival instance
    festival = Festival(env, servers, mean_security_time_short, std_security_time_short, mean_security_time_long, std_security_time_long, mean_scan_time, std_scan_time, [], total_festival_goers)
    print("Creating festival instance...")

    # Run festival simulation
    env.process(run_festival(env, servers,  mean_arrival_high, std_arrival_high, weight_arrival_high, mean_arrival_low, std_arrival_low, weight_arrival_low, total_festival_goers, mean_group_size, std_group_size, initial_waiting, festival))
    env.run(until=simulation_duration)
    print("Running festival simulation...")

    # Count number of people leaving the queue at each time step
    time_steps = np.arange(0, env.now + 1)
    print("time steps...", time_steps)

    print("At main... people leaving queue",festival.people_leaving_queue)
    print("len peopel leaving queue",len(festival.people_leaving_queue))

    # leaving_counts = []

    # for t in time_steps:
    #     #print("for loop at time_step =", t)
    #     count = festival.people_leaving_queue.count(t)
    #     #print("for loop at count...", count)
    #     leaving_counts.append(count)
    #     #print("for loop at leaving_counts...")
    #     #print("leaving counts:", leaving_counts)


    #leaving_counts = [festival.people_leaving_queue.count(t) for t in time_steps]
    print("Counting number of people leaving the queue...")

    results = {
        "people_leaving_queue": festival.people_leaving_queue
    }
    print("Preparing results...")

    return results


# Run simulation
results = simulate_festival(config["total_festival_goers"], config["simulation_duration"], config["servers"],  config["mean_arrival_high"], config["std_arrival_high"], config["weight_arrival_high"], config["mean_arrival_low"], config["std_arrival_low"], config["weight_arrival_low"], config["mean_group_size"], config["std_group_size"], config["mean_security_time_short"], config["std_security_time_short"], config["mean_security_time_long"], config["std_security_time_long"], config["mean_scan_time"], config["std_scan_time"], config["initial_waiting"])

print("Storing results in a JSON file...")
# Store results in a JSON file
output_file = "case_study_servers.json"
with open(output_file, "w") as f:
    json.dump(results, f)


print("Simulation results saved to", output_file)
