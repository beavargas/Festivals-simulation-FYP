import json
from main import main
import numpy as np
import pandas as pd

def run_experiment(num_runs):
    mean_waiting_times = []
    std_waiting_times = []

    for i in range(num_runs):
        main()
        simulation_data_df = pd.read_json('simulation_data.json')
        #print(simulation_data_df)
        run_waiting_times_mean = []
        run_waiting_times_std = []
        for index, row in simulation_data_df.iterrows():
            mean_waiting_time = row.mean()
            std_waiting_time = row.std()
            run_waiting_times_mean.append(mean_waiting_time)
            run_waiting_times_std.append(std_waiting_time)
            #print(mean_waiting_time)
        mean_waiting_times.append(run_waiting_times_mean)
        std_waiting_times.append(run_waiting_times_std)
    
    df_mean_waiting_times = pd.DataFrame(mean_waiting_times).T
    print(df_mean_waiting_times)
    df_std_waiting_times = pd.DataFrame(std_waiting_times).T
    print(df_std_waiting_times)
             

        #with open(f'simulation_data.json', 'r') as file:
            #simulation_data = json.load(file)
            #print(simulation_data)
            #simulation_data_df = pd.DataFrame(simulation_data)
            #print(simulation_data_df.head())

            
    
   
    
    
            
            
            
if __name__ == '__main__':
    run_experiment(5)
    


