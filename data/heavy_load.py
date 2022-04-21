'''
This file contains code where the load on switches is more.
This means that the arrival rate on the switches will be much higher than the service rate.

In this case we consider the following rate of values to generate the data - 
λ = random numbers in range(50, 100)
μ = random numbers in range(1, 5)
'''

import pandas as pd
import numpy as np


switch_count = 34

# Randomly generating lambda and mu values (same for all) for 34 switches
arrival_lambda_list = list(np.random.randint(low=50, high=100, size=switch_count))
service_mu_list = [np.random.randint(low=1, high=5)]*switch_count

print("Arrival Lambda = {}".format(arrival_lambda_list))
print("Service Mu = {}".format(service_mu_list))

# Generate the data
data = []
event_count = 100

for i in range(0, switch_count):
    arrival_times = np.random.exponential(1/arrival_lambda_list[i], event_count)
    arrival_timestamps = np.cumsum(arrival_times)
    service_times = np.random.exponential(1/service_mu_list[i], event_count)
    departure_timestamps = arrival_timestamps + service_times

    for j in range(0, event_count):
        data.append((arrival_timestamps[j], i, 1))
        data.append((departure_timestamps[j], i, -1))

# Sorts the data as per the first element (timestamps in our case)
data.sort()
table_data = []

temp_list = [0] * switch_count

for i in range(0,len(data)):
    timestamp = data[i][0]
    switch_number = data[i][1]
    update = data[i][2]

    temp_list[switch_number]+=update
    table_data.append([item for item in temp_list])
    
final_data = pd.DataFrame(table_data)
print(final_data)
final_csv_data = final_data.to_csv('data.csv')  