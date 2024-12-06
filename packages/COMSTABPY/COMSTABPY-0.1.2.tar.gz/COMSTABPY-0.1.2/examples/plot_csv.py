import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = pd.read_csv('sat_data.csv')

#transform data['date'] to datetime, the data are in the form of 'yyyymmdd'
data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')

#vars to plot
vars_plt_1 = ['CRYPTO','DIATO','DINO','GREEN','HAPTO','PROKAR']
vars_plt_2 = ['MICRO','NANO','PICO']

fig,axs = plt.subplots(1,2, figsize=(10,5))
axs = axs.flatten()
for ivar,var in enumerate(vars_plt_1):
    axs[0].plot(data['date'].values,data[var].values,label=var)
for ivar,var in enumerate(vars_plt_2):
    axs[1].plot(data['date'].values,data[var].values,label=var)

for ax in axs:
    ax.set_xlabel('Date')
    ax.set_ylabel('$mg CHL/m^3$')
    ax.legend()
fig.tight_layout()
figname = 'sat_data.png'
fig.savefig(figname,dpi=600)