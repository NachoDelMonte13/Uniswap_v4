import numpy as np
import matplotlib.pyplot as plt

# Simulation of Uniswap V4 hooks impact (reward and penalty system for fees)

# Initial parameters
np.random.seed(42)
num_traders = 10000  # Number of simulated traders
swap_sizes = np.random.exponential(50, num_traders)  # Swap sizes (exponential distribution)
base_fee = 0.003  # Base pool fee (0.3%)
base_gas_cost = 0.01  # Average gas cost for a transaction

# Hooks: Reward and penalty system for fees
def dynamic_fee(swap_size, volatility):
    """Calculates the dynamic fee based on swap size and market volatility."""
    if swap_size < 10:
        return base_fee * 2  # Penalty for small swaps
    elif volatility > 0.05:
        return base_fee * 0.5  # Reward for traders in high volatility
    else:
        return base_fee  # Base fee

# Simulate market volatility
market_volatility = np.random.uniform(0.01, 0.1, num_traders)

# Apply dynamic fees
fees = [dynamic_fee(swap_sizes[i], market_volatility[i]) for i in range(num_traders)]

def total_cost(swap_size, fee, gas_cost):
    """Calculates the total cost of a transaction: pool fee + gas cost."""
    return swap_size * fee + gas_cost

# Calculate total costs with and without hooks
base_total_costs = [total_cost(swap_sizes[i], base_fee, base_gas_cost) for i in range(num_traders)]
hook_total_costs = [total_cost(swap_sizes[i], fees[i], base_gas_cost) for i in range(num_traders)]

# Compare total transaction volumes
base_volumes = swap_sizes * base_fee
hook_volumes = swap_sizes * fees

# Visualize the impact of hooks on fees and total costs
plt.figure(figsize=(12, 6))
plt.hist(base_total_costs, bins=50, alpha=0.7, label="Total Cost - Base Fee")
plt.hist(hook_total_costs, bins=50, alpha=0.7, label="Total Cost - With Hooks")
plt.title("Impact of Hooks on Total Transaction Costs - Uniswap V4")
plt.xlabel("Total Transaction Cost")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# Final results
print("Results Summary:")
print(f"Average total cost (base): {np.mean(base_total_costs):.4f}")
print(f"Average total cost (with hooks): {np.mean(hook_total_costs):.4f}")

# ------------------------
# Demand elasticity: Impact of fees on transaction volume
# ------------------------

def demand_elasticity(fee_multiplier, swap_sizes, gas_cost, elasticity=-0.5):
    """Simple elasticity of demand model: 
    Volume reduction based on increased fees and gas costs."""
    adjusted_swaps = swap_sizes * (fee_multiplier ** elasticity)
    adjusted_total_costs = adjusted_swaps * base_fee * fee_multiplier + gas_cost
    return adjusted_total_costs

# Elasticity scenarios
fee_multipliers = np.linspace(0.5, 2, 5)  # From 50% less to 2x higher fees
elasticity_results = [demand_elasticity(fm, swap_sizes, base_gas_cost) for fm in fee_multipliers]

# Visualize elasticity impact
plt.figure(figsize=(10, 6))
for i, costs in enumerate(elasticity_results):
    plt.hist(costs, bins=50, alpha=0.5, label=f"Fee x{fee_multipliers[i]:.1f}")
plt.title("Demand Elasticity - Impact of Fees and Gas on Total Costs")
plt.xlabel("Adjusted Total Cost")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# Compare total adjusted costs by elasticity
print("Impact of Elasticity on Total Costs:")
for i, fm in enumerate(fee_multipliers):
    print(f"Fee x{fm:.1f}: Average total cost = {np.mean(elasticity_results[i]):.4f}")

# ------------------------
# Liquidity migration: Traders leaving the network due to high fees
# ------------------------

def liquidity_migration(fee_multiplier, gas_cost, threshold=1.5):
    """Simulates liquidity migration when fees and total costs exceed a threshold."""
    migrated = np.where(fee_multiplier > threshold, 0.5, 1)  # 50% of traders migrate if fee > threshold
    adjusted_swaps = swap_sizes * migrated
    adjusted_total_costs = adjusted_swaps * base_fee * fee_multiplier + gas_cost
    return adjusted_total_costs

# Simulate migration
migration_results = [liquidity_migration(fm, base_gas_cost) for fm in fee_multipliers]

# Visualize liquidity migration
plt.figure(figsize=(10, 6))
for i, costs in enumerate(migration_results):
    plt.hist(costs, bins=50, alpha=0.5, label=f"Fee x{fee_multipliers[i]:.1f}")
plt.title("Liquidity Migration - Impact of High Fees and Gas on Total Costs")
plt.xlabel("Remaining Total Cost")
plt.ylabel("Frequency")
plt.legend()
plt.show()

# Compare total adjusted costs by migration
print("Impact of Liquidity Migration on Total Costs:")
for i, fm in enumerate(fee_multipliers):
    print(f"Fee x{fm:.1f}: Remaining average total cost = {np.mean(migration_results[i]):.4f}")
