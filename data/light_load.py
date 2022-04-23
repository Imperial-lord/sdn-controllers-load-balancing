'''
This file contains code where the load on switches is less.
This means that the arrival rate on the switches will be much smaller than the service rate.

In this case we consider the following rate of values to generate the data - 
λ = random numbers in range(1, 5)
μ = a random number in range(50, 100)
'''

import pandas as pd
import numpy as np


def gen_lambda_mu_lists(switch_count):
    # Randomly generating lambda and mu values (same for all) for 34 switches
    arrival_lambda_list = list(np.random.randint(
        low=1, high=5, size=switch_count))
    service_mu_list = [np.random.randint(low=50, high=100)]*switch_count

    return arrival_lambda_list, service_mu_list


def gen_data_csv(table_data):
    final_data = pd.DataFrame(table_data)
    final_csv_data = final_data.to_csv('csv/data_light.csv')
    return final_data
