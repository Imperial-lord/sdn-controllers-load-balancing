'''
This file contains code where the load on switches is skewed.
This means that the arrival rate on the switches will be much higher than the arrival rate on other switches.
For our purpose let's put a very high arrival rate on randomly choosen 2 switches.

In this case we consider the following rate of values to generate the data - 
λ = high: random numbers in range(50, 100); low: random numbers in range(5, 10)
μ = a random number in range(25, 50)
'''

import pandas as pd
import numpy as np


def gen_lambda_mu_lists(switch_count):
    # Randomly generating lambda and mu values (same for all) for 34 switches
    arrival_lambda_list = list(np.random.randint(
        low=5, high=10, size=switch_count))
    arrival_lambda_list[0] = np.random.randint(low=50, high=100)
    arrival_lambda_list[1] = np.random.randint(low=50, high=100)
    service_mu_list = [np.random.randint(low=1, high=5)]*switch_count

    return arrival_lambda_list, service_mu_list


def gen_data_csv(table_data):
    final_data = pd.DataFrame(table_data)
    final_csv_data = final_data.to_csv('csv/data_skewed.csv')
    return final_data
