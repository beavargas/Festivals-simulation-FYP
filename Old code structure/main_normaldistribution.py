"""
Queuing model using simpy
Normal distribution for server times and interarrival times
This code return the average waiting time given an number of servers.
"""
import simpy
import statistics
import random
import matplotlib.pyplot as plt
import numpy as np
 
# List to collect the total amount of time each festival-goer spends from arrival to entering the festival
waiting_time = []

# Creating the 'Festival' enviroment as a class
class Festival(object):

    def __init__(self, env, servers, mean_scan_time, std_scan_time):
        self.env = env
        self.server = simpy.Resource(env, capacity=servers)
        self.mean_scan_time = mean_scan_time
        self.std_scan_time = std_scan_time

    def ticket_scan(self, festival_goer):
        scanning_time = np.random.normal(self.mean_scan_time, self.std_scan_time)
        scanning_time = np.clip(scanning_time, 0.1, 5)
        yield self.env.timeout(scanning_time) 

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
        yield request # puts the festival-goer in a waiting state until a server becomes available.
        yield env.process(festival.ticket_scan(festival_goer)) #  yields the process of getting the ticket scanned by calling the ticket_scan method of the Festival class.
    
    waiting_time.append(env.now - arrival_time) # calculates total waiting time of the festival-goer

# Creating a function that runs the festival and generates agents
def run_festival(env, servers, mean_interarrival, std_interarrival):
    """ 
    This function generates 3 people waiting outside before the festival opens and begin moving them through the system.
    This function also creates a new person in an interval of 12 seconds abd move through the system at their own time.
    """

    festival = Festival(env, servers, mean_scan_time=1,std_scan_time=0.8)

    for festival_goer in range(3): # 3 is the number of people already waiting in the queue when the festival opens
        env.process(go_to_festival(env, festival_goer, festival))  
    
    while True:
        interarrival_time = max(0, random.normalvariate(mean_interarrival, std_interarrival))
        yield env.timeout(interarrival_time) 
        festival_goer += 1
        env.process(go_to_festival(env, festival_goer, festival))
        #print(festival_goer)
    
    
    


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

def main():
    # set up
    with open("params.txt", "r") as file:
        server_values = [int(line.strip()) for line in file]

    average_wait_times = []
    std_devs = []

    for servers in server_values:
        random.seed(42)

        # run simulation
        env = simpy.Environment()
        env.process(run_festival(env, servers, mean_interarrival=0.5, std_interarrival=0.05))
        env.run(until=90)
       

        # view output
        mins, secs = average_waiting_time(waiting_time)
        #print(f"The average wait time is {mins} minutes and {secs} seconds.")
        std_dev = statistics.stdev(waiting_time)

        average_wait_times.append((mins, secs))
        std_devs.append(std_dev)
    
    
    mins, secs = zip(*average_wait_times)
    # Plotting
    #plt.errorbar(secs, mins, yerr=std_devs, fmt='o', capsize=3)
    #plt.plot(server_values, [mins for mins, _ in average_wait_times], marker='o')
    #plt.scatter(server_values, [mins for mins, _ in average_wait_times], marker='o', label='Average Wait Time')
    print(len(waiting_time))
    print(len(server_values))

    plt.scatter(server_values, waiting_time)
    plt.xlabel('Number of Servers')
    plt.ylabel('Average Wait Time (minutes)')
    plt.title('Average Wait Time vs. Number of Servers')
    plt.grid(True)
    plt.show()
    
  

if __name__ == '__main__':
    main()

    