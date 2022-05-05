#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 14:35:01 2019

@author: nraoult
"""

import matplotlib
matplotlib.use('Agg')
import netCDF4
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches


def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())


def nash(targets, predictions):
    eps = np.sum((predictions - targets) ** 2)/np.sum((targets-np.nanmean(targets))**2)
    #return 1-eps
    return eps



loc = "./"
sites = pd.read_table("experiment_sites.txt",sep=",",index_col=False)

table_lai_rmse = np.zeros((6,12))

isite = 0 
for row in sites.head(12).itertuples():
    site      = row.Site
    print(site)
    
    nclai  = netCDF4.Dataset(sorted(glob.glob(loc+'tmp_lai/OptLAI_'+site+'_GA_lai/output.nc'))[-1])
    laiobs = nclai["data_site0_var0"][0,:]
    laiold = nclai["data_site0_var0"][1,:]
    nclai.close()
    
    ncelai = netCDF4.Dataset(sorted(glob.glob(loc+'tmp_elai/OptLAI_'+site+'_GA_elai/output.nc'))[-1])
    elainew = ncelai["data_site0_var0"][3,:]
    ncelai.close()
    
    ncnlai = netCDF4.Dataset(sorted(glob.glob(loc+'tmp_lainorm/OptLAI_'+site+'_GA_lainorm_post/output.nc'))[-1])
    lainorm = ncnlai["data_site0_var0"][1,:]
    ncnlai.close()
    
    laitypes =[laiold, elainew, lainorm] #lainew, 
    for i in range(len(laitypes)):
        table_lai_rmse[i,isite] = round(rmse(laiobs,laitypes[i]),3)

    isite = isite +1

temp1 = table_lai_rmse/table_lai_rmse[0,:]
plt.figure(figsize=(6,7))
for i in range(0,12):
    values = [temp1[1,i],temp1[2,i]]
    plt.plot(i, temp1[1,i],marker="x",markersize=15,linewidth=0,markeredgewidth=3,label="LAI opt",color="C0")
    plt.plot(i, temp1[2,i],marker="x",markersize=15,linewidth=0,markeredgewidth=3,label="eLAI opt",color="C1")
    plt.vlines(i, ymin=np.nanmin(values), ymax=np.nanmax(values),color="grey",linestyle=":")
    plt.axhline(y=1,color="grey",linestyle='--')      
    # set up axis
    plt.ylim(0,3)
    plt.xlim(-0.5,9.5)
    plt.xticks(np.arange(0,10,1), sites["Site"], size=15, rotation=35)
    plt.ylabel("RMSE/RMSE$_{prior}$ (LAI)",size=17)
    plt.yticks(size=15)
    # create legend
    empty_patch =  mlines.Line2D([], [], color='white', marker='',markeredgewidth=2, linestyle='None',markersize=10, label='')
    elai_patch = mpatches.Patch(color='C0', label='eLAI opt')
    lainorm_patch = mpatches.Patch(color='C1', label='norm opt')
    plt.legend(handles=[elai_patch,lainorm_patch],ncol=1,framealpha=0,edgecolor="black", fontsize=15)

plt.savefig("LAI_RMSE.png")
plt.close()
