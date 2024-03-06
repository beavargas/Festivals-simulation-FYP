# Festival class and processes
import simpy
import random
import numpy as np


class Festival(object):

    def __init__(self, env, servers, mean_security_time, std_security_time, mean_scan_time, std_scan_time, waiting_times_per_server,  total_festival_goers):
        self.env = env
        self.server = simpy.Resource(env, capacity=servers)
        self.mean_security_time = mean_security_time
        self.std_security_time = std_security_time
        self.mean_scan_time = mean_scan_time
        self.std_scan_time = std_scan_time
        self.waiting_times_per_server = []
        self.total_festival_goers = total_festival_goers
    
    def security_check(self):
        security_time = max(0, np.random.normal(self.mean_security_time, self.std_security_time))
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

def run_festival(env, servers, mean_interarrival, std_interarrival, total_festival_goers, festival):
    festival_goer = 1
    while festival_goer <= total_festival_goers:
        interarrival_time = max(0, random.normalvariate(mean_interarrival, std_interarrival))
        yield env.timeout(interarrival_time)
        env.process(go_to_festival(env, festival))
        festival_goer += 1

        


