#%%
#
# TWELITE soil moisture monitoring data visualizer
#

#import and initialize
import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt
import sys

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#get commandline args
args = sys.argv

if len(args) != 2 :
    print("Usage : python twelite_graph_soil_moisture.py logfile.csv")
    sys.exit()

#read data from cvs to pandas data frame
df_moisture = pd.read_csv('../log/'+args[1], names=['time', 'seq', 'LQI', 'battery', 'ai1', 'ai2', 'ai3', 'ai4'])
df_moisture.time = pd.to_datetime(df_moisture.time,format='%Y-%m-%dT%H:%M:%S')
df_moisture.time = df_moisture.time
df_moisture = df_moisture.set_index('time')

#print(df_moisture)

#%%
#visualize data
#all
fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6, 1, sharex=True, figsize=(6.0, 8.0))
cmap = plt.get_cmap("tab10")
ax1.set_title("Sensor data (All period, LQI, battery, analog input)")

ax1.plot(df_moisture.index, df_moisture["LQI"], color=cmap(0))
ax1.set_ylabel('LQI (-)')
ax1.xaxis_date()

ax2.plot(df_moisture.index, df_moisture["battery"], color=cmap(1))
ax2.set_ylabel('Battery (mV)')
ax2.set_ylim(2400,2900)
ax2.xaxis_date()

ax3.set_title('Strelitzia', loc='left')
ax3.plot(df_moisture.index, df_moisture["ai1"], color=cmap(2))
ax3.set_ylabel('Input 1 (mV)')
ax3.xaxis_date()

ax4.set_title('Pachira', loc='left')
ax4.plot(df_moisture.index, df_moisture["ai2"], color=cmap(3))
ax4.set_ylabel('Input 2 (mV)')
ax4.xaxis_date()

ax5.set_title('Unbellata', loc='left')
ax5.plot(df_moisture.index, df_moisture["ai3"], color=cmap(4))
ax5.set_ylabel('Input 3 (mV)')
ax5.xaxis_date()

ax6.set_title('Illuminance', loc='left')
ax6.plot(df_moisture.index, df_moisture["ai4"], color=cmap(8))
ax6.set_ylabel('Input 4 (mV)')
ax6.xaxis_date()

fig.autofmt_xdate()
plt.tight_layout()
plt.savefig("soil_moisture_monitor_"+str(dt.date.today())+".png")
#plt.show()