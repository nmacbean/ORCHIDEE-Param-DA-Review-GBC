#!/usr/local/install/python-2.7.5/bin/ipython

"""
Script for plotting mean annual GPP posterior and difference global maps from MacBean et al. (2018) and Bacour et al. (2019) SIF optimization papers.
"""
__author__ = "Natasha MacBean"
__version__ = "1.0 (07.22.2021)"
__email__ = "nlmacbean@gmail.com"


import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy
import sys


#--------------------------------
#---------- FUNCTIONS -----------
#--------------------------------

def _get_var(infile, var):
    """
    reads all data of a certain variable from a netcdf file and returns it.
    """

    f=nc.Dataset(infile,'r')
    out_var=f.variables[var][:]
    f.close()

    return out_var
    

def _get_Lat_Lon(infile):
    """
    gets the latitude and longitude values of a file - OUTPUT: lat, lon
    """

    f=nc.Dataset(infile,'r')

    if 'lat' in f.variables.keys(): lt=f.variables['lat']
    if 'latitude' in f.variables.keys(): lt=f.variables['latitude']
    if 'y' in f.variables.keys(): lt=f.variables['y']
    if 'nav_lat' in f.variables.keys(): lt=f.variables['nav_lat']

    if 'lon' in f.variables.keys(): ln=f.variables['lon']
    if 'longitude' in f.variables.keys(): ln=f.variables['longitude']
    if 'nav_lon' in f.variables.keys(): ln=f.variables['nav_lon']

    Lat=lt[:]
    Lon=ln[:]

    f.close()

    return Lat, Lon




#---------------------------
#---------- MAIN -----------
#---------------------------

# -
# - Set-up
# -
infile = 'macbean2018_bacour2019_global_GPP.nc'
var_names = ['macbean2018_SIFoptim_meanAnnGPP_Prior', 'macbean2018_SIFoptim_meanAnnGPP_Post', \
	     'bacour2019_SIFoptim_meanAnnGPP_Prior', 'bacour2019_SIFoptim_meanAnnGPP_Post']
nmaps = len(var_names)
outdir = './'


# - 
# - get lat and lon and set-up data array
# -
lat, lon = _get_Lat_Lon(infile)
mean_ann_gpps = np.zeros((nmaps, len(lat), len(lon)))


# -
# - get data
# -
for nvar, var in enumerate(var_names):
   mean_ann_gpps[nvar,:,:] = _get_var(infile, var)


# -
# - get difference maps
# -
diff_mean_ann_gpps = np.zeros((nmaps/2, len(lat), len(lon)))
diff_mean_ann_gpps[0] = mean_ann_gpps[1,:,:] - mean_ann_gpps[0,:,:]
diff_mean_ann_gpps[1] = mean_ann_gpps[3,:,:] - mean_ann_gpps[2,:,:]


# - 
# - plot global maps
# -

# - set-up plot
f = plt.figure(figsize=(8,3.5))#, sharex=True, sharey=True)
plt.subplots_adjust(left=0.01, right=0.85, bottom=0.02, top=0.97, wspace=0.05, hspace=0.05)
crs = ccrs.PlateCarree()
titles = ['GOME-2 SIF + Linear SIF-GPP model', 'OCO-2 SIF + Process-based SIF-GPP model']
cbar1_axes = f.add_axes([0.87, 0.54, 0.02, 0.4])		# [left, bottom, width, height]
cbar2_axes = f.add_axes([0.87, 0.05, 0.02, 0.4])		# [left, bottom, width, height]

# - loop over subplots
for nmap in range(nmaps):
	
	# - set-up plot
	ax = f.add_subplot( nmaps/2, nmaps/2, nmap+1, projection=crs )
	ax.set_global()
	ax.coastlines()
	ax.gridlines(alpha=0.3, xlocs=[-180,-120,-60,0,60,120,180], ylocs=[-60,-30,0,30,60,90]) #draw_labels=True, alpha=0.5, xlocs=[-180,-120,-60,0,60,120,180], ylocs=[-90,-60,-30,0,30,60,90])
	extents = [-180, 180, -60, 90]
	ax.set_extent(extents)

	# - get grid lats and lons
	gridlons, gridlats = np.meshgrid(lon, lat)

	# - add data
	if nmap <= 1: 
		data = np.ma.masked_where(mean_ann_gpps[nmap+2,:,:]==0, mean_ann_gpps[nmap+2,:,:])
		cmap = mpl.cm.viridis
		vmin, vmax = 0, 3.5
		bounds = np.linspace(vmin, vmax, 15)
		norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)
	else:
		data = np.ma.masked_where(diff_mean_ann_gpps[nmap-2,:,:]==0, diff_mean_ann_gpps[nmap-2,:,:])
		cmap = mpl.cm.RdBu
		vmin, vmax = -1.5, 1.5
		bounds = np.linspace(vmin, vmax, 13)
		norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)
	im1 = plt.pcolormesh( gridlons, gridlats, data, cmap=cmap, norm=norm, vmin=vmin, vmax=vmax)
		
	
	# - colorbar
	if nmap == 1:
		cbar = plt.colorbar(cax=cbar1_axes, extend='both').set_label(label='Posterior mean annual\nGPP (kgCm$^{-2}$yr${-1}$)', size=9.5)
	if nmap == 3:
		cbar = plt.colorbar(cax=cbar2_axes, extend='both').set_label(label='Mean ann GPP difference\n(post-prior) (kgCm$^{-2}$yr${-1}$)', size=9.5)
	#if nmap == 1 or nmap == 3: cbar.ax.tick_params(labelsize=5)
	
	# - add title
	if nmap <=1: 
		ax.set_title(titles[nmap], fontsize=11, loc='center')
	
		
# - save plot
#plt.show()
outfile = outdir + 'macbean2018_bacour2019_global_gpp_map_plot.pdf'
plt.savefig(outfile)
