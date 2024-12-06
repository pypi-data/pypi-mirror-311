import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import sys
from scipy.stats import pearsonr


#chose depth layer
layer = 'surface'
layer = 'deep'

if layer == 'surface':
    ncnames  = ['result_surface_winter.nc','result_surface_summer.nc','result_surface_year.nc']
    z_layers = [0,4,8]
#deep
if layer == 'deep':
    ncnames  = ['result_deep_winter.nc','result_deep_summer.nc','result_deep_year.nc']
    z_layers = [25,50,75]

communities = ['P','Z','TOT']
markers = np.array(['o','^','*'])
colors = np.array(['b','r','g'])

ny = 5

for inc,ncname in enumerate(ncnames):
    # Load the data
    ds = xr.open_dataset(ncname)
    fig,axs = plt.subplots(3,3,figsize=(10,10))

    #get the indexes of the z_layers
    depth = ds.depth.values
    z_indexes = np.zeros(3,dtype=int)
    for iz,z_layer in enumerate(z_layers):
        z_indexes[iz] = np.argmin(np.abs(depth+z_layer))
    for icomm,community in enumerate(communities):
        for iax,iz in enumerate(z_indexes):
            #mean biomass (species,time,depth)
            data = ds[community][:,:,iz]
            count = np.count_nonzero(~np.isnan(data), axis=1)
            #remove species appearing in fewer than "ny" timesteps
            data = data[count >= ny]
            mean_biomass = np.nanmean(data,axis=1)
            cv_biomass   = np.nanstd(data,axis=1)/np.nanmean(data,axis=1)
            var_biomass  = np.nanvar(data,axis=1)
            #subtitute zeros in cv_biomass with nan
            mean_biomass[cv_biomass==0] = np.nan
            var_biomass[cv_biomass==0] = np.nan
            cv_biomass[cv_biomass==0] = np.nan
            mask = np.zeros_like(mean_biomass,dtype=bool)
#           if community == 'Z' and 'summer' in ncname:# and layer == 'surface':
            if False:
                #remove elements in cv_biomass and mean_biomass with cv_biomass>1
                mask = cv_biomass>1.0
                mean = mean_biomass[~mask]
                var  = var_biomass[~mask]
                cv   = cv_biomass[~mask]
                TPL = np.polyfit(np.log10(mean[~np.isnan(mean)]), np.log10(cv[~np.isnan(cv)]), 1)
                _, p = pearsonr(np.log10(mean[~np.isnan(mean)]), np.log10(cv[~np.isnan(cv)]))

                meansum = np.nanmean(np.nansum(data,axis=0))
                varsum = np.nanvar(np.nansum(data,axis=0))
                cvsum = np.sqrt(varsum)/meansum
                CVe = 10**TPL[1] * (meansum / n)**TPL[0]
                sumsd = np.nansum(np.sqrt(var))
                CVtilde = sumsd / meansum
#               sys.exit()
#            if community == 'Z':
#                if 'year' in ncname:
#                   sys.exit()
            else:
                TPL = np.polyfit(np.log10(mean_biomass[~np.isnan(mean_biomass)]), np.log10(cv_biomass[~np.isnan(cv_biomass)]), 1)
            #TPL = np.polyfit(np.log10(mean_biomass[~mask]), np.log10(cv_biomass[~mask]), 1)
                r, p = pearsonr(np.log10(mean_biomass[~np.isnan(mean_biomass)]), np.log10(cv_biomass[~np.isnan(cv_biomass)]))
            #_, p = pearsonr(np.log10(mean_biomass[~mask]), np.log10(cv_biomass[~mask]))
                meansum = np.nanmean(np.nansum(data,axis=0))
                varsum = np.nanvar(np.nansum(data,axis=0))
                cvsum = np.sqrt(varsum)/meansum
                n = ds[community][:,:,iz].shape[0]
                CVe = 10**TPL[1] * (meansum / n)**TPL[0]
                sumsd = np.nansum(np.sqrt(var_biomass))
                CVtilde = sumsd / meansum

            #axs[icomm,iax].scatter(np.log10(mean_biomass[~mask]),np.log10(cv_biomass[~mask]),marker=markers[icomm],c=colors[inc],alpha=0.7)
            #axs[icomm,iax].scatter(np.log10(mean_biomass[mask]),np.log10(cv_biomass[mask]),marker=markers[icomm],c=colors[inc],alpha=0.2)
            #axs[icomm,iax].plot(np.log10(mean_biomass),TPL[0]*np.log10(mean_biomass)+TPL[1],c='k',label='b='+str(round((TPL[0]+1)*2,2))+', p-value='+str(round(p,3)))
            #plot data and then set log scale
            axs[icomm,iax].scatter(mean_biomass[~mask],cv_biomass[~mask],marker=markers[icomm],c=colors[inc],alpha=0.7)
            axs[icomm,iax].scatter(mean_biomass[mask],cv_biomass[mask],marker=markers[icomm],c=colors[inc],alpha=0.2)
            axs[icomm,iax].plot(mean_biomass,np.power(mean_biomass,TPL[0])*(10**TPL[1]),c='k',label='b='+str(round((TPL[0]+1)*2,2))+', p-value='+str(round(p,3))+', r='+str(round(r,2)))

            #axs[icomm,iax].axhline(np.log10(CVtilde),c='k',ls='--',zorder=0,alpha=0.5)
            #axs[icomm,iax].axvline(np.log10(meansum/n),c='k',ls=':',zorder=2)
            #axs[icomm,iax].axhline(np.log10(CVe),c='k',ls=':',zorder=1)
            axs[icomm,iax].axhline(CVtilde,c='k',ls='--',zorder=0,alpha=0.5)
            axs[icomm,iax].axvline(meansum/n,c='k',ls=':',zorder=2)
            axs[icomm,iax].axhline(CVe,c='k',ls=':',zorder=1)
            
            axs[icomm,iax].set_xscale('log')
            axs[icomm,iax].set_yscale('log')
            
            
            axs[icomm,iax].set_title(community+' at '+str(round(depth[iz], 3))[:4]+' m')#+' '+str(round(CVe,2))+' '+str(round(cvsum,2)))
            #axs[icomm,iax].set_xlabel('log10(mean biomass)')
            #axs[icomm,iax].set_ylabel('log10(cv biomass)')
            if community == 'TOT':
                axs[icomm,iax].set_xlabel(r'$\mu_i$ mean biomass')
            axs[icomm,iax].set_ylabel(r'$CV_i$')
            axs[icomm,iax].legend(loc='lower center')
    fig.tight_layout()
    plt.show()
    fig.savefig('taylor_'+ncname[:-3]+'.png')

            



