# Festival class and processes
import simpy
import random
import numpy as np


class Festival(object):

    def __init__(self, env, servers, mean_security_time_short, std_security_time_short, mean_security_time_long, std_security_time_long, mean_scan_time, std_scan_time, waiting_times_per_server,  total_festival_goers):
        self.env = env
        self.server = simpy.Resource(env, capacity=servers)
        self.mean_security_time_short = mean_security_time_short
        self.std_security_time_short = std_security_time_short
        self.mean_security_time_long = mean_security_time_long
        self.std_security_time_long = std_security_time_long
        self.mean_scan_time = mean_scan_time
        self.std_scan_time = std_scan_time
        self.total_festival_goers = total_festival_goers
        self.waiting_times_per_server = []
        self.people_leaving_queue = []
    
    def security_check(self):
        #security_time = max(0, np.random.normal(self.mean_security_time, self.std_security_time))
        if np.random.rand() < 0.90:  # randomly select between short and long scan
            security_time = max(0, np.random.normal(self.mean_security_time_short, self.std_security_time_short))
        else:
            security_time = max(0, np.random.normal(self.mean_security_time_long, self.std_security_time_long))
        
        #print(f"Security check started at {self.env.now}")
        yield self.env.timeout(security_time)
        #print(f"Security check finished at {self.env.now}")
    
    def ticket_scan(self):
        scanning_time = max(0, np.random.normal(self.mean_scan_time, self.std_scan_time))
        
        #print(f"Ticket scanning started at {self.env.now}")
        yield self.env.timeout(scanning_time)
        #print(f"Ticket scanning finished at {self.env.now}")

    def get_waiting_times_per_server(self):
        #return(self.get_waiting_times_per_server)
        return np.array(self.waiting_times_per_server)

def go_to_festival(env, festival):

    arrival_time = env.now # Record the current simulation time

    # Perform security check
    #print(f"Festival goer arrived at {env.now}")
    yield env.process(festival.security_check())

    with festival.server.request() as request:
        yield request
        yield env.process(festival.ticket_scan())
        festival.people_leaving_queue.append(env.now)
        #print(f"Festival goer left at {env.now}")
        #print("festival.people_leaving_queue", festival.people_leaving_queue)
    
    festival_goer_waiting_time = env.now - arrival_time
    festival.waiting_times_per_server.append(festival_goer_waiting_time)
    return festival_goer_waiting_time

def generate_bimodal_interarrival(mean_arrival_high, std_arrival_high, weight_arrival_high, mean_arrival_low, std_arrival_low, weight_arrival_low):
    weights = [weight_arrival_high, weight_arrival_low]
    weights /= np.sum(weights)  # Normalize weights to sum up to 1
    choice = np.random.choice([0, 1], p=weights)  # Choose based on weights
    if choice == 0:
        return max(0, np.random.normal(mean_arrival_high, std_arrival_high))
    else:
        return max(0, np.random.normal(mean_arrival_low, std_arrival_low))

def run_festival(env, servers, mean_arrival_high, std_arrival_high, weight_arrival_high, mean_arrival_low, std_arrival_low, weight_arrival_low, total_festival_goers, mean_group_size, std_group_size, initial_waiting, festival):
    
    for _ in range(initial_waiting):
        env.process(go_to_festival(env, festival))
    
    festival_goer = initial_waiting
    while festival_goer <= total_festival_goers:
        interarrival_time = generate_bimodal_interarrival(mean_arrival_high, std_arrival_high, weight_arrival_high, mean_arrival_low, std_arrival_low, weight_arrival_low)

        group_size = max(1, round(np.random.normal(mean_group_size, std_group_size)))

        remaining_people = total_festival_goers - festival_goer

        group_size = min(group_size, remaining_people)
    
        for person in range(group_size):
                yield env.timeout(interarrival_time)
                #print(f"Festival goer arrived at {env.now}")
                env.process(go_to_festival(env, festival))
                #print(interarrival_time)
            
        festival_goer += group_size
        #print(festival_goer)

        if festival_goer >= total_festival_goers:
            break
    print("Exiting run_festival function")
