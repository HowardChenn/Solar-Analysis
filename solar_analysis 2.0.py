import pandas as pd
import os
from glob import glob

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

all_data['Month'] = all_data['Time'].dt.to_period('M')

monthly_stats = all_data.groupby('Month').agg(
    total_production_kWh=('PV(kWh)', 'sum'),
    total_purchased_kWh=('Purchased Energy(kWh)', 'sum'),
    total_feed_in_kWh=('Feed-in(kWh)', 'sum'),
    total_load_kWh=('Load(kWh)', 'sum'),
    days=('Time', 'nunique')
).reset_index()

monthly_stats['total_cost'] = (
    0.95 * monthly_stats['days'] +
    0.26 * monthly_stats['total_purchased_kWh'] -
    0.05 * monthly_stats['total_feed_in_kWh']
)
monthly_stats['original_cost'] = (
    0.95 * monthly_stats['days'] +
    0.26 * monthly_stats['total_load_kWh']
)
monthly_stats['total_saving'] = monthly_stats['original_cost'] - monthly_stats['total_cost']

monthly_stats['avg_daily_saving'] = monthly_stats['total_saving'] / monthly_stats['days']
monthly_stats['avg_daily_production'] = (monthly_stats['total_production_kWh'] / monthly_stats['days']).round(1)
monthly_stats['avg_daily_solar_consumed'] = (
    (monthly_stats['total_load_kWh'] - monthly_stats['total_purchased_kWh']) / monthly_stats['days']
)
monthly_stats['avg_daily_feed_in'] = (monthly_stats['total_feed_in_kWh'] / monthly_stats['days']).round(1)
monthly_stats['avg_daily_total_load'] = (monthly_stats['total_load_kWh'] / monthly_stats['days']).round(1)

monthly_stats = monthly_stats[
    [
        'Month',
        'total_production_kWh',
        # 'total_feed_in_kWh',
        'total_load_kWh',
        # 'total_purchased_kWh',
        'days',
        # 'total_cost',
        # 'original_cost',
        # 'total_saving',
        # 'avg_daily_saving',
        'avg_daily_production',
        # 'avg_daily_solar_consumed',
        # 'avg_daily_feed_in',
        'avg_daily_total_load'
    ]
]

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', None)

print(monthly_stats)

monthly_stats.to_csv('monthly_solar_report.csv', index=False)
