import glob
import pandas as pd
from datetime import datetime

entire_solar_data = glob.glob('solar_data/*.csv')
print(entire_solar_data)
analysed_solar_data = pd.DataFrame(columns=[
    'Month', 
    'Num of Day', 
    # Basic sum
    'Total Production', 
    'Total Purchased', 
    'Total Feed-in', 
    'Total Load',
    'Total Consumption',
    # Cost Calculation
    'Total Cost',
    'Original Cost',
    'Total Saving',
])
solar_data_production_data = pd.DataFrame(columns=[
    'Month', 
    'Num of Day', 
    'Total Production', 
    'Average Daily Production',
    'Median Daily Production',
    'Max Daily Production',
    'Min Daily Production'
])
solar_data_purchase_data = pd.DataFrame(columns=[
    'Month', 
    'Num of Day', 
    'Total Purchased', 
    'Average Daily Purchased',
    'Median Daily Purchased',
    'Max Daily Purchased',
    'Min Daily Purchased'
])
solar_data_feedin_data = pd.DataFrame(columns=[
    'Month', 
    'Num of Day', 
    'Total Feed-in', 
    'Average Daily Feed-in',
    'Median Daily Feed-in',
    'Max Daily Feed-in',
    'Min Daily Feed-in'
])
solar_data_load_data = pd.DataFrame(columns=[
    'Month', 
    'Num of Day', 
    'Total Load', 
    'Average Daily Load',
    'Median Daily Load',
    'Max Daily Load',
    'Min Daily Load'
])
solar_data_consumption_data = pd.DataFrame(columns=[
    'Month', 
    'Num of Day', 
    'Total Production', 
    'Total Load', 
    'Total Solar Consumed',
    'Average Daily Solar Consumed',
    'Median Daily Solar Consumed',
    'Max Daily Solar Consumed',
    'Min Daily Solar Consumed'
])
# Current Electricity Price
daily_supply_charge = 0.9449
per_kwh_charge = 0.2618
feed_in_tariff = 0.05

aggregated_data_columns = []

for i, month_data in enumerate(entire_solar_data):
    df = pd.read_csv(month_data)
    for col_index, column in enumerate(df.columns):
        col_name = column.lower()
        if not (col_index, col_name) in aggregated_data_columns:
            if i != 0:
                print('Data Structure Inconsistency: Check File' + entire_solar_data[i])
            aggregated_data_columns.append((col_index, col_name))
print(aggregated_data_columns)
column_names = []
for i, column_name in sorted(aggregated_data_columns):
    column_names.append(column_name)
print(column_names)
aggregated_daily_data = pd.DataFrame(columns=column_names)
for monthly_data in entire_solar_data:
    df = pd.read_csv(monthly_data)
    df.columns = [col.lower() for col in df.columns]
    df = df[column_names]
    if not df.empty:
        aggregated_daily_data = pd.concat([aggregated_daily_data, df], ignore_index=True)
        
aggregated_daily_data = aggregated_daily_data.sort_values(by=aggregated_daily_data.columns[0])
aggregated_daily_data.to_csv('aggregated_data.csv', index=False)

# for month_data in entire_solar_data:
#     df = pd.read_csv(month_data)
#     month = datetime.strptime(df.iloc[0, 0], '%Y-%m-%d')
#     month_num = month.month
#     month_name = month.strftime('%B')
#     month_label = str(month_num) + ' ' + month_name
#     day_num = df.iloc[:, 0].count()
#     total_solar_production = round(df.iloc[:, 1].sum(), 1)
#     total_purchased_energy = round(df.iloc[:, 2].sum(), 1)
#     total_feed_in = round(df.iloc[:, 3].sum(), 1)
#     total_load = round(df.iloc[:, 4].sum(), 1)
#     total_solar_consumption = total_solar_production - total_feed_in
#     total_cost = round(day_num * daily_supply_charge + total_purchased_energy * per_kwh_charge - total_feed_in * feed_in_tariff, 1)
#     original_cost = round(day_num * daily_supply_charge + total_load * per_kwh_charge, 1)
#     total_saving = round(original_cost - total_cost, 1)
#     average_daily_cost = round(total_cost / day_num, 1)
#     average_daily_saving = round(total_saving / day_num, 1)
    
#     analysed_solar_data.loc[len(analysed_solar_data)] = [
#         month_label, 
#         day_num, 
#         total_solar_production, 
#         total_purchased_energy, 
#         total_feed_in, 
#         total_load,
#         total_solar_consumption,
#         total_cost,
#         original_cost,
#         total_saving
#     ]

#     average_daily_production = round(total_solar_production / day_num, 1)
#     median_daily_production = df.iloc[:, 1].median()
#     max_daily_production = df.iloc[:, 1].max()
#     min_daily_production = df.iloc[:, 1].min()
#     solar_data_production_data.loc[len(solar_data_production_data)] = [
#         month_label, 
#         day_num, 
#         total_solar_production, 
#         average_daily_production,
#         median_daily_production,
#         max_daily_production,
#         min_daily_production
#     ]

