# The generation of synthetic data

For this problem we are generating synthetic data for packets arrival and servicing from switches. We will later use actual data recorded from network traffic.

## Defining parameters

For this data generation we come across 2 terms:
- Arrival Rate (λ) = We are assuming arrivals can be monitored using a Poisson process with parameter λ
- Service Rate (μ) = We are assuming that the packet service times cab be monitored using a Exponential process with parameter μ 

## How is data generated?

For each switch we assume that the arrival is a poisson process with parameter λ<sub>i</sub>. However the service rate parameter μ is taken as for all switches.

Basically since the arrivals occur as a Poi(λ) process, the inter-arrival times are exponentially distributed with mean λ. For each switch we compute the time of arrivals and add the service time to it to note the timestamp when the packets depart. 

**It is interesting to observe that at each timestamp only one arrival or departure can occur.** This means we can save tuples in the following format -

```python
tuple(timestamp, switch, flow +/-)
```

Using these tuples we finally build our table of data. This is how our table will look roughly.

 Timestamp    | Switch 01 | Switch 02 | Switch 03 | ... | Switch 34 |
| :---        | :---      | :---      | :---      | :---| :---      |         
| 0.2546      | 0         | 0         | 0         | ... | 1         | 
| 0.3947      | 1         | 0         | 0         | ... | 0         | 
| 0.4247      | 2         | 0         | 0         | ... | 0         | 
| 0.4547      | 3         | 0         | 0         | ... | 0         | 
...
| 0.9649      | 0         | 0         | 1         | ... | 0         | 
| 0.9947      | 0         | 0         | 0         | ... | 0         | 