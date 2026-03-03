import pandas as pd
import os
from glob import glob

daily_export_folder_path = 'daily_export'
csv_files = glob(os.path.join(daily_export_folder_path, '*.csv'))
daily_export_concat_path = 'generated_data/daily_export_concat.csv'

try: 
    daily_export_concat = pd.read_csv(daily_export_concat_path)
except Exception:
    dfs = [pd.read_csv(file) for file in csv_files]
    daily_export_concat = pd.concat(dfs, ignore_index=True)
    daily_export_concat.to_csv(daily_export_concat_path, index=False)

columns = ['Time','PV(W)','Grid(W)','Load(W)']

cols_to_convert = ["PV(W)", "Grid(W)", "Load(W)"]

daily_export_concat[cols_to_convert] = (
    daily_export_concat[cols_to_convert]
        .apply(pd.to_numeric, errors="coerce")
)

daily_export_concat['Time'] = pd.to_datetime(daily_export_concat.iloc[:,0])
daily_export_concat = daily_export_concat.sort_values('Time').set_index('Time')
hourly = daily_export_concat.resample('h').sum()/12000

hourly['month'] = hourly.index.month
hourly['hour'] = hourly.index.hour

hourly_agg = hourly.groupby(['month','hour']).agg({
    'PV(W)': ['mean','max','min'],
    'Grid(W)': ['mean','max','min'],
    'Load(W)': ['mean','max','min']
}).round(1)
print(hourly_agg.head())
hourly_agg.to_csv('generated_data/hourly_aggregated.csv')

def hour_to_period(hour):
    if 23 <= hour or hour < 6:
        return "11pm-6am"
    elif 6 <= hour < 11:
        return "6am-11am"
    elif 11 <= hour < 14:
        return "11am-2pm"
    elif 14 <= hour < 16:
        return "2pm-4pm"
    elif 16 <= hour < 18:
        return "4pm-6pm"
    elif 18 <= hour < 20:
        return "6pm-8pm"
    else:
        return "8pm-11pm"

hours = hourly_agg.index.get_level_values('hour')
periods = hours.map(hour_to_period)
hourly_periods = hourly_agg.copy()
hourly_periods['period'] = periods

period_agg = (
    hourly_periods.groupby([hourly_periods.index.get_level_values('month'), 'period']).sum().round(1)
)

period_order = [
    '11pm-6am',
    '6am-11am',
    '11am-2pm',
    '2pm-4pm',
    '4pm-6pm',
    '6pm-8pm',
    '8pm-11pm'
]

period_agg = period_agg.reset_index()

period_agg['period'] = pd.Categorical(
    period_agg['period'],
    categories=period_order,
    ordered=True
)

period_agg = period_agg.sort_values(['month','period'])
period_agg = period_agg.set_index(["month", "period"])
print(period_agg.head())
period_agg.to_csv('generated_data/period_agg.csv')