#     average_daily_purchase= round(total_purchased_energy / day_num, 1)
#     median_daily_purchase = df.iloc[:, 2].median()
#     max_daily_purchase = df.iloc[:, 2].max()
#     min_daily_purchase = df.iloc[:, 2].min()
#     solar_data_purchase_data.loc[len(solar_data_purchase_data)] = [
#         month_label, 
#         day_num, 
#         total_purchased_energy, 
#         average_daily_purchase,
#         median_daily_purchase,
#         max_daily_purchase,
#         min_daily_purchase
#     ]

#     average_daily_feed_in = round(total_feed_in / day_num, 1)
#     median_daily_feedin = df.iloc[:, 3].median()
#     max_daily_feedin = df.iloc[:, 3].max()
#     min_daily_feedin = df.iloc[:, 3].min()
#     solar_data_feedin_data.loc[len(solar_data_feedin_data)] = [
#         month_label, 
#         day_num, 
#         total_feed_in, 
#         average_daily_feed_in,
#         median_daily_feedin,
#         max_daily_feedin,
#         min_daily_feedin
#     ]

#     average_daily_total_load = round(total_load / day_num, 1)
#     median_daily_load = df.iloc[:, 4].median()
#     max_daily_load = df.iloc[:, 4].max()
#     min_daily_load = df.iloc[:, 4].min()
#     solar_data_load_data.loc[len(solar_data_load_data)] = [
#         month_label, 
#         day_num, 
#         total_load, 
#         average_daily_total_load,
#         median_daily_load,
#         max_daily_load,
#         min_daily_load
#     ]

#     average_daily_solar_consumption = round(total_solar_consumption / day_num, 1)
#     median_daily_consumption = analysed_solar_data.iloc[:, 6].median()
#     max_daily_consumption = analysed_solar_data.iloc[:, 6].max()
#     min_daily_consumption = analysed_solar_data.iloc[:, 6].min()
#     solar_data_consumption_data.loc[len(solar_data_consumption_data)] = [
#         month_label, 
#         day_num, 
#         total_solar_production,
#         total_load, 
#         total_solar_consumption,
#         average_daily_solar_consumption,
#         median_daily_consumption,
#         max_daily_consumption,
#         min_daily_consumption
#     ]

# analysed_solar_data_sorted = analysed_solar_data.sort_values(by=analysed_solar_data.columns[0], ascending=True).reset_index(drop=True)
# solar_data_production_data_sorted = solar_data_production_data.sort_values(by=solar_data_production_data.columns[0], ascending=True).reset_index(drop=True)
# solar_data_purchase_data_sorted = solar_data_purchase_data.sort_values(by=solar_data_purchase_data.columns[0], ascending=True).reset_index(drop=True)
# solar_data_feedin_data_sorted = solar_data_feedin_data.sort_values(by=solar_data_feedin_data.columns[0], ascending=True).reset_index(drop=True)
# solar_data_load_data_sorted = solar_data_load_data.sort_values(by=solar_data_load_data.columns[0], ascending=True).reset_index(drop=True)
# solar_data_consumption_data_sorted = solar_data_consumption_data.sort_values(by=solar_data_consumption_data.columns[0], ascending=True).reset_index(drop=True)
# pd.set_option('display.colheader_justify', 'left')
# table1_to_print = analysed_solar_data_sorted.to_string(formatters={analysed_solar_data_sorted.columns[0]: '{:<15}'.format})
# table2_to_print = solar_data_production_data_sorted.to_string(formatters={solar_data_production_data_sorted.columns[0]: '{:<15}'.format})
# table3_to_print = solar_data_purchase_data_sorted.to_string(formatters={solar_data_purchase_data_sorted.columns[0]: '{:<15}'.format})
# table4_to_print = solar_data_feedin_data_sorted.to_string(formatters={solar_data_feedin_data_sorted.columns[0]: '{:<15}'.format})
# table5_to_print = solar_data_load_data_sorted.to_string(formatters={solar_data_load_data_sorted.columns[0]: '{:<15}'.format})
# table6_to_print = solar_data_consumption_data_sorted.to_string(formatters={solar_data_consumption_data_sorted.columns[0]: '{:<15}'.format})
# print('Overall Essential Data')
# print(table1_to_print)
# print()
# print('Daily Solar Production Analysis')
# print(table2_to_print)
# print()
# print('Daily Purchase kwh Analysis')
# print(table3_to_print)
# print()
# print('Daily Solar Feed-in Analysis')
# print(table4_to_print)
# print()
# print('Daily Load Analysis')
# print(table5_to_print)
# print()
# print('Daily Consumption Analysis')
# print(table6_to_print)
