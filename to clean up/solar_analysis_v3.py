import pandas as pd
import os
from glob import glob

# -----------------------------
# LOAD RAW DAILY DATA (UNCHANGED LOGIC)
# -----------------------------
folder_path = 'solar_data'
csv_files = glob(os.path.join(folder_path, '*.csv'))

all_data = pd.DataFrame()

for file in csv_files:
    df = pd.read_csv(file)

    if 'Purchased energy(kWh)' in df.columns:
        df = df.rename(columns={'Purchased energy(kWh)': 'Purchased Energy(kWh)'})
    if 'Energy purchase(kWh)' in df.columns:
        df = df.rename(columns={'Energy purchase(kWh)': 'Purchased Energy(kWh)'})

    df['Time'] = pd.to_datetime(df['Time'])
    all_data = pd.concat([all_data, df], ignore_index=True)

# -----------------------------
# MONTHLY AGGREGATION (UNCHANGED)
# -----------------------------
all_data['Month'] = all_data['Time'].dt.to_period('M')

monthly_stats = all_data.groupby('Month').agg(
    total_production_kWh=('PV(kWh)', 'sum'),
    total_purchased_kWh=('Purchased Energy(kWh)', 'sum'),
    total_feed_in_kWh=('Feed-in(kWh)', 'sum'),
    total_load_kWh=('Load(kWh)', 'sum'),
    days=('Time', 'nunique')
).reset_index()

# -----------------------------
# COST MODEL (UNCHANGED)
# -----------------------------
monthly_stats['total_cost'] = (
    0.95 * monthly_stats['days'] +
    0.26 * monthly_stats['total_purchased_kWh'] -
    0.05 * monthly_stats['total_feed_in_kWh']
)

monthly_stats['original_cost'] = (
    0.95 * monthly_stats['days'] +
    0.26 * monthly_stats['total_load_kWh']
)

monthly_stats['total_saving'] = (
    monthly_stats['original_cost'] - monthly_stats['total_cost']
)

monthly_stats['avg_daily_saving'] = monthly_stats['total_saving'] / monthly_stats['days']
monthly_stats['avg_daily_production'] = monthly_stats['total_production_kWh'] / monthly_stats['days']
monthly_stats['avg_daily_solar_consumed'] = (
    (monthly_stats['total_load_kWh'] - monthly_stats['total_purchased_kWh'])
    / monthly_stats['days']
)
monthly_stats['avg_daily_feed_in'] = monthly_stats['total_feed_in_kWh'] / monthly_stats['days']
monthly_stats['avg_daily_total_load'] = monthly_stats['total_load_kWh'] / monthly_stats['days']

monthly_stats = monthly_stats[
    [
        'Month',
        'total_production_kWh',
        'total_feed_in_kWh',
        'total_load_kWh',
        'total_purchased_kWh',
        'days',
        'total_cost',
        'original_cost',
        'total_saving',
        'avg_daily_saving',
        'avg_daily_production',
        'avg_daily_solar_consumed',
        'avg_daily_feed_in',
        'avg_daily_total_load'
    ]
]

# -----------------------------
# YEAR SUMMARY (NEW)
# -----------------------------
sum_columns = [
    'total_production_kWh',
    'total_feed_in_kWh',
    'total_load_kWh',
    'total_purchased_kWh',
    'total_cost',
    'original_cost',
    'total_saving'
]

year_totals = monthly_stats[sum_columns].sum()

avg_columns = [
    'avg_daily_saving',
    'avg_daily_production',
    'avg_daily_solar_consumed',
    'avg_daily_feed_in',
    'avg_daily_total_load'
]

weighted_year_averages = (
    (monthly_stats[avg_columns]
     .multiply(monthly_stats['days'], axis=0)
     .sum())
    / 365
)

# -----------------------------
# INSIGHTS (NEW)
# -----------------------------
monthly_stats['self_consumption_ratio'] = (
    (monthly_stats['total_load_kWh'] - monthly_stats['total_purchased_kWh'])
    / monthly_stats['total_production_kWh']
)

insights = {
    'best_saving_month': monthly_stats.loc[monthly_stats['total_saving'].idxmax()],
    'worst_saving_month': monthly_stats.loc[monthly_stats['total_saving'].idxmin()],
    'highest_production_month': monthly_stats.loc[monthly_stats['total_production_kWh'].idxmax()],
    'highest_grid_dependency_month': monthly_stats.loc[monthly_stats['total_purchased_kWh'].idxmax()],
    'best_self_consumption_month': monthly_stats.loc[monthly_stats['self_consumption_ratio'].idxmax()],
}

# -----------------------------
# OUTPUT
# -----------------------------
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print("\n========== MONTHLY SUMMARY ==========\n")
print(monthly_stats.round(3))

print("\n========== YEAR TOTALS ==========\n")
print(year_totals.round(2))

print("\n========== TRUE 12-MONTH AVERAGES ==========\n")
print(weighted_year_averages.round(3))

print("\n========== INSIGHTS ==========\n")
for k, v in insights.items():
    print(k)
    print(v)
    print()

monthly_stats.to_csv('monthly_solar_report.csv', index=False)







import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("monthly_solar_report.csv")
df["Month"] = df["Month"].astype(str)

# 1. Solar production vs household load
plt.figure()
plt.plot(df["Month"], df["total_production_kWh"], marker="o")
plt.plot(df["Month"], df["total_load_kWh"], marker="o")
plt.title("Monthly Solar Production vs Load")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Grid dependency
plt.figure()
plt.bar(df["Month"], df["total_purchased_kWh"])
plt.title("Monthly Grid Energy Purchased")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 3. Cost savings trend
plt.figure()
plt.plot(df["Month"], df["total_saving"], marker="o")
plt.title("Monthly Electricity Cost Savings")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 4. Feed-in vs self-consumed solar
self_consumed = df["total_load_kWh"] - df["total_purchased_kWh"]

plt.figure()
plt.plot(df["Month"], df["total_feed_in_kWh"], marker="o")
plt.plot(df["Month"], self_consumed, marker="o")
plt.title("Feed-in vs Self-Consumed Solar Energy")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 5. Average daily production
plt.figure()
plt.plot(df["Month"], df["avg_daily_production"], marker="o")
plt.title("Average Daily Solar Production")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
