import sys
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
from data import heavy_load, light_load, skewed_load, table
from graph_building import build_graph
from q_learning import q_learning
from switch_migration import calculate_controller_cluster_load_ratio, calculate_discrete_coefficient
from graph_helpers import calculate_Dij_from_states, show_all_plots

# ----------------------------------------------------------------------------------------------------------------

# Initialise the number of controllers and the gml files to use.
k = int(input("Enter the number of controllers to allocate: "))
graph = nx.read_gml('gml/Arnes.gml', label='id')
switch_count = len(graph.nodes)

# ----------------------------------------------------------------------------------------------------------------
# log_file_name = "logs/Log_message{}.log".format(datetime.now().time())
# log_file = open(log_file_name, "w")
# print("Check the system logs at - " + log_file_name + "\n")
# sys.stdout = log_file

# ----------------------------------------------------------------------------------------------------------------

# Create CSV files for different load scenarios
# (i) Heavy Load
print('------------------- Heavy Load -------------------')
arrival_lambda_list, service_mu_list = heavy_load.gen_lambda_mu_lists(switch_count)
table_data = table.generate_table(arrival_lambda_list, service_mu_list, switch_count)
final_data_heavy = heavy_load.gen_data_csv(table_data)

# (ii) Light Load
print('------------------- Light Load -------------------')
arrival_lambda_list, service_mu_list = light_load.gen_lambda_mu_lists(switch_count)
table_data = table.generate_table(arrival_lambda_list, service_mu_list, switch_count)
final_data_light = light_load.gen_data_csv(table_data)

# (iii) Skewed Load
print('------------------- Skewed Load -------------------')
arrival_lambda_list, service_mu_list = skewed_load.gen_lambda_mu_lists(switch_count)
table_data = table.generate_table(arrival_lambda_list, service_mu_list, switch_count)
final_data_skewed = skewed_load.gen_data_csv(table_data)

# ----------------------------------------------------------------------------------------------------------------
final_data = final_data_heavy
controllers_Q, controller_sets_Q, controller_sets_G, load_array = build_graph(k, graph, final_data)
states_list, disc_reward_list = q_learning(controller_sets_Q, controllers_Q, k, switch_count, load_array)
d_coeff_list = calculate_Dij_from_states(k, states_list, controllers_Q, load_array)

show_all_plots(d_coeff_list, disc_reward_list, 'Load Heavy')

# ----------------------------------------------------------------------------------------------------------------
final_data = final_data_light
controllers_Q, controller_sets_Q, controller_sets_G, load_array = build_graph(k, graph, final_data)
states_list, disc_reward_list = q_learning(controller_sets_Q, controllers_Q, k, switch_count, load_array)
d_coeff_list = calculate_Dij_from_states(k, states_list, controllers_Q, load_array)

show_all_plots(d_coeff_list, disc_reward_list, 'Load Light')

# ----------------------------------------------------------------------------------------------------------------
final_data = final_data_skewed
controllers_Q, controller_sets_Q, controller_sets_G, load_array = build_graph(k, graph, final_data)
states_list, disc_reward_list = q_learning(controller_sets_Q, controllers_Q, k, switch_count, load_array)
d_coeff_list = calculate_Dij_from_states(k, states_list, controllers_Q, load_array)

show_all_plots(d_coeff_list, disc_reward_list, 'Load Skewed')

# ----------------------------------------------------------------------------------------------------------------
# sys.stdout = sys.__stdout__
