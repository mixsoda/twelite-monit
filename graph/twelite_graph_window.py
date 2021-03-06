#%%
#
# Nature remo sensor data visualizer
#

#import and initialize
import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt
import sys

import matplotlib
#matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#get commandline args
args = sys.argv

if len(args) != 2 :
    print("Usage : python twelite_graph_window.py logfile.csv")
    sys.exit()

#read data from cvs to pandas data frame
df_2FS = pd.read_csv('../log/'+args[1], names=['time', 'seq', 'LQI', 'lock', 'battery', 'ADC'])
df_2FS.time = pd.to_datetime(df_2FS.time,format='%Y-%m-%dT%H:%M:%S')
df_2FS = df_2FS.set_index('time')

df_2FS = df_2FS.sort_index()

df_2FS.loc[df_2FS['lock'] == 128, 'lock'] = 0
df_2FS.loc[df_2FS['lock'] == 129, 'lock'] = 1

df_LQI_mean = df_2FS["LQI"].resample("D").mean()
df_LQI_max = df_2FS["LQI"].resample("D").max()
df_LQI_min = df_2FS["LQI"].resample("D").min()

df_wopen_1min = df_2FS["lock"].resample('1min').mean().interpolate('time')
df_wopen = (df_wopen_1min/60).resample('D').sum()

df_BATT_mean = df_2FS["battery"].resample("D").mean()
df_BATT_max = df_2FS["battery"].resample("D").max()
df_BATT_min = df_2FS["battery"].resample("D").min()

#%%
#visualize data
#all
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
cmap = plt.get_cmap("Set1")
ax1.set_title("Sensor data (All period, LQI, open time, battery)")

ax1.plot(df_LQI_mean.index, df_LQI_mean, color=cmap(1))
ax1.fill_between(df_LQI_mean.index, df_LQI_max, df_LQI_min, alpha=0.3, color=cmap(1))
ax1.set_ylabel('LQI (-)')
ax1.xaxis_date()

ax2.plot(df_wopen.index, df_wopen, color=cmap(2))
ax2.set_yticks([0, 6, 12, 18, 24])
ax2.set_ylabel('hours/day')
ax2.xaxis_date()

ax3.plot(df_BATT_mean.index, df_BATT_mean, color=cmap(3))
ax3.fill_between(df_LQI_mean.index, df_BATT_max, df_BATT_min, alpha=0.3, color=cmap(3))
ax3.set_ylabel('Battery (mV)')
ax3.xaxis_date()

fig.autofmt_xdate()
plt.tight_layout()
plt.savefig("window_lock_monitor_2FS_"+str(dt.date.today())+".png")
plt.show()

# %%
