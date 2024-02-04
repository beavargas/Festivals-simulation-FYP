# Festival class and processes
import simpy
import random
import numpy as np


class Festival(object):

    def __init__(self, env, servers, mean_scan_time, std_scan_time, waiting_times_per_server):
        self.env = env
        self.server = simpy.Resource(env, capacity=servers)
        self.mean_scan_time = mean_scan_time
        self.std_scan_time = std_scan_time
        self.waiting_times_per_server = []
    
    def ticket_scan(self, festival_goer):
        scanning_time = np.random.normal(self.mean_scan_time, self.std_scan_time)
        yield self.env.timeout(scanning_time)

    def get_waiting_times_per_server(self):
        return np.array(self.waiting_times_per_server)

def go_to_festival(env, festival_goer, festival):
    arrival_time = env.now # Record the current simulation time

    with festival.server.request() as request:
        yield request
        yield env.process(festival.ticket_scan(festival_goer))
    
    festival_goer_waiting_time = env.now - arrival_time
    
