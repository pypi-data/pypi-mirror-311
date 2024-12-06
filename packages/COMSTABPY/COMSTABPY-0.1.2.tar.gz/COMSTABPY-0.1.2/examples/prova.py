import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import sys

#chose depth layer
layer = 'surface'
#layer = 'deep'

if layer == 'surface':
    ncnames  = ['result_surface_year.nc']
    z_layers = [0]
#deep
if layer == 'deep':
    ncnames  = ['result_deep_winter.nc','result_deep_summer.nc','result_deep_year.nc']
    z_layers = [25,50,75]

communities = ['P','Z','TOT']

ny = 5

for inc,ncname in enumerate(ncnames):
    # Load the data
    ds = xr.open_dataset(ncname)
    fig,axs = plt.subplots(3,1,figsize=(10,10))

    #compute the mean of ds such that the mean is computed over the same days of all the years and the output is a year long timeseries
    #ds = ds.groupby('time.dayofyear').mean('time')
    #time = np.array(ds['dayofyear'][:])    
    time = np.array(ds['time'][:])

    #get the indexes of the z_layers
    depth = ds.depth.values
    z_indexes = np.zeros(3,dtype=int)
    for iz,z_layer in enumerate(z_layers):
        z_indexes[iz] = np.argmin(np.abs(depth+z_layer))
    iz = z_indexes[0]
    community = 'TOT'
    #mean biomass (time,species)
    mean_biomass = np.array(ds[community][:,:,iz])
    #long_names = np.array(ds['long_species'][0,:])
    long_names = np.array(ds['long_species'][:])
    #short_names = np.array(ds['species'][0,:])
    short_names = np.array(ds['species'][:])
    #in long_names if the species is Heterotrophic Nanoflagellates (HNAN) add string '_ ' to the long name
    long_names = np.array([long_names[i]+'_ ' if 'HNAN' in long_names[i] else long_names[i] for i in range(len(long_names))])
    #same for bacteria
    long_names = np.array([long_names[i]+'_ ' if 'Bacteria' in long_names[i] else long_names[i] for i in range(len(long_names))])
    species_names = np.array([short_names[ii].split('_')[0]+'_'+long_names[ii].split('_')[1] for ii in range(len(short_names))])
    
    mean_biomass = np.transpose(mean_biomass)
    count = np.count_nonzero(~np.isnan(mean_biomass), axis=0)
    species_names = species_names[count >= ny]
    mean_biomass = mean_biomass[:,count >= ny]
    #reorder mean_biomass and species_names as the magnitude of np.mean(mean_biomass,axis=0)
    indexes = np.argsort(np.nan_to_num(np.nanmean(mean_biomass,axis=0), copy=False, nan=-np.inf))[::-1]
    mean_biomass = mean_biomass[:,indexes]
    species_names = species_names[indexes]
    id_P1 = np.array([i for i in range(len(species_names)) if 'P1' in species_names[i]])
    id_P2 = np.array([i for i in range(len(species_names)) if 'P2' in species_names[i]])
    id_P3 = np.array([i for i in range(len(species_names)) if 'P3' in species_names[i]])
    id_P4 = np.array([i for i in range(len(species_names)) if 'P4' in species_names[i]])
    id_P5 = np.array([i for i in range(len(species_names)) if 'P5' in species_names[i]])
    id_P6 = np.array([i for i in range(len(species_names)) if 'P6' in species_names[i]])
    id_P7 = np.array([i for i in range(len(species_names)) if 'P7' in species_names[i]])
    id_P8 = np.array([i for i in range(len(species_names)) if 'P8' in species_names[i]])
    id_P9 = np.array([i for i in range(len(species_names)) if 'P9' in species_names[i]])
    id_Z3 = np.array([i for i in range(len(species_names)) if 'Z3' in species_names[i]])
    id_Z4 = np.array([i for i in range(len(species_names)) if 'Z4' in species_names[i]])
    id_Z5 = np.array([i for i in range(len(species_names)) if 'Z5' in species_names[i]])
    id_Z6 = np.array([i for i in range(len(species_names)) if 'Z6' in species_names[i]])

    P1 = np.nansum(mean_biomass[:,id_P1],axis=1)
    P2 = np.nansum(mean_biomass[:,id_P2],axis=1)
    P3 = np.nansum(mean_biomass[:,id_P3],axis=1)
    P4 = np.nansum(mean_biomass[:,id_P4],axis=1)
    P5 = np.nansum(mean_biomass[:,id_P5],axis=1)
    P6 = np.nansum(mean_biomass[:,id_P6],axis=1)
    P7 = np.nansum(mean_biomass[:,id_P7],axis=1)
    P8 = np.nansum(mean_biomass[:,id_P8],axis=1)
    P9 = np.nansum(mean_biomass[:,id_P9],axis=1)
    Z3 = np.nansum(mean_biomass[:,id_Z3],axis=1)
    Z4 = np.nansum(mean_biomass[:,id_Z4],axis=1)
    Z5 = np.nansum(mean_biomass[:,id_Z5],axis=1)
    Z6 = np.nansum(mean_biomass[:,id_Z6],axis=1)

    species_names = np.array(ds['paper_species'][:])
    species_names = species_names[count >= ny]

    #how many species to label
    nlabels = 5
    for ispec,spe_name in enumerate(species_names):
        if ispec < nlabels:
            axs[0].plot(time,mean_biomass[:,ispec],label=spe_name,alpha=0.8)
        else:
            axs[0].plot(time,mean_biomass[:,ispec],alpha=0.3)
    axs[1].plot(time,P1,label='P1',alpha=0.8,c='b')
    axs[1].plot(time,P2,label='P2',alpha=0.8,c='g')
    axs[1].plot(time,P3,label='P3',alpha=0.8,c='r')
    axs[1].plot(time,P4,label='P4',alpha=0.8,c='c')
    axs[1].plot(time,P5,label='P5',alpha=0.8,c='m')
    axs[1].plot(time,P6,label='P6',alpha=0.8,c='y')
    axs[1].plot(time,P7,label='P7',alpha=0.8,c='k')
    axs[1].plot(time,P8,label='P8',alpha=0.8,c='orange')
    axs[1].plot(time,P9,label='P9',alpha=0.8,c='purple')
    axs[2].plot(time,Z3,label='Z3',alpha=0.8,c='b')
    axs[2].plot(time,Z4,label='Z4',alpha=0.8,c='g')
    axs[2].plot(time,Z5,label='Z5',alpha=0.8,c='r')
    axs[2].plot(time,Z6,label='Z6',alpha=0.8,c='c')

    for iax,ax in enumerate(axs):
        ax.set_ylabel('biomass $[mgC/m^3]$')
#        ax.set_yscale('log')
        ax.legend()
    fig.tight_layout()
    plt.show()
    fig.savefig('prova_'+ncname[:-3]+'.png')

            



