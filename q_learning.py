import numpy as np
import random

from switch_migration import calculate_controller_cluster_load, calculate_controller_cluster_load_ratio, calculate_controller_load_capacity, calculate_controller_mean_load_ratio, calculate_discrete_coefficient

# Supporting functions for Q-Learning


def egreedy_policy(state, epsilon, Q_matrix):
    '''
    This function returns the action that should be taken
    Given the state and epsilon
    '''
    if np.random.random() < epsilon:
        return np.random.choice(3)
    else:
        return np.random.choice(np.flatnonzero(Q_matrix[state] == np.max(Q_matrix[state])))


def update_epsilon(epsilon, epsilon_dec, epsilon_min):
    '''
    This function updates the epsilon value needed for the EGreedy approach
    '''
    if epsilon > epsilon_min:
        epsilon -= epsilon_dec
    else:
        epsilon = epsilon_min

    return epsilon


def q_learning(controller_sets_Q, controllers_Q, k, switch_count, load_array):
    '''
    When the migration efficiency can't be optimized by using the greedy strategy only
    to make decisions, exploring non-greedy situations at the case of probability in each
    decision and combining ε-greedy and decision-making to select migration triples, so as
    to obtain global optimal switch migration decision based on reinforcement learning
    '''

    # Initialising a few things for Q-Learning

    # Q_matrix is initialised in a way that each state is represented as a tuple and mapped to 3 actions
    # namely do nothing, add a switch or remove a switch.

    Q_matrix = {tuple([0]*k): [0]*3}

    # Setting the values for
    # gamma - discount factor
    # alpha - learning rate

    gamma = 0.99
    def alpha(n): return 1/(pow(n+1, 0.6))
    def b(n): return 1/(n+1)

    # Handling epsilon values for epgreedy
    epsilon = 0.7
    epsilon_dec = 0.0025
    epsilon_min = 0.05

    # Setting the initial state to all zeros
    state = tuple([0]*k)

    # Store a list of states to plot later
    states_list = []

    # List to store discounted rewards
    disc_reward_list = []
    l_n_list = []
    cum_disc_reward = 0

    # List to store number of switch exchanges
    num_switch_exchanges = 0
    num_switch_exchanges_list = []

    # Store Sn & Smax to generate the Lagrange multiplier
    S_max = 4000
    S_n = 0
    l_n = 1

    for n in range(0, len(load_array)):

        print('\n----------------Iteration {}-----------------\n'.format(n))

        # Use the previous state - (initial or transient) and reconfigure
        # it with the new data obtained. Change the state to inculcate the
        # new flows in the switches.

        old_load = [0]*switch_count if n == 0 else load_array[n-1]
        new_load = load_array[n]

        # Find the switch that has a different flow count this time (add or remove)

        for i in range(0, switch_count):
            if(old_load[i] != new_load[i]):
                diff_switch = i
                break

        # Modify the state after obtaining the appropriate controller cluster and
        # change the number of flows - increase or decrease based on event

        for i in range(0, len(controller_sets_Q)):
            if diff_switch in controller_sets_Q[i]:
                state = list(state)
                state[i] += new_load[diff_switch] - old_load[diff_switch]
                state = tuple(state)
                break

        states_list.append(state)

        # ------------------------------ Start Q-Learning ------------------------------

        # Randomly choose a controller to transfer switch from/to
        C_i = np.random.choice(k)

        # Add the state to the Q-matrix dict if not already present
        if state in Q_matrix:
            print(
                "Already present state {} with Q-value {}".format(state, Q_matrix[state]))
        else:
            Q_matrix[state] = [0]*3

        # Find the action corresponding to the state based on an E-Greedy approach
        action = egreedy_policy(state, epsilon, Q_matrix)

        # Safegaurd against impossible actions -- check/change
        if(state[C_i] == 0 and action == 2):
            action = 0

        print("Action = " + ["do nothing", "add 1 switch to {}".format(
            controllers_Q[C_i]), "remove 1 switch from {}".format(controllers_Q[C_i])][action])

        cost = 0

        # Find the next state and the reward corresponding to the action
        if action == 0:
            # Do nothing
            next_state = state
            num_switch_exchanges_list.append(num_switch_exchanges)

        elif action == 1:
            # Add 1 switch to Ci
            # In this case choose the most overloaded switch
            # The switch should not be in the same controller as destination

            S_n += pow(alpha(n), n)
            num_switch_exchanges += 1
            num_switch_exchanges_list.append(num_switch_exchanges)

            controller_dest = C_i
            controller_src = controller_dest
            switch = 0
            temp_load = -np.inf
            for i in range(0, switch_count):
                if(load_array[n][i] >= temp_load and (i not in controller_sets_Q[controller_dest])):
                    switch = i
                    temp_load = load_array[n][i]

            for i in range(0, k):
                if(switch in controller_sets_Q[i]):
                    controller_src = i

            no_of_flows = load_array[n][switch]
            cost = no_of_flows

            # Transfer the switch between controllers
            controller_sets_Q[controller_src].remove(switch)
            controller_sets_Q[controller_dest].append(switch)

            print("Source controller = {}, Destination controller = {}, Switch selected = {}, Number of flows on switch = {}".format(
                controller_src, controller_dest, switch, no_of_flows))

            next_state = state
            next_state = list(next_state)
            next_state[controller_src] -= no_of_flows
            next_state[controller_dest] += no_of_flows
            next_state = tuple(next_state)

        else:
            # Remove 1 switch from Ci
            # In this case choose the most underloaded controller
            # Transfer a random switch from the source controller to this destination controller

            S_n += pow(alpha(n), n)
            num_switch_exchanges += 1
            num_switch_exchanges_list.append(num_switch_exchanges)

            controller_src = C_i
            controller_dest = controller_src
            temp_flows = np.inf
            for i in range(0, k):
                if(state[i] <= temp_flows and i != controller_src):
                    controller_dest = i
                    temp_flows = state[i]

            switch = random.choice(controller_sets_Q[controller_src])
            no_of_flows = load_array[n][switch]
            cost = no_of_flows

            # Transfer the switch between controllers
            controller_sets_Q[controller_src].remove(switch)
            controller_sets_Q[controller_dest].append(switch)

            print("Source controller = {}, Destination controller = {}, Switch selected = {}, Number of flows on switch = {}".format(
                controller_src, controller_dest, switch, no_of_flows))

            next_state = state
            next_state = list(next_state)
            next_state[controller_src] -= no_of_flows
            next_state[controller_dest] += no_of_flows
            next_state = tuple(next_state)

        print("Current State = {}".format(state))
        print("Next State = {}".format(next_state))

        # Check if the Q_matrix dict has a tuple or not. If no, create an entry
        if next_state in Q_matrix:
            print(
                "Already present next state {} and Q-value {}".format(next_state, Q_matrix[next_state]))
        else:
            Q_matrix[next_state] = [0]*3

        # Reward calculation
        # The reward in this case is given as -
        # Reward = -D'ij; where D'ij is the new discrete coefficient of the system

        controller_cluster_load = {}
        for i in range(0, k):
            controller_cluster_load[controllers_Q[i]] = next_state[i]
        controller_cluster_load_ratio = calculate_controller_cluster_load_ratio(
            controller_cluster_load, load_array)
        Dij_new = calculate_discrete_coefficient(controller_cluster_load_ratio)

        reward = -Dij_new
        l_n += b(n)*(S_n - S_max)

        if(l_n < 0):
            l_n = 0
        if(l_n > 10000):
            l_n = 10000

        discounted_reward = reward*pow(gamma, n)
        cum_disc_reward += discounted_reward

        print(cum_disc_reward)

        disc_reward_list.append(cum_disc_reward)
        l_n_list.append(l_n)

        Q_matrix[state][action] = (1-alpha(n))*Q_matrix[state][action] + \
            alpha(n)*((reward - l_n*cost) + gamma*max(Q_matrix[next_state]))

        # Update the state to the new state
        state = next_state

        # Update epsilon for the next iteration
        epsilon = update_epsilon(epsilon, epsilon_dec, epsilon_min)

    return states_list, disc_reward_list, num_switch_exchanges_list
