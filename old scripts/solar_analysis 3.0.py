import os
import pandas as pd
import matplotlib.pyplot as plt

# Define folder path
folder_path = 'solar_data'

# Updated day type thresholds
def get_day_type(pv):
    if pv > 23:
        return 'Red'
    elif pv >= 15:
        return 'Yellow'
    else:
        return 'Blue'

# Load data
all_data = []
for file in os.listdir(folder_path):
    if file.endswith('.csv'):
        df = pd.read_csv(os.path.join(folder_path, file))
        df['Time'] = pd.to_datetime(df['Time'])
        df['Day Type'] = df['PV(kWh)'].apply(get_day_type)
        all_data.append(df)

# Combine and sort
data = pd.concat(all_data)
data = data.sort_values('Time')
data['MM-DD'] = data['Time'].dt.strftime('%m-%d')

# Color map
color_map = {'Red': 'red', 'Yellow': 'gold', 'Blue': 'blue'}
bar_colors = data['Day Type'].map(color_map)

# Chart 1: Daily PV Production
plt.figure(figsize=(14, 6))
plt.bar(data['MM-DD'], data['PV(kWh)'], color=bar_colors)
plt.xticks(rotation=90)
plt.title('Daily PV Production (Color-Coded)')
plt.ylabel('PV(kWh)')
plt.xlabel('Date (MM-DD)')
plt.tight_layout()
plt.show()

# Chart 2: % of Day Types per Month
data['Month'] = data['Time'].dt.strftime('%B')
day_type_pct = data.groupby(['Month', 'Day Type']).size().unstack().fillna(0)
day_type_pct_percent = day_type_pct.div(day_type_pct.sum(axis=1), axis=0) * 100

month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
day_type_pct_percent = day_type_pct_percent.reindex(month_order).dropna(how='all')

day_type_pct_percent.plot(
    kind='bar',
    stacked=True,
    figsize=(10, 6),
    color=[color_map.get(col, 'gray') for col in day_type_pct_percent.columns]
)
plt.title('Percentage of Day Types per Month')
plt.ylabel('Percentage (%)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Chart 3: Count of Blue Days per Month
blue_days = data[data['Day Type'] == 'Blue'].groupby('Month').size()
blue_days = blue_days.reindex(month_order).dropna()

blue_days.plot(kind='bar', color='blue', figsize=(8, 5))
plt.title('Number of Rainy (Blue) Days per Month')
plt.ylabel('Number of Days')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
