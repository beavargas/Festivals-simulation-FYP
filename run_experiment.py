
import json
from main import main
#import case_study_actual_main
import numpy as np
import pandas as pd
import random

def run_experiment(num_runs):    
    mean_waiting_times = []
    std_waiting_times = []
    simulation_sample_means = []
    simulation_sample_std = []
    
    
    for i in range(num_runs):
        print(i)
        #case_study_actual_main.main()
        main()
        simulation_data_df = pd.read_json('MMA_5000.json')
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
    num_rows, num_cols = df_mean_waiting_times.shape

    #print("Number of rows:", num_rows)
    #print("Number of columns:", num_cols)


    df_std_waiting_times = pd.DataFrame(std_waiting_times).T
    #print(df_std_waiting_times)

    a = df_mean_waiting_times.to_json('RESULTS_MMA_5000.json')
 


            
        
            
if __name__ == '__main__':
    run_experiment(100)
    


