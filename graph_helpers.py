import matplotlib.pyplot as plt
import os
from switch_migration import calculate_controller_cluster_load_ratio, calculate_discrete_coefficient


def calculate_Dij_from_states(k, states_list, controllers_Q, load_array):
    d_coeff_list = []
    for n in range(0, len(states_list)):
        state = states_list[n]

        controller_cluster_load = {}
        for i in range(0, k):
            controller_cluster_load[controllers_Q[i]] = state[i]

        controller_cluster_load_ratio = calculate_controller_cluster_load_ratio(controller_cluster_load, load_array)
        Dij = calculate_discrete_coefficient(controller_cluster_load_ratio)

        d_coeff_list.append(Dij)

    return d_coeff_list


def show_all_plots(d_coeff_list, disc_reward_list, plot_type):
    plot_directory = 'plots/{}/'.format(plot_type)
    if not os.path.exists(plot_directory):
        os.makedirs(plot_directory)

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
    plt.savefig('plots/{}/discrete_coeff.png'.format(plot_type))
    plt.clf()

    # Discounted reward vs iterations
    plt.xlabel('Iterations')
    plt.ylabel('Discounted Reward')
    plt.plot(time, plot_disc_reward)
    plt.savefig('plots/{}/discounted_reward.png'.format(plot_type))
    plt.clf()
