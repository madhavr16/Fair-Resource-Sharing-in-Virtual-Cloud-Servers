# Fair-Resource-Sharing-in-Virtual-Cloud-Servers
This project implements a fair resource allocation system for cloud environments using cooperative game theory (Shapley value). It ensures equitable distribution of limited resources (CPU, memory, etc.) among virtual machines (VMs) with varying demands, preventing large VMs from monopolizing resources while protecting smaller ones from starvation.

## Key Features
✅ Shapley Value Allocation – Fairly distributes resources based on each VM's marginal contribution across all possible coalitions.
✅ Proportional Allocation – Traditional demand-based allocation for comparison.
✅ Visualization – Matplotlib plots comparing fairness and efficiency.
✅ Mathematically Rigorous – Implements exact Shapley computation for small systems.

## Example Results
![image](https://github.com/user-attachments/assets/8fefa205-f09e-4900-aa65-e1f837ff2eaa)

## How It Works
Input: List of VMs (id, demand) and total resources.

Shapley Calculation:
Computes all possible VM coalitions.
Evaluates each VM’s marginal contribution.
Weights contributions by coalition probability

Proportional Allocation: Simple demand-based division.

Visualization: Compares allocations and satisfaction ratios.

## Why Shapley
✔ Fairness: No VM dominates; small VMs guaranteed minimal resources.
✔ Strategy-proof: VMs can’t gain by misreporting demands.
✔ Dynamic Adaptation: Adjusts allocations when demands/resources change.

### License
MIT License – Free for academic and commercial use.

