#%%
#
# Nature remo sensor data visualizer
#

#import and initialize
import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt

import matplotlib
#matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#read data from cvs to pandas data frame
df_2FS = pd.read_csv('id1.csv', names=['time', 'seq', 'LQI', 'lock', 'battery', 'ADC'])
df_2FS.time = pd.to_datetime(df_2FS.time,format='%Y-%m-%dT%H:%M:%S')
df_2FS = df_2FS.set_index('time')

df_2FS = df_2FS.sort_index()

df_2FS.loc[df_2FS['lock'] == 128, 'lock'] = 0
df_2FS.loc[df_2FS['lock'] == 129, 'lock'] = 1

#print(df_2FS)


#%%
#visualize data
#all
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
cmap = plt.get_cmap("Set1")
ax1.set_title("Sensor data (All period, LQI, lock state, battery)")

ax1.plot(df_2FS.index, df_2FS["LQI"], color=cmap(1))
ax1.set_ylabel('LQI (-)')
ax1.xaxis_date()

ax2.plot(df_2FS.index, df_2FS["lock"], color=cmap(2))
ax2.set_ylabel('lock state')
ax2.xaxis_date()

ax3.plot(df_2FS.index, df_2FS["battery"], color=cmap(3))
ax3.set_ylabel('Battery (mV)')
ax3.xaxis_date()

fig.autofmt_xdate()
plt.savefig("window_lock_monitor_2FS_"+str(dt.date.today())+".png")
plt.show()

# %%
