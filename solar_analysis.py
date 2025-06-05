import glob
import pandas as pd
from datetime import datetime

entire_solar_data = glob.glob('solar_data/*.csv')

for month_data in entire_solar_data:
    df = pd.read_csv(month_data)
    month = datetime.strptime(df.iloc[0, 0], '%Y-%m-%d').month
    day_num = df.iloc[:, 0].count()
    total_solar_production = round(df.iloc[:, 1].sum(), 1)
    total_purchased_energy = round(df.iloc[:, 2].sum(), 1)
    total_feed_in = round(df.iloc[:, 3].sum(), 1)
    total_load = round(df.iloc[:, 4].sum(), 1)
    print('month: ' + str(month))
    print('total_solar_production')
    print(total_solar_production)
    print('total_purchased_energy')
    print(total_purchased_energy)
    print('total_feed_in')
    print(total_feed_in)
    print('total_load')
    print(total_load)
    print('number of days')
    print(day_num)

