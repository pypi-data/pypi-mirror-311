import numpy as np
#import netCDF4 as nc
import COMSTABPY
import matplotlib.pyplot as plt
import xarray as xr

#load the stability analysis module
stb = COMSTABPY.comstab()


ncnames = ['result_surface_winter.nc','result_surface_summer.nc','result_surface_year.nc','result_deep_winter.nc','result_deep_summer.nc','result_deep_year.nc']

#communities names: phytoplankton, zooplankton, total(B+P+Z)
communities = ['P','Z','TOT']
labels = np.array(['s_w_P','s_w_Z','s_w_TOT','s_s_P','s_s_Z','s_s_TOT','s_y_P','s_y_Z','s_y_TOT','d_w_P','d_w_Z','d_w_TOT','d_s_P','d_s_Z','d_s_TOT','d_y_P','d_y_Z','d_y_TOT'])

markers = ['o','^','*']
colors = ['b','r','g']

cvs_arr  = np.zeros((len(labels),32,4)) #32 is maximum depth layers number
stab_arr = np.zeros((len(labels),32,4))
rela_arr = np.zeros((len(labels),32,3))
H_arr    = np.zeros((len(labels),32,2)) #eveness of mean and variance
depths   = np.zeros((len(labels),32))

meanflag = False # False # True if you want to compute the annual mean of the data

for inc,ncname in enumerate(ncnames):
    # Load the data
    ds = xr.open_dataset(ncname)
    
    if meanflag:
        ds = ds.groupby('time.year').mean('time')
        time = np.array(ds['year'][:])
    else:
        time = np.array(ds['time'][:])    

    for icomm,community in enumerate(communities):
        data = np.array(ds[community])[:,:,:]

        if 'surface' in ncname:
            #concatenate ds.depth with nans to fill the array
            depths[inc*3+icomm,:] = np.concatenate((ds.depth.values,np.full(32-len(ds.depth.values),np.nan)))
        else:
            depths[inc*3+icomm,:] = ds.depth.values

        for idepth in range(data.shape[2]):
#           print(idepth)
            try:
                data_ny = data[~mask,:,idepth]
                ny = 5
                count = np.count_nonzero(~np.isnan(data_ny), axis=1)
                data_ny = data_ny[count >= ny]
                H_arr[inc*3+icomm,idepth,0]  = stb.eveness(np.nanmean(data_ny[:,:],axis=1))
                H_arr[inc*3+icomm,idepth,1]  = stb.eveness(np.nanstd(data_ny[:,:],axis=1))
            except:
                H_arr[inc*3+icomm,idepth] = np.array([np.nan,np.nan])

            try:
                #remove rows with all nan values of temporal axis of data
                mask = np.isnan(data[:,:,idepth]).all(axis=1)
                result = stb.partition(data[~mask,:,idepth],ny=5,stamp=False)
                cvs_arr[inc*3+icomm,idepth]  = result['CVs']
                stab_arr[inc*3+icomm,idepth] = result['Stabilization']
                rela_arr[inc*3+icomm,idepth] = result['Relative']
#               data_ny = data[~mask,:,idepth]
#               ny = 5
#               count = np.count_nonzero(~np.isnan(data_ny), axis=1)
#               data_ny = data_ny[count >= ny]
#               H_arr[inc*3+icomm,idepth,0]  = stb.eveness(np.nanmean(data_ny[:,:],axis=1))
#               H_arr[inc*3+icomm,idepth,1]  = stb.eveness(np.nanstd(data_ny[:,:],axis=1))
            except:
                cvs_arr[inc*3+icomm,idepth]  = np.array([np.nan,np.nan,np.nan,np.nan])
                stab_arr[inc*3+icomm,idepth] = np.array([np.nan,np.nan,np.nan,np.nan])
                rela_arr[inc*3+icomm,idepth] = np.array([np.nan,np.nan,np.nan])
#               H_arr[inc*3+icomm,idepth] = np.array([np.nan,np.nan])
                continue
 
        if 'surface' in ncname:
            cvs_arr[inc*3+icomm,26:] = np.array([np.nan,np.nan,np.nan,np.nan])
            stab_arr[inc*3+icomm,26:] = np.array([np.nan,np.nan,np.nan,np.nan])
            rela_arr[inc*3+icomm,26:] = np.array([np.nan,np.nan,np.nan])
            H_arr[inc*3+icomm,26:] = np.array([np.nan,np.nan])

#plot of CVc vs for all communities and depths, divideded in three plots for summer, winter and year

