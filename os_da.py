# Import required libraries
import itertools  # For generating combinations of VMs (coalitions)
import math       # For factorial calculations in Shapley value
import matplotlib.pyplot as plt  # For visualization of results

class CloudResourceGame:
    """Main class implementing cooperative game theory for resource allocation"""
    
    def __init__(self, vms, total_resources):
        """
        Initialize the resource allocation game
        
        Args:
            vms: List of VM objects representing virtual machines
            total_resources: Total available resources in the cloud system
        """
        self.vms = vms          # List of VM objects
        self.total_resources = total_resources  # Total available resources
        self.n = len(vms)       # Number of VMs in the system
    
    def characteristic_function(self, coalition):
        """
        Calculate the value of a coalition (group of VMs)
        
        Args:
            coalition: List of VMs forming a coalition
            
        Returns:
            Minimum of either the coalition's total demand or total available resources
        """
        total_demand = sum(vm.demand for vm in coalition)
        return min(total_demand, self.total_resources)
    
    def calculate_shapley_values(self):
        """Calculate Shapley values for all VMs using combinatorial method"""
        # Initialize Shapley values to 0 for each VM
        shapley_values = [0.0] * self.n
        
        # Consider all possible coalition sizes from 1 to n VMs
        for coalition_size in range(1, self.n + 1):
            # Generate all possible combinations of VMs of current size
            for coalition_indices in itertools.combinations(range(self.n), coalition_size):
                # Get the actual VM objects for this coalition
                coalition = [self.vms[i] for i in coalition_indices]
                # Calculate value of this coalition
                value = self.characteristic_function(coalition)
                
                # For each VM in the coalition, calculate its marginal contribution
                for vm_idx in coalition_indices:
                    # Create coalition without current VM
                    sub_coalition = [self.vms[i] for i in coalition_indices if i != vm_idx]
                    # Calculate value of coalition without this VM
                    value_without = self.characteristic_function(sub_coalition)
                    # Marginal contribution = value with VM - value without VM
                    marginal_contribution = value - value_without
                    
                    # Calculate weight for this coalition (probability of forming this coalition)
                    weight = (math.factorial(len(sub_coalition)) * \
                             math.factorial(self.n - len(sub_coalition) - 1)) / \
                             math.factorial(self.n)
                    
                    # Add weighted contribution to VM's Shapley value
                    shapley_values[vm_idx] += marginal_contribution * weight
        
        return shapley_values
    
    def calculate_proportional_allocation(self):
        """Calculate traditional proportional resource allocation"""
        total_demand = sum(vm.demand for vm in self.vms)
        
        # If total demand <= available resources, give each VM its full demand
        if total_demand <= self.total_resources:
            return [vm.demand for vm in self.vms]
        # Otherwise allocate proportionally to each VM's demand
        else:
            return [self.total_resources * (vm.demand / total_demand) for vm in self.vms]
    
    def allocate_resources(self):
        """Allocate resources using Shapley values"""
        # Get Shapley values for all VMs
        shapley_values = self.calculate_shapley_values()
        total_shapley = sum(shapley_values)
        
        # Handle edge case where total Shapley value is 0 or negative
        if total_shapley <= 0:
            return [0] * self.n
        
        # Calculate actual allocations based on Shapley values
        allocations = []
        for i in range(self.n):
            # Allocate proportionally to Shapley value
            alloc = self.total_resources * (shapley_values[i] / total_shapley)
            # Ensure VM doesn't get more than its demand
            allocations.append(min(alloc, self.vms[i].demand))
        
        return allocations

class VM:
    """Class representing a Virtual Machine"""
    
    def __init__(self, id, demand):
        """
        Initialize a VM
        
        Args:
            id: Unique identifier for the VM
            demand: Resource demand of the VM
        """
        self.id = id        # VM identifier
        self.demand = demand  # Resource demand
    
    def __repr__(self):
        """String representation of VM for printing"""
        return f"VM(id={self.id}, demand={self.demand})"

