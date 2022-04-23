from math import sqrt

# Switch Migration Design
'''
LCi: the load of the controller Ci
CCi: the load capacity of the controller Ci
RCi: the load ratio of the controller Ci
LSk: the packet-in message sending rate of the switch Sk
R: mean load ratio of all controllers
D: load ratio deviation coefficient between two controllers
E: migrate switch efficiency between controllers
HSk: number of hops between the switch and the controller
'''

# A. Load Balancing

'''
Controllers' Load
Populating `controller_cluster_load` array
Eg - {c1:36363663, c2:3234325, c3:32523525, c4:3523535, c5:3542646}
Load for a controller is the sum of load on it + all it's switches
'''


def calculate_controller_cluster_load(time_step, controller_sets, load_array):
    controller_cluster_load = {}
    index = 0
    for controller_set in controller_sets:
        total_load = 0
        for switch in controller_set:
            total_load += load_array[time_step][switch]

        controller_cluster_load[controllers[index]] = total_load
        index += 1
    return controller_cluster_load

# TEST ABOVE FUNCTION --------------------------------------
# controller_cluster_load = calculate_controller_cluster_load(0, controller_sets)
# print(controller_cluster_load)
# -----------------------------------------------------------


'''
Controllers' Load Capacity
For finding this, we assume the extreme most case, i.e, number of controllers = 1
For this, the load capacity at a given time step = sum of all load on all switches at that time step.
The `load capacity of all controllers` = max of the load capacity over all time steps, and assumed to be uniform for all controllers.
'''


def calculate_controller_load_capacity(load_array):
    load_capacity_at_ts = []
    for time_step in range(0, len(load_array)):
        values = load_array[time_step].values()
        total = sum(values)
        load_capacity_at_ts.append(total)
    return max(load_capacity_at_ts)


'''
Controllers' Load Ratio
The `load ratio for a controller` is the ratio of it's load to load capacity
'''


def calculate_controller_cluster_load_ratio(controller_cluster_load, load_array):
    CONTROLLERS_LOAD_CAPACITY = calculate_controller_load_capacity(load_array)
    controller_cluster_load_ratio = {}
    for controller in controller_cluster_load:
        controller_cluster_load_ratio[controller] = controller_cluster_load[controller] / \
            CONTROLLERS_LOAD_CAPACITY
    return controller_cluster_load_ratio

# TEST ABOVE FUNCTION ---------------------------------------
# controller_cluster_load_ratio = calculate_controller_cluster_load_ratio(controller_cluster_load)
# print(controller_cluster_load_ratio)
# -----------------------------------------------------------


'''
Controllers' Mean Load Ratio
The mean load ratio of controllers is given as mean of load ratios of all controllers
'''


def calculate_controller_mean_load_ratio(controller_cluster_load_ratio):
    values = controller_cluster_load_ratio.values()
    no_of_controllers = len(values)
    controller_mean_load_ratio = sum(values)/no_of_controllers
    return controller_mean_load_ratio

# TEST ABOVE FUNCTION ---------------------------------------
# controller_mean_load_ratio = calculate_controller_mean_load_ratio(controller_cluster_load_ratio)
# print(controller_mean_load_ratio)
# -----------------------------------------------------------


'''
Discrete Coefficient 
The discrete coefficient is used to describe the degree of discrete of 
the controller's load ratio and the mean load ratio between controllers
'''


def calculate_discrete_coefficient(controller_cluster_load_ratio):
    controller_mean_load_ratio = calculate_controller_mean_load_ratio(
        controller_cluster_load_ratio)
    D_num = 0
    D_denom = controller_mean_load_ratio
    no_of_controllers = len(controller_cluster_load_ratio.values())

    for controller in controller_cluster_load_ratio:
        load_ratio = controller_cluster_load_ratio[controller]
        D_num += ((load_ratio - controller_mean_load_ratio)**2) / \
            no_of_controllers

    D_num = sqrt(D_num)
    if(D_denom == 0):
        return 0

    D = D_num/D_denom
    return D

# TEST ABOVE FUNCTION ---------------------------------------
# discrete_coefficient = calculate_discrete_coefficient(controller_cluster_load_ratio)
# print(discrete_coefficient)
# -----------------------------------------------------------
