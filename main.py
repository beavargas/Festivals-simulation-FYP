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

# Creating a function for the agent to move through the enviroment
def go_to_festival(env, festival_goer, festival):

    """Function process:
    1) arrival_time = env.now: festival-goer arrives at the festival
    2) festival.server.request(): festival_goer generates a request to use a server
    3) yield request: festival_goer waits for a server to become available if all are currently in use
    4) yield env.process(): festival_goer uses an available server to get their ticket scanned by calling Festival.ticket_scan()
    5) using env now again, calculates the total waiting time of the festival goer and appends it to the waiting_time list
    """
    arrival_time = env.now 

    with festival.server.request() as request: # with statement automatically releases the festival goer once the process is complete
        yield request
        yield env.process(festival.ticket_scan(festival_goer))
    
    waiting_time.append(env.now - arrival_time) # calculates total waiting time of the festival-goer

# Creating a function that runs the festival and generates agents
def run_festival(env, servers):
    """ 
    This function generates 3 people waiting outside before the festival opens and begin moving them through the system.
    This function also creates a new person in an interval of 12 seconds abd move through the system at their own time.
    """

    festival = Festival(env, servers)

    for festival_goer in range(3): # 3 is the number of people already waiting in the queue when the festival opens
        env.process(go_to_festival(env, festival_goer, festival))
    
    while True:
        yield env.timeout(0,20) # wait before generating a new personn. 0.20 represents 12 seconds since 12 seconds divided by 60 seconds is 0.20.
        festival_goer += 1
        env.process(go_to_festival(env, festival_goer, festival))


# Creating a function that calculates the average waiting time
def average_waiting_time(waiting_time):
    """
    This function takes the waiting_time list as an argument and outputs the average wait time.
    It then converts it to minutes and seconds to make the output understandable for the user
    """
    average_wait = statistics.mean(waiting_time)

    minutes, frac_minutes = divmod(average_wait, 1)
    seconds = frac_minutes * 60
    return round(minutes), round(seconds)