fig,axs = plt.subplots(1,3,figsize=(10,10))
for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'winter' in ncname:
            axs[0].scatter(cvs_arr[iax*3+icomm,:,3], depths[iax*3+icomm], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
        if 'summer' in ncname:
            axs[1].scatter(cvs_arr[iax*3+icomm,:,3], depths[iax*3+icomm], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'year' in ncname:
            axs[2].scatter(cvs_arr[iax*3+icomm,:,3], depths[iax*3+icomm], c=colors[2], marker=markers[icomm], alpha=0.5)

#axs[0].legend()
axs[0].set_ylabel('Depth (m)')
for ax in axs:
    ax.set_xlabel('$CV_c$')
    ax.axhline(-10, c='k', ls='--')
#    ax.set_xscale('log')
    ax.set_xlim(0.1,2.5)
    ax.set_ylim(-100,0)

pl = axs[0].scatter([],[], s=100,  marker='o', color='k')
zl = axs[0].scatter([],[], s=100,  marker='^', color='k')
tl = axs[0].scatter([],[], s=100,  marker='*', color='k')
axs[0].legend((pl,zl,tl),
				('P', 'Z', 'TOT'),
				scatterpoints=1,
				#loc='center left',
				ncol=1,
				fontsize=10,
				frameon=False,
#				title='Total\nStabilization',
				borderpad=1.5,
				#bbox_to_anchor=(0.4,0.95)
                loc = 'lower right')

plt.show()
fig.savefig('CVc_vs_depth.png')

#plot of CVe
fig,axs = plt.subplots(1,3,figsize=(10,10))

for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'winter' in ncname:
            axs[0].scatter(cvs_arr[iax*3+icomm,:,0], depths[iax*3+icomm], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
        if 'summer' in ncname:
            axs[1].scatter(cvs_arr[iax*3+icomm,:,0], depths[iax*3+icomm], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'year' in ncname:
            axs[2].scatter(cvs_arr[iax*3+icomm,:,0], depths[iax*3+icomm], c=colors[2], marker=markers[icomm], alpha=0.5)

#axs[0].legend()
axs[0].set_ylabel('Depth (m)')
for ax in axs:
    ax.set_xlabel('$CV_e$')
    ax.axhline(-10, c='k', ls='--')
#    ax.set_xscale('log')
    ax.set_xlim(0.1,2.5)
    ax.set_ylim(-100,0)

axs[0].legend((pl,zl,tl),
				('P', 'Z', 'TOT'),
				scatterpoints=1,
				#loc='center left',
				ncol=1,
				fontsize=10,
				frameon=False,
#				title='Total\nStabilization',
				borderpad=1.5,
				#bbox_to_anchor=(0.4,0.95)
                loc = 'lower right')

plt.show()

fig.savefig('CVe_vs_depth.png')

#plot of Delta
fig,axs = plt.subplots(1,3,figsize=(10,10))

for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'summer' in ncname:
            axs[1].scatter(stab_arr[iax*3+icomm,:,1], depths[iax*3+icomm], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'winter' in ncname:
            axs[0].scatter(stab_arr[iax*3+icomm,:,1], depths[iax*3+icomm], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
        if 'year' in ncname:
            axs[2].scatter(stab_arr[iax*3+icomm,:,1], depths[iax*3+icomm], c=colors[2], marker=markers[icomm], alpha=0.5)

#axs[0].legend()
axs[0].set_ylabel('Depth (m)')
for ax in axs:
    ax.set_xlabel(r'$\Delta$')
    ax.axhline(-10, c='k', ls='--')
    ax.axvline(1.0, c='k', ls='-', alpha=0.7, zorder=0)
    ax.set_xlim(0.25,1.5)
    ax.set_ylim(-100,0)

axs[0].legend((pl,zl,tl),
				('P', 'Z', 'TOT'),
				scatterpoints=1,
				#loc='center left',
				ncol=1,
				fontsize=10,
				frameon=False,
#				title='Total\nStabilization',
				borderpad=1.5,
				#bbox_to_anchor=(0.4,0.95)
                loc = 'lower left')

plt.show()

fig.savefig('Delta_vs_depth.png')

#plot of psi
fig,axs = plt.subplots(1,3,figsize=(10,10))

for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'summer' in ncname:
            axs[1].scatter(stab_arr[iax*3+icomm,:,2], depths[iax*3+icomm], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'winter' in ncname:
            axs[0].scatter(stab_arr[iax*3+icomm,:,2], depths[iax*3+icomm], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
        if 'year' in ncname:
            axs[2].scatter(stab_arr[iax*3+icomm,:,2], depths[iax*3+icomm], c=colors[2], marker=markers[icomm], alpha=0.5)

#axs[0].legend()
axs[0].set_ylabel('Depth (m)')
for ax in axs:
    ax.set_xlabel('$\psi$')
    ax.set_xlim(0.5,1.2)
    ax.axhline(-10, c='k', ls='--')
    ax.set_ylim(-100,0)

axs[0].legend((pl,zl,tl),
				('P', 'Z', 'TOT'),
				scatterpoints=1,
				#loc='center left',
				ncol=1,
				fontsize=10,
				frameon=False,
#				title='Total\nStabilization',
				borderpad=1.5,
				#bbox_to_anchor=(0.4,0.95)
                loc = 'lower left')

plt.show()

fig.savefig('psi_vs_depth.png')

#plot of omega
fig,axs = plt.subplots(1,3,figsize=(10,10))

for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'summer' in ncname:
            axs[1].scatter(stab_arr[iax*3+icomm,:,3], depths[iax*3+icomm], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'winter' in ncname:
            axs[0].scatter(stab_arr[iax*3+icomm,:,3], depths[iax*3+icomm], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
        if 'year' in ncname:
            axs[2].scatter(stab_arr[iax*3+icomm,:,3], depths[iax*3+icomm], c=colors[2], marker=markers[icomm], alpha=0.5)

#axs[0].legend()
axs[0].set_ylabel('Depth (m)')
for ax in axs:
    ax.set_xlabel(r'$\omega$')
    ax.set_xlim(0.5,1.2)
    ax.axhline(-10, c='k', ls='--')
    ax.set_ylim(-100,0)

axs[0].legend((pl,zl,tl),
				('P', 'Z', 'TOT'),
				scatterpoints=1,
				#loc='center left',
				ncol=1,
				fontsize=10,
				frameon=False,
#				title='Total\nStabilization',
				borderpad=1.5,
				#bbox_to_anchor=(0.4,0.95)
                loc = 'lower left')
                

plt.show()

fig.savefig('omega_vs_depth.png')

#plot of eveness of mean
fig,axs = plt.subplots(1,3,figsize=(10,10))

for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'summer' in ncname:
            axs[1].scatter(H_arr[iax*3+icomm,:,0], depths[iax*3+icomm], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'winter' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], depths[iax*3+icomm], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
        if 'year' in ncname:
            axs[2].scatter(H_arr[iax*3+icomm,:,0], depths[iax*3+icomm], c=colors[2], marker=markers[icomm], alpha=0.5)

#axs[0].legend()
axs[0].set_ylabel('Depth (m)')
for ax in axs:
    ax.set_xlabel(r'$H_{\mu}$')
    ax.set_xlim(0.4,1.0)
    ax.set_ylim(-100,0)
    ax.axhline(-10, c='k', ls='--')

axs[0].legend((pl,zl,tl),
                                ('P', 'Z', 'TOT'),
                                scatterpoints=1,
                                #loc='center left',
                                ncol=1,
                                fontsize=10,
                                frameon=False,
#                               title='Total\nStabilization',
                                borderpad=1.5,
                                #bbox_to_anchor=(0.4,0.95)
                loc = 'lower right')
plt.show()

fig.savefig('H_mu_vs_depth.png')

#plot of eveness of standard deviation
fig,axs = plt.subplots(1,3,figsize=(10,10))

for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'summer' in ncname:
            axs[1].scatter(H_arr[iax*3+icomm,:,1], depths[iax*3+icomm], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'winter' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,1], depths[iax*3+icomm], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
        if 'year' in ncname:
            axs[2].scatter(H_arr[iax*3+icomm,:,1], depths[iax*3+icomm], c=colors[2], marker=markers[icomm], alpha=0.5)

#axs[0].legend()
axs[0].set_ylabel('Depth (m)')
for ax in axs:
    ax.set_xlabel(r'$H_{\sigma}$')
    ax.set_xlim(0.4,1.0)
    ax.set_ylim(-100,0)
    ax.axhline(-10, c='k', ls='--')

axs[0].legend((pl,zl,tl),
                                ('P', 'Z', 'TOT'),
                                scatterpoints=1,
                                #loc='center left',
                                ncol=1,
                                fontsize=10,
                                frameon=False,
#                               title='Total\nStabilization',
                                borderpad=1.5,
                                #bbox_to_anchor=(0.4,0.95)
                loc = 'lower right')


plt.show()
fig.savefig('H_sigma_vs_depth.png')

#plot of delta against eveness of mean and standard deviation
fig,axs = plt.subplots(1,2,figsize=(10,5))

for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'summer' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], stab_arr[iax*3+icomm,:,1], c=colors[1], marker=markers[icomm], alpha=0.5)
            axs[1].scatter(H_arr[iax*3+icomm,:,1], stab_arr[iax*3+icomm,:,1], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'winter' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], stab_arr[iax*3+icomm,:,1], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
            axs[1].scatter(H_arr[iax*3+icomm,:,1], stab_arr[iax*3+icomm,:,1], c=colors[0], marker=markers[icomm], alpha=0.5)
        if 'year' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], stab_arr[iax*3+icomm,:,1], c=colors[2], marker=markers[icomm], alpha=0.5)
            axs[1].scatter(H_arr[iax*3+icomm,:,1], stab_arr[iax*3+icomm,:,1], c=colors[2], marker=markers[icomm], alpha=0.5)
axs[0].set_ylabel(r'$\Delta$')
axs[0].set_xlabel(r'$H_{\mu}$')
axs[1].set_xlabel(r'$H_{\sigma}$')

axs[0].legend((pl,zl,tl),
                                ('P', 'Z', 'TOT'),
                                scatterpoints=1,
                                #loc='center left',
                                ncol=1,
                                fontsize=10,
                                frameon=False,
#                               title='Total\nStabilization',
                                borderpad=1.5,
                                #bbox_to_anchor=(0.4,0.95)
                loc = 'lower right')
#set log sclae
#axs[0].set_xscale('log')
#axs[1].set_xscale('log')
#axs[0].set_yscale('log')
#axs[1].set_yscale('log')

for ax in axs:
    ax.axhline(1, c='k', ls='--')

plt.show()
fig.savefig('H_Delta.png')

#plot of psi against eveness of mean and standard deviation
fig,axs = plt.subplots(1,2,figsize=(10,5))

for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'summer' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], stab_arr[iax*3+icomm,:,2], c=colors[1], marker=markers[icomm], alpha=0.5)
            axs[1].scatter(H_arr[iax*3+icomm,:,1], stab_arr[iax*3+icomm,:,2], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'winter' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], stab_arr[iax*3+icomm,:,2], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
            axs[1].scatter(H_arr[iax*3+icomm,:,1], stab_arr[iax*3+icomm,:,2], c=colors[0], marker=markers[icomm], alpha=0.5)
        if 'year' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], stab_arr[iax*3+icomm,:,2], c=colors[2], marker=markers[icomm], alpha=0.5)
            axs[1].scatter(H_arr[iax*3+icomm,:,1], stab_arr[iax*3+icomm,:,2], c=colors[2], marker=markers[icomm], alpha=0.5)
axs[0].set_ylabel(r'$\psi$')
axs[0].set_xlabel(r'$H_{\mu}$')
axs[1].set_xlabel(r'$H_{\sigma}$')

axs[0].legend((pl,zl,tl),
                                ('P', 'Z', 'TOT'),
                                scatterpoints=1,
                                #loc='center left',
                                ncol=1,
                                fontsize=10,
                                frameon=False,
#                               title='Total\nStabilization',
                                borderpad=1.5,
                                #bbox_to_anchor=(0.4,0.95)
                loc = 'lower right')
#set log sclae
#axs[0].set_xscale('log')
#axs[1].set_xscale('log')
#axs[0].set_yscale('log')
#axs[1].set_yscale('log')

for ax in axs:
    ax.axhline(1, c='k', ls='--')

plt.show()
fig.savefig('H_psi.png')

#plot of omega against eveness of mean and standard deviation
fig,axs = plt.subplots(1,2,figsize=(10,5))

for iax,ncname in enumerate(ncnames):
    for icomm,community in enumerate(communities):
        if 'summer' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], stab_arr[iax*3+icomm,:,3], c=colors[1], marker=markers[icomm], alpha=0.5)
            axs[1].scatter(H_arr[iax*3+icomm,:,1], stab_arr[iax*3+icomm,:,3], c=colors[1], marker=markers[icomm], alpha=0.5)
        if 'winter' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], stab_arr[iax*3+icomm,:,3], c=colors[0], marker=markers[icomm], alpha=0.5, label=community)
            axs[1].scatter(H_arr[iax*3+icomm,:,1], stab_arr[iax*3+icomm,:,3], c=colors[0], marker=markers[icomm], alpha=0.5)
        if 'year' in ncname:
            axs[0].scatter(H_arr[iax*3+icomm,:,0], stab_arr[iax*3+icomm,:,3], c=colors[2], marker=markers[icomm], alpha=0.5)
            axs[1].scatter(H_arr[iax*3+icomm,:,1], stab_arr[iax*3+icomm,:,3], c=colors[2], marker=markers[icomm], alpha=0.5)
axs[0].set_ylabel(r'$\omega$')
axs[0].set_xlabel(r'$H_{\mu}$')
axs[1].set_xlabel(r'$H_{\sigma}$')

axs[0].legend((pl,zl,tl),
                                ('P', 'Z', 'TOT'),
                                scatterpoints=1,
                                #loc='center left',
                                ncol=1,
                                fontsize=10,
                                frameon=False,
#                               title='Total\nStabilization',
                                borderpad=1.5,
                                #bbox_to_anchor=(0.4,0.95)
                loc = 'lower right')
#set log sclae
#axs[0].set_xscale('log')
#axs[1].set_xscale('log')
#axs[0].set_yscale('log')
#axs[1].set_yscale('log')

for ax in axs:
    ax.axhline(1, c='k', ls='--')

plt.show()
fig.savefig('H_omega.png')
