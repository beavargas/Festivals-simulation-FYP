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
        self.waiting_times_per_server = []
        self.total_festival_goers = total_festival_goers
    
    def security_check(self):
        #security_time = max(0, np.random.normal(self.mean_security_time, self.std_security_time))
        if np.random.rand() < 0.90:  # randomly select between short and long scan
            security_time = max(0, np.random.normal(self.mean_security_time_short, self.std_security_time_short))
        else:
            security_time = max(0, np.random.normal(self.mean_security_time_long, self.std_security_time_long))
        
        yield self.env.timeout(security_time)
    
    def ticket_scan(self):
        scanning_time = max(0, np.random.normal(self.mean_scan_time, self.std_scan_time))
        
        yield self.env.timeout(scanning_time)

    def get_waiting_times_per_server(self):
        #return(self.get_waiting_times_per_server)
        return np.array(self.waiting_times_per_server)

def go_to_festival(env, festival):

    arrival_time = env.now # Record the current simulation time

    # Perform security check
    yield env.process(festival.security_check())

    with festival.server.request() as request:
        yield request
        yield env.process(festival.ticket_scan())
    
    festival_goer_waiting_time = env.now - arrival_time
    festival.waiting_times_per_server.append(festival_goer_waiting_time)
    return festival_goer_waiting_time

def bus_arrivals(env, festival, bus_capacity, bus_interarrival_time):
    while True:
        yield env.timeout(bus_interarrival_time)
        for _ in range(bus_capacity):
            env.process(go_to_festival(env, festival))

def run_festival(env, servers, bus_capacity, bus_interarrival_time, lamda_interarrival, total_festival_goers, mean_group_size, std_group_size, festival):
    festival_goer = 0

    env.process(bus_arrivals(env, festival, bus_capacity, bus_interarrival_time ))

    while festival_goer <= total_festival_goers:
        walking_interarrival_time = max(0, np.random.poisson(lamda_interarrival))

        group_size = max(1, round(np.random.normal(mean_group_size, std_group_size)))

        remaining_people = total_festival_goers - festival_goer

        group_size = min(group_size, remaining_people)
    
        for person in range(group_size):
                yield env.timeout(walking_interarrival_time)
                env.process(go_to_festival(env, festival))
                #print(interarrival_time)
            
        festival_goer += group_size
        #print(festival_goer)

        if festival_goer >= total_festival_goers:
            break
        

        


