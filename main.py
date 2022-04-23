import networkx as nx
import matplotlib.pyplot as plt
from data import heavy_load, light_load, skewed_load, table
from graph_building import build_graph
from q_learning import q_learning
from switch_migration import calculate_controller_cluster_load_ratio, calculate_discrete_coefficient

# ----------------------------------------------------------------------------------------------------------------

# Initialise the number of controllers and the gml files to use.
k = int(input("Enter the number of controllers to allocate: "))
graph = nx.read_gml('gml/Arnes.gml', label='id')
switch_count = len(graph.nodes)

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

d_coeff_list = []
for n in range(0, len(states_list)):
    state = states_list[n]

    controller_cluster_load = {}
    for i in range(0, k):
        controller_cluster_load[controllers_Q[i]] = state[i]

    controller_cluster_load_ratio = calculate_controller_cluster_load_ratio(controller_cluster_load, load_array)
    Dij = calculate_discrete_coefficient(controller_cluster_load_ratio)

    d_coeff_list.append(Dij)


time = []
plot_d_coeff = []
plot_disc_reward = []

for i in range(0, 6000, 1):
    time.append(i)
    plot_d_coeff.append(d_coeff_list[i])
    plot_disc_reward.append(disc_reward_list[i])

# Discrete coefficient vs iterations
plt.xlabel('Iterations')
plt.ylabel('Discrete Coefficient')
plt.plot(time, plot_d_coeff)
plt.show()

# Discounted reward vs iterations
plt.xlabel('Iterations')
plt.ylabel('Discounted Reward')
plt.plot(time, plot_disc_reward)
plt.show()
