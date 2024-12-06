import xarray as xr
import glob
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd

# Load the data
path = '/gss/gss_work/DRES_OGS_BiGe/Observations/TIME_RAW_DATA/ONLINE_V10C/SAT/CHL/DT/DAILY/ORIG/'
filenames = glob.glob(path+'*.nc')
#sort by date, names are in the format path/yearmonthday_name.nc
dates = np.array([int(f.split('/')[-1].split('_')[0]) for f in filenames])
#sort filenames by date
filenames = np.array([x for _,x in sorted(zip(dates,filenames))])
dates = np.array([x for x,_ in sorted(zip(dates,filenames))])
#select files from 2019 to 2020
filenames = filenames[(dates >= 20190101) & (dates <= 20231231)]
dates = dates[(dates >= 20190101) & (dates <= 20231231)]

#cordinates of boussole
lat = 43.367
lon = 7.9

ds = xr.open_dataset(filenames[0])
CHL = np.zeros(len(filenames))
WTM = np.zeros(len(filenames))
SENSORMASK = np.zeros(len(filenames))
QI_CHL = np.zeros(len(filenames))
CRYPTO = np.zeros(len(filenames))
DIATO = np.zeros(len(filenames))
DINO = np.zeros(len(filenames))
GREEN = np.zeros(len(filenames))
HAPTO = np.zeros(len(filenames))
MICRO = np.zeros(len(filenames))
NANO = np.zeros(len(filenames))
PICO = np.zeros(len(filenames))
PROKAR = np.zeros(len(filenames))

data_vars = np.array(ds.data_vars)

for idate,date in enumerate(dates):
    print('doing ',idate/len(dates)*100,'%')
    ds = xr.open_dataset(filenames[idate])
    #select lat and lon nearest to boussole plus minus 5 steps (5km here)
    ilat = np.argmin(np.abs(ds.lat.values-lat))
    ilon = np.argmin(np.abs(ds.lon.values-lon))
    #select the data
    CHL[idate] = np.nanmean(ds['CHL'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    WTM[idate] = np.nanmean(ds['WTM'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    SENSORMASK[idate] = np.nanmean(ds['SENSORMASK'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    QI_CHL[idate] = np.nanmean(ds['QI_CHL'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    CRYPTO[idate] = np.nanmean(ds['CRYPTO'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    DIATO[idate] = np.nanmean(ds['DIATO'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    DINO[idate] = np.nanmean(ds['DINO'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    GREEN[idate] = np.nanmean(ds['GREEN'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    HAPTO[idate] = np.nanmean(ds['HAPTO'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    MICRO[idate] = np.nanmean(ds['MICRO'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    NANO[idate] = np.nanmean(ds['NANO'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    PICO[idate] = np.nanmean(ds['PICO'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])
    PROKAR[idate] = np.nanmean(ds['PROKAR'].values[0,ilat-5:ilat+5:,ilon-5:ilon+5])

#save the data in csv file
df = pd.DataFrame({'date':dates,'CHL':CHL,'WTM':WTM,'SENSORMASK':SENSORMASK,'QI_CHL':QI_CHL,'CRYPTO':CRYPTO,
                     'DIATO':DIATO,'DINO':DINO,'GREEN':GREEN,'HAPTO':HAPTO,'MICRO':MICRO,'NANO':NANO,'PICO':PICO,'PROKAR':PROKAR})

df.to_csv('sat_data.csv',index=False)

#plot the data

#vars to plot
vars_plt = ['CRYPTO','DIATO','DINO','GREEN','HAPTO','MICRO','NANO','PICO','PROKAR']
fig,axs = plt.subplots()

for ivar,var in enumerate(vars_plt):
    axs.plot(df[var].values,label=var)

axs.legend()
fig.savefig('sat_data.png',dpi=600)

