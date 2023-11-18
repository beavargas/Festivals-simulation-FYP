"""
Simple queuing model using simpy
This code return the average waiting time given an number of servers.
"""
import simpy
import statistics
import random

# List to collect the total amount of time each festival-goer spends from arrival to entering the festival
waiting_time = []

# Creating the 'Festival' enviroment as a class
class Festival(object):

    def __init__(self, env, servers):
        self.env = env
        self.server = simpy.Resource(env, capacity=10)

    def ticket_scan(self, festival_goer):
        yield self.env.timeout(random.randint(1,3)) # randomly assigns each ticket scan a time between 1 and 3
        
