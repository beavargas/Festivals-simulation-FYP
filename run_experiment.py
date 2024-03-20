import json
import main
import numpy as np
import pandas as pd

def run_experiment(num_runs):
    all_simulation_data = []
    all_mean_waiting_times = []
    all_std_waiting_time = []

    for i in range(num_runs):
        main()
        with open(f'simulation_data.json', 'r') as file:
            simulation_data = json.load(file)
            simulation_data_df = pd.DataFrame(simulation_data)
            for row in simulation_data_df:
                mean_waiting_time = np.mean(simulation_data_df, axis=1)
                all_mean_waiting_times.extend(mean_waiting_time)
                std_waiting_time = np.std(simulation_data_df, axis=1)
                all_std_waiting_time.extend(std_waiting_time)
            all_simulation_data.append(simulation_data_df)
    


