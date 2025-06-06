import glob
import pandas as pd
from datetime import datetime

entire_solar_data = glob.glob('solar_data/*.csv')
analysed_solar_data = pd.DataFrame(columns=[
    'Month', 
    'Num of Day', 
    # Basic sum
    'Total Production', 
    'Total Purchased', 
    'Total Feed-in', 
    'Total Load',
    # Cost Calculation
    'Total Cost',
    'Original Cost',
    'Total Saving',
    #Average Daily Elements
    'Average Daily Cost',
    'Average Daily Saving',
    'Average Daily Production',
    'Average Daily Solar Consumption',
    'Average Daily Feed-in',
    'Average Daily Total Load'
])

# Current Electricity Price
daily_supply_charge = 0.9449
per_kwh_charge = 0.2618
feed_in_tariff = 0.05

for month_data in entire_solar_data:
    df = pd.read_csv(month_data)
    month = datetime.strptime(df.iloc[0, 0], '%Y-%m-%d')
    month_num = month.month
    month_name = month.strftime('%B')
    month_label = str(month_num) + ' ' + month_name
    day_num = df.iloc[:, 0].count()
    total_solar_production = round(df.iloc[:, 1].sum(), 1)
    total_purchased_energy = round(df.iloc[:, 2].sum(), 1)
    total_feed_in = round(df.iloc[:, 3].sum(), 1)
    total_load = round(df.iloc[:, 4].sum(), 1)
    total_solar_consumption = total_solar_production - total_feed_in
    total_cost = round(day_num * daily_supply_charge + total_purchased_energy * per_kwh_charge - total_feed_in * feed_in_tariff, 1)
    original_cost = round(day_num * daily_supply_charge + total_load * per_kwh_charge, 1)
    total_saving = round(original_cost - total_cost, 1)
    average_daily_cost = round(total_cost / day_num, 1)
    average_daily_saving = round(total_saving / day_num, 1)
    average_daily_production = round(total_solar_production / day_num, 1)
    average_daily_solar_consumption = round(total_solar_consumption / day_num, 1)
    average_daily_feed_in = round(total_feed_in / day_num, 1)
    average_daily_total_load = round(total_load / day_num, 1)
    analysed_solar_data.loc[len(analysed_solar_data)] = [
        month_label, 
        day_num, 
        total_solar_production, 
        total_purchased_energy, 
        total_feed_in, 
        total_load,
        total_cost,
        original_cost,
        total_saving,
        average_daily_cost,
        average_daily_saving,
        average_daily_production,
        average_daily_solar_consumption,
        average_daily_feed_in,
        average_daily_total_load
    ]

analysed_solar_data_sorted = analysed_solar_data.sort_values(by=analysed_solar_data.columns[0], ascending=True).reset_index(drop=True)
pd.set_option('display.colheader_justify', 'left')
table_to_print = analysed_solar_data_sorted.to_string(formatters={analysed_solar_data_sorted.columns[0]: '{:<15}'.format})
print(table_to_print)
