
![sdn-controllers-load-balancing](https://user-images.githubusercontent.com/45942031/140089516-08ea50dd-ff1e-481d-b481-6222cd9ff01b.png)

## Abstract 
Software-Defined Network (SDN) is a networking paradigm featuring the separation of the control and data plane of the network devices. With refined centralized management and network programmability, SDN brings unique advantages as compared to traditional networks. To address the issue of scalability, the control plane is physically distributed although logically centralized. Since network traffic is both spatially and temporally dynamic, a multi-controller deployment in SDN needs a load balancing mechanism to deal with local overloads effectively.

The primary motivation behind this work is to build a framework that learns from the network traffic and aims to balance it quickly, reduce unnecessary migration overhead and get a faster response rate of the in-packet request. To this end, we use the load ratio deviation between the controllers and generate optimal migration triplets, consisting of the migrate-out and migration-in domains and a set of switches for migration. We utilize reinforcement learning under the constraint of the best efficiency and without migration conflicts to attain the global optimal controller load balancing with minimum cost. When compared with greedy and random selection approaches, our work provides better results.

## Repository Structure
* **Data** - This folder has all the data used in the python code: Arnes Topology data and Network Load data. Along with this, we have toy data used for testing the algorithms
* **Documents** - This folder contains all resources, PPTs, meeting notes and relevant information
* **Overleaf Work** - A zip file with the entire LaTeX project.

Other than these, we have _.ipynb_ files, which are connected to Google Colab projects. There are 3 projects - one complete implementation, one merged for averaged results, one toy implementation to compare with pen and paper work done separately. 
