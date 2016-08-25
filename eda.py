# Importing required modules

import pandas as pd
import blaze as blz
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

# loading data; data was downloaded and saved to a sqlite database
# separately (code can be found here: 
# https://github.com/pohalloran/airline-delays/blob/master/download.py)
# I use Blaze (http://blaze.pydata.org/) to query the sqlite db in parallel
# and collapse the data by month and year for these exploratory graphs

ds1 = blz.Data('sqlite:///./data/flights.db::flights')
ds2 = blz.by(blz.merge(ds1.Month, ds1.Year), delcount=ds1.DepDel15.sum(), 
             totcount=ds1.Flights.sum())
ds3 = blz.into(pd.DataFrame, ds2)
ds3['percentdelay'] = ds3.delcount/ds3.totcount
ds3 = ds3.sort(["Year", "Month"])
ds3['date'] = pd.date_range('1987-10-01', periods=345, freq='M')

# setting up plot

demand = ds3[['totcount', 'date']]
demand = demand.set_index(['date'])
f, ax = plt.subplots(figsize=(12,9))
demand.plot(x_compat=True,ax=ax)
plt.ylabel('Number of flights')
plt.xlabel('Year')

# generate heatmap for delays

pivot = ds3.pivot("Month", "Year", "percentdelay")

f, ax = plt.subplots(figsize=(12, 9))
heatmap = sns.heatmap(pivot)

# delays by carrier bar graph

ds4 = blz.by(ds1.Carrier, ndelays = ds1.DepDel15.sum(), ntot = ds1.Flights.sum())
carriers = blz.into(pd.DataFrame, ds4)
carriers['pctdelay'] = carriers.ndelays/carriers.ntot
carriers = carriers.sort(['pctdelay'], ascending=False)

f, ax = plt.subplots(figsize=(12,9))
sns.barplot(x='Carrier', y='pctdelay', data=carriers, palette="RdYlGn")
plt.ylabel('Percentage of flights delayed')
plt.xlabel('Carrier')
