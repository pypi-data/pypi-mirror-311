import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import sys
import pandas as pd
#chose depth layer
layer = 'surface'
layer = 'deep'

if layer == 'surface':
    ncnames  = ['result_surface_winter.nc','result_surface_summer.nc','result_surface_year.nc']
    z_layers = [0,4,8]
    z_layers = [0]
#deep
if layer == 'deep':
    ncnames  = ['result_deep_winter.nc','result_deep_summer.nc','result_deep_year.nc']
    z_layers = [25,50,75]
    z_layers = [0]

community = 'TOT'
colors = ['b','r','g']

ny = 5

#import network metrics from csv file
df = pd.read_csv('NetworkMetrics.csv')
nodes = df['nodes']
EC    = df['EigenevectorCentrality']
BC    = df['BetweenessCentrality']
ND    = df['NodeDegree']
L     = df['LongestPath'][1:]

fig,axs = plt.subplots(3,3,figsize=(10,10))
for inc,ncname in enumerate(ncnames):
    # Load the data
    ds = xr.open_dataset(ncname)
    #compute the mean of ds such that the mean is computed over the same days of all the years and the output is a year long timeseries
    ds = ds.groupby('time.dayofyear').mean('time')
    time = np.array(ds['dayofyear'][:])    

    #get the indexes of the z_layers
    depth = ds.depth.values
#   z_indexes = np.zeros(3,dtype=int)
#   for iz,z_layer in enumerate(z_layers):
#       z_indexes[iz] = np.argmin(np.abs(depth+z_layer))
#   for iax,iz in enumerate(z_indexes):
    #mean biomass (time,species)
    mean_biomass = np.mean(ds[community][:,:,:],axis=2)
    EC_weighted = np.zeros_like(EC,dtype=float)
    BC_weighted = np.zeros_like(BC,dtype=float)
    ND_weighted = np.zeros_like(ND,dtype=float)
    if community == 'TOT':
        species_names = np.array(ds['species'][0,:])
    else:
        species_names = np.array(ds['species'+community][0,:])
    count = np.count_nonzero(~np.isnan(mean_biomass), axis=0)
    mean_biomass[:,count < ny] = np.nan
    #compute the mean of the biomass
    mean_biomass = np.nanmean(mean_biomass,axis=0)
    mean_biomass = mean_biomass/np.nansum(mean_biomass)

    #weight the metric with the biomass
    for inode,node in enumerate(nodes):
        for ispec,spec_name in enumerate(species_names):
            if node in spec_name:
                EC_weighted[inode] = EC[inode]*mean_biomass[ispec]
                BC_weighted[inode] = BC[inode]*mean_biomass[ispec]
                ND_weighted[inode] = ND[inode]*mean_biomass[ispec]
    #plot the network metrics
    x = np.array(df.index)
    axs[inc,0].scatter(x[1:],EC_weighted[1:],c=colors[inc],s=9)
    axs[inc,0].set_title('Eigenvector Centrality')
    axs[inc,1].scatter(x[1:],BC_weighted[1:],c=colors[inc],s=9)
    axs[inc,1].set_title('Betweeness Centrality')
    axs[inc,2].scatter(x[1:],ND_weighted[1:],c=colors[inc],s=9)
    axs[inc,2].set_title('Node Degree')
    for inode,node in enumerate(nodes):
        if node == 'P1_20' or node == 'Z5_15':
            axs[inc,0].scatter(x[inode],EC_weighted[inode],c=colors[inc],marker='*',s=50)
            axs[inc,1].scatter(x[inode],BC_weighted[inode],c=colors[inc],marker='*',s=50)
            axs[inc,2].scatter(x[inode],ND_weighted[inode],c=colors[inc],marker='*',s=50)

    axs[inc,0].set_yscale('log')
    axs[inc,1].set_yscale('log')
    axs[inc,2].set_yscale('log')
for iax,ax in enumerate(axs.ravel()):
    ax.set_xticks(range(0,len(nodes[1:]),int(len(nodes[1:])/20)))
    ax.set_xticklabels(nodes[1:][::int(len(nodes[1:])/20)],rotation=90)


            
fig.tight_layout()
plt.show()
#    fig.savefig('mean_biomass_'+ncname[:-3]+'.png')

#plot the center of gravity along the water column

fig,axs = plt.subplots(figsize=(5,7))
for inc,ncname in enumerate(ncnames):
    # Load the data
    ds = xr.open_dataset(ncname)
    #compute the mean in time of ds

    depth = ds.depth.values
    for iz,z in enumerate(depth):
        mean_biomass = ds.TOT[:,:,iz]
        count = np.count_nonzero(~np.isnan(mean_biomass), axis=1)
        mean_biomass[count < ny,:] = np.nan
        mean_biomass = np.nanmean(mean_biomass,axis=1)
        extincted = np.isnan(mean_biomass)
        L_now = L[extincted]
        CG = np.nansum(L_now) / ( len(L_now) * np.max(L_now) )
        axs.scatter(CG,z,c=colors[inc],s=9,marker='*') 

axs.set_xlabel('Center of Gravity')
axs.set_ylabel('Depth [m]')
fig.tight_layout()
plt.show()
fig.savefig('center_of_gravity.png',dpi=600)