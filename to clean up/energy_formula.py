#cheapest plan ampol 
daily_supply_1 = 0.95
usage_1 = 0.26
solar_fit_1 = 0.05

#current plan alinta
daily_supply_2 = 1.1
usage_2 = 0.29
solar_fit_2 = 0.08

def daily_cost(total_usage, paid_usage, solar): 
    no_solar_cost = daily_supply_1 + total_usage*usage_1
    ampol_cost = daily_supply_1 + paid_usage*usage_1 - solar*solar_fit_1
    current_cost = daily_supply_2 + paid_usage*usage_2 - solar*solar_fit_2
    ampol_saving = no_solar_cost - ampol_cost
    current_saving = no_solar_cost - current_cost
    print("No solar cost: $" + str(no_solar_cost))
    print("Ampol cost: $" + str(ampol_cost))
    print("Current cost: $" + str(current_cost))
    print("Ampol saving: $" + str(ampol_saving))
    print("Current saving: $" + str(current_saving))

# daily_cost(19.1, 8.4, 26.2)
# daily_cost(5.4, 3.1, 29.2)
daily_cost(10, 5, 10)


def calculate_costs(total_usage, paid_usage, solar): 
    ampol_cost = daily_supply_1 + paid_usage*usage_1 - solar*solar_fit_1
    current_cost = daily_supply_2 + paid_usage*usage_2 - solar*solar_fit_2
    return ampol_cost, current_cost

import numpy as np
import matplotlib.pyplot as plt
total_usage_range = np.linspace(4, 25, 22)  # 100 points from 4 to 30
paid_usage_range = np.linspace(2, 15, 14)  # 100 points from 2 to 20
solar_range = np.linspace(10, 30, 21)      # 100 points from 10 to 35

ampol_costs = []
current_costs = []
matching_values = []  # Store matching (total_usage, paid_usage, solar, cost)

tolerance = 1e-6  # Allow small floating-point differences

for total_usage in total_usage_range:
    for paid_usage in paid_usage_range:
        if paid_usage < total_usage:
            for solar in solar_range:
                ampol_cost, current_cost = calculate_costs(total_usage, paid_usage, solar)
                ampol_costs.append(ampol_cost)
                current_costs.append(current_cost)

                # Check if costs are approximately the same
                if abs(ampol_cost - current_cost) < tolerance:
                    matching_values.append((total_usage, paid_usage, solar, ampol_cost))
matching_values.sort(key=lambda x: x[2])

# Output matching values
print("total of " + str(len(ampol_costs)) + 'and only '+ str(len(matching_values)) + 'matches')
for match in matching_values:
    print(f"Match found: Total Usage={match[0]}, Paid Usage={match[1]}, Solar={match[2]}, Cost=${match[3]:.2f}")

if not matching_values:
    print("No matches found where Ampol cost equals Current cost.")

# Extract data
total_usage_values = [match[0] for match in matching_values]
paid_usage_values = [match[1] for match in matching_values]
solar_values = [match[2] for match in matching_values]
cost_values = [match[3] for match in matching_values]

# Plot
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(total_usage_values, paid_usage_values, solar_values, c=cost_values, cmap='viridis', alpha=0.8)

# Add color bar
plt.colorbar(scatter, ax=ax, label="Cost ($)")

# Labels
ax.set_title("4D Data Visualization: Cost as Color")
ax.set_xlabel("Total Usage (kWh)")
ax.set_ylabel("Paid Usage (kWh)")
ax.set_zlabel("Solar (kWh)")

plt.show()