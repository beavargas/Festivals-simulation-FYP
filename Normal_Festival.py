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
        self.queue_length = 0
    
    def security_check(self):
        security_time = max(0, np.random.normal(self.mean_security_time, self.std_security_time))
        yield self.env.timeout(security_time)

    def ticket_scan(self):
        scanning_time = max(0, np.random.normal(self.mean_scan_time, self.std_scan_time))
        yield self.env.timeout(scanning_time)

    def get_waiting_times_per_server(self):
        return np.array(self.waiting_times_per_server)

def go_to_festival(env, festival):

    arrival_time = env.now # Record the current simulation time

    festival.queue_length += 1

    # Perform security check
    yield env.process(festival.security_check())

    with festival.server.request() as request:
        yield request
        yield env.process(festival.ticket_scan())

    festival.queue_length -= 1
    
    festival_goer_waiting_time = env.now - arrival_time
    festival.waiting_times_per_server.append(festival_goer_waiting_time)
    return festival_goer_waiting_time

def run_festival(env, servers, mean_interarrival, std_interarrival, total_festival_goers, mean_group_size, std_group_size, festival):
    festival_goer = 0
    while festival_goer <= total_festival_goers:
        interarrival_time = max(0, random.normalvariate(mean_interarrival, std_interarrival))

        group_size = max(1, round(random.normalvariate(mean_group_size, std_group_size)))

        remaining_people = total_festival_goers - festival_goer

        group_size = min(group_size, remaining_people)
    
        for person in range(group_size):
                yield env.timeout(interarrival_time)
                env.process(go_to_festival(env, festival))
                #print(interarrival_time)
            
        festival_goer += group_size
        #print(festival_goer)

        if festival_goer >= total_festival_goers:
            break


        


