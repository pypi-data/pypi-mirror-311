import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import sys

#chose depth layer
layer = 'surface'
#layer = 'deep'

if layer == 'surface':
    ncnames  = ['result_surface_winter.nc','result_surface_summer.nc','result_surface_year.nc']
    z_layers = [0,4,8]
#deep
if layer == 'deep':
    ncnames  = ['result_deep_winter.nc','result_deep_summer.nc','result_deep_year.nc']
    z_layers = [25,50,75]

communities = ['P','Z','TOT']

ny = 5

for inc,ncname in enumerate(ncnames):
    # Load the data
    ds = xr.open_dataset(ncname)
    fig,axs = plt.subplots(3,3,figsize=(10,10))

    #compute the mean of ds such that the mean is computed over the same days of all the years and the output is a year long timeseries
    ds = ds.groupby('time.dayofyear').mean('time')
    time = np.array(ds['dayofyear'][:])    

    #get the indexes of the z_layers
    depth = ds.depth.values
    z_indexes = np.zeros(3,dtype=int)
    for iz,z_layer in enumerate(z_layers):
        z_indexes[iz] = np.argmin(np.abs(depth+z_layer))
    for icomm,community in enumerate(communities):
        for iax,iz in enumerate(z_indexes):
            #mean biomass (time,species)
            mean_biomass = np.array(ds[community][:,:,iz])
            if community == 'TOT':
                long_names = np.array(ds['long_species'][0,:])
                short_names = np.array(ds['species'][0,:])
                paper_names = np.array(ds['paper_species'][0,:])
            else:
                short_names = np.array(ds['species'+community][0,:])
                long_names = np.array(ds['long_species'+community][0,:])
                paper_names = np.array(ds['paper_species'+community][0,:])
            #in long_names if the species is Heterotrophic Nanoflagellates (HNAN) add string '_ ' to the long name
            long_names = np.array([long_names[i]+'_ ' if 'HNAN' in long_names[i] else long_names[i] for i in range(len(long_names))])
            #same for bacteria
            long_names = np.array([long_names[i]+'_ ' if 'Bacteria' in long_names[i] else long_names[i] for i in range(len(long_names))])
            species_names = np.array([short_names[ii].split('_')[0]+'_'+long_names[ii].split('_')[1] for ii in range(len(short_names))])
            species_names = paper_names
            count = np.count_nonzero(~np.isnan(mean_biomass), axis=0)
            species_names = species_names[count >= ny]
            mean_biomass = mean_biomass[:,count >= ny]
            #reorder mean_biomass and species_names as the magnitude of np.mean(mean_biomass,axis=0)
            indexes = np.argsort(np.nan_to_num(np.nanmean(mean_biomass,axis=0), copy=False, nan=-np.inf))[::-1]
            mean_biomass = mean_biomass[:,indexes]
            species_names = species_names[indexes]
            #how many species to label
            nlabels = 5
            for ispec,spe_name in enumerate(species_names):
                if ispec < nlabels:
                    axs[icomm,iax].plot(time,mean_biomass[:,ispec],label=spe_name,alpha=0.8)
                else:
                    axs[icomm,iax].plot(time,mean_biomass[:,ispec],alpha=0.3)
            axs[icomm,iax].set_title(community+' at '+str(round(depth[iz], 3))[:4]+' m')
            axs[icomm,iax].set_yscale('log')
            if community == 'TOT':
                axs[icomm,iax].set_xlabel('day of year')
            axs[icomm,iax].set_ylabel('biomass $[mgC/m^3]$')
            axs[icomm,iax].legend(loc='lower center')
    fig.tight_layout()
    plt.show()
    fig.savefig('mean_biomass_'+ncname[:-3]+'.png')

            