def visualize_results(vms, shapley_alloc, prop_alloc, total_resources):
    """
    Visualize allocation results using matplotlib
    
    Args:
        vms: List of VM objects
        shapley_alloc: List of allocations using Shapley method
        prop_alloc: List of allocations using proportional method
        total_resources: Total available resources
    """
    # Create figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Prepare VM labels and demand values
    vm_ids = [f"VM {vm.id}" for vm in vms]
    demands = [vm.demand for vm in vms]
    
    # Plot 1: Shapley Allocation
    ax1.bar(vm_ids, demands, alpha=0.5, label='Demand')
    ax1.bar(vm_ids, shapley_alloc, alpha=0.8, label='Allocated (Shapley)')
    ax1.axhline(y=total_resources, color='r', linestyle='--', label='Total Resources')
    ax1.set_title('Shapley Value Allocation')
    ax1.set_ylabel('Resource Units')
    ax1.legend()
    
    # Plot 2: Proportional Allocation
    ax2.bar(vm_ids, demands, alpha=0.5, label='Demand')
    ax2.bar(vm_ids, prop_alloc, alpha=0.8, label='Allocated (Proportional)')
    ax2.axhline(y=total_resources, color='r', linestyle='--', label='Total Resources')
    ax2.set_title('Proportional Allocation')
    ax2.legend()
    
    # Create separate figure for satisfaction comparison
    fig2, ax3 = plt.subplots(figsize=(8, 5))
    
    # Calculate demand satisfaction ratios (allocation/demand, capped at 1)
    satisfaction_shapley = [min(a/d, 1) for a,d in zip(shapley_alloc, demands)]
    satisfaction_prop = [min(a/d, 1) for a,d in zip(prop_alloc, demands)]
    
    # Plot satisfaction comparison
    width = 0.35
    x = range(len(vm_ids))
    ax3.bar(x, satisfaction_shapley, width, label='Shapley')
    ax3.bar([p + width for p in x], satisfaction_prop, width, label='Proportional')
    ax3.set_xticks([p + width/2 for p in x])
    ax3.set_xticklabels(vm_ids)
    ax3.set_ylabel('Demand Satisfaction Ratio')
    ax3.set_title('Demand Satisfaction Comparison')
    ax3.legend()
    ax3.set_ylim(0, 1.1)  # Set y-axis limits from 0 to 110%
    
    # Adjust layout and display plots
    plt.tight_layout()
    plt.show()

def main():
    """Main function to run the resource allocation simulation"""
    # Create 3 VMs with different demands
    vms = [
        VM(1, 10),  # VM 1 demands 10 units
        VM(2, 20),  # VM 2 demands 20 units
        VM(3, 30),  # VM 3 demands 30 units
    ]
    total_resources = 45  # Total resources available
    
    # Initialize the resource allocation game
    game = CloudResourceGame(vms, total_resources)
    
    # Calculate allocations using both methods
    shapley_alloc = game.allocate_resources()
    prop_alloc = game.calculate_proportional_allocation()
    
    # Print results header
    print("Fair Resource Allocation using Cooperative Game Theory")
    print("="*60)
    print(f"Total server resources: {total_resources}")
    print("VM Demands:")
    for vm in vms:
        print(f"  {vm}")
    
    # Print allocation results
    print("\nAllocation Methods:")
    print("-"*60)
    # Format table header
    print("{:<15} {:<15} {:<15} {:<15}".format("VM", "Demand", "Shapley Alloc", "Proportional Alloc"))
    # Print each VM's allocation
    for i, vm in enumerate(vms):
        print("{:<15} {:<15} {:<15.2f} {:<15.2f}".format(
            f"VM {vm.id}", vm.demand, shapley_alloc[i], prop_alloc[i]))
    
    # Calculate and print satisfaction metrics
    print("\nMetrics:")
    print("-"*60)
    satisfaction_shapley = sum(min(a/vm.demand, 1) for a, vm in zip(shapley_alloc, vms)) / len(vms)
    satisfaction_prop = sum(min(a/vm.demand, 1) for a, vm in zip(prop_alloc, vms)) / len(vms)
    
    print(f"Average demand satisfaction (Shapley): {satisfaction_shapley:.2%}")
    print(f"Average demand satisfaction (Proportional): {satisfaction_prop:.2%}")
    
    # Visualize the results
    visualize_results(vms, shapley_alloc, prop_alloc, total_resources)

if __name__ == "__main__":
    # Run the main function if this script is executed directly
    main()