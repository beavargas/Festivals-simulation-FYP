# Festival class and processes
import simpy
import random
import numpy as np


class Festival(object):

    def __init__(self, env, servers, waiting_times_per_server,  total_festival_goers):
        self.env = env
        self.server = simpy.Resource(env, capacity=servers)
        self.waiting_times_per_server = []
        self.total_festival_goers = total_festival_goers

    def ticket_scan(self):
        scan_time = self.env.timeout(np.random.uniform(0,4)) 
        
        yield scan_time
        
        

    def get_waiting_times_per_server(self):
        return np.array(self.waiting_times_per_server)

def go_to_festival(env, festival):

    arrival_time = env.now # Record the current simulation time

    with festival.server.request() as request:
        yield request
        yield env.process(festival.ticket_scan())
    
    festival_goer_waiting_time = env.now - arrival_time
    festival.waiting_times_per_server.append(festival_goer_waiting_time)
    return festival_goer_waiting_time

def run_festival(env, servers, total_festival_goers, festival):
   
    festival_goer = 0
    while festival_goer <= total_festival_goers:
        interarrival_time = 0.20

        group_size = np.random.randint(1,7)
        

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


        


