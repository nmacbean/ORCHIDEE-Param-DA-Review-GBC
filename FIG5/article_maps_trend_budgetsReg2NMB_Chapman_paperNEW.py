# =======================
# Plot bilans globaux
# =======================

__author__ = "Cedric Bacour"
__version__ = "1.0 (07.08.2021)"
__email__ = "cedric.bacour@lsce.ipsl.fr"


import os,sys
import numpy as np
import netCDF4
import glob
import matplotlib.pyplot as plt
import scipy.stats
import cPickle
import set_colors
from collections import OrderedDict
plt.ion()



# ========================================================
# Main
# ========================================================

# -
# - Parametres
# -
path_out = './'
if not os.path.isdir(path_out): os.mkdir(path_out)

colors = {}
ccols1 = set_colors.colors['tableau20']
colors['stepwise'] = ccols1[-1]
colors['F+S+CO2'] = 'C0' 
colors['F'] = 'C1'
colors['S'] = 'C2'
colors['stepwise'] = 'C3'


# -
# - Lecture des donnees
# -
filein = os.path.join(path_out,'bilans_regions2_trendIav_NMB_Chapman-article.pickle')
res = cPickle.load(file(filein,'r'))




#
# - Trends par regions
# - 
###regions = ['nhemisphere','tropics']
regs_names_sorted = ['nhemisphere','tropics']
annees = np.arange(10)+2000
ifig = 1
try:
    plt.close(ifig)
except:
    pass
dy = 0.06
iX = 0.075

vars = OrderedDict( [ ('NEEt', OrderedDict([('cases', ['F+S+CO2','stepwise'])]) ), \
                      ('GPPt', OrderedDict([('cases', ['F','S'])]) ) ] )
label_position = {'NEEt':{'nhemisphere':0.4,'tropics':0.9},'GPPt':{'nhemisphere':60.5, 'tropics':109.2}}

xleg = {'NEEt':{'nhemisphere':0.55,'tropics':0.3},'GPPt':{'nhemisphere':0.2, 'tropics':0.3}}
yleg = {'NEEt':{'nhemisphere':0.3,'tropics':0.3},'GPPt':{'nhemisphere':0.57, 'tropics':0.57}}

f, axn = plt.subplots(figsize=(9,5), sharex=True, sharey=True)
plt.subplots_adjust(left=0.08, right=0.99, bottom=0.09, top=0.94, wspace=0.1, hspace=0.05)

for (ireg,reg) in enumerate(regs_names_sorted):

    for (ivar,var) in enumerate(vars.keys()):
    
        means = [res['trendIav']['prior_%s'%(var)][reg]['mean']]
        trends = [res['trendIav']['prior_%s'%(var)][reg]['trend']]
        iavs = [res['trendIav']['prior_%s'%(var)][reg]['iav']]
        for (i,k) in enumerate(vars[var]['cases']):
            means.append(res['trendIav']['post_%s_%s'%(var,k)][reg]['mean'])
            trends.append(res['trendIav']['post_%s_%s'%(var,k)][reg]['trend'])
            iavs.append(res['trendIav']['post_%s_%s'%(var,k)][reg]['iav'])

        ax = plt.subplot(2, 2, ireg*len(vars.keys())+ivar+1)
        ax.plot(annees, res['prior'][var]['yearly_budgets'][reg],'-',color='0.5',label='prior')


        for cas in vars[var]['cases']:
            style = '-'
            if "resOpti" in cas: style = "--"
            col_cas = cas
            if cas == 'F+S+CO2':
                label_cas = 'simultaneous'
            elif cas == 'F':
                label_cas = 'FLUXNET NEE'
            elif cas == 'S':
                label_cas = 'MODIS NDVI'
            else:
                label_cas = cas
            if "PRIORSPIN_KSOILC" in col_cas: col_cas = col_cas.replace("_PRIORSPIN_KSOILC","")
            ax.plot(annees, res['post'][var][cas]['yearly_budgets'][reg],style,color=colors[col_cas],label=label_cas)
        if 'NEE' in var: ax.plot([annees[0], annees[-1]],[0,0],'--k')


        if reg == 'tropics':
            ax.set_xticks(annees)
            ax.set_xticklabels([str(annee) for annee in annees], rotation=30, horizontalalignment='right')
        else:
            ax.set_xticklabels('')
        if reg == 'nhemisphere':
            plt.title(var.replace('t',' (PgCyr$^{-1}$)'), fontsize=14)
            ax.legend(frameon=False)
        if var == 'NEEt': ax.set_ylabel('%s'%(reg), fontsize = 14)

        
        ax.text(xleg[var][reg],yleg[var][reg],'Mean',transform=ax.transAxes, fontsize=7)
        ax.text(xleg[var][reg]+iX,yleg[var][reg],' Trend ',transform=ax.transAxes, fontsize=7)
        ax.text(xleg[var][reg]+iX*2,yleg[var][reg],' IAV ',transform=ax.transAxes, fontsize=7)

        i = 0
        ax.text(xleg[var][reg],yleg[var][reg]-0.05-(dy*i),'%6.2f'%(means[i]),transform = ax.transAxes, color='0.5', fontsize=7)
        ax.text(xleg[var][reg]+iX,yleg[var][reg]-0.05-(dy*i),'%6.2f'%(trends[i]),transform = ax.transAxes, color='0.5', fontsize=7)
        ax.text(xleg[var][reg]+iX*2,yleg[var][reg]-0.05-(dy*i),'%6.2f'%(iavs[i]),transform = ax.transAxes, color='0.5', fontsize=7)
        
        
        for (i,k) in enumerate(vars[var]['cases']):
            i+=1
            col_cas = k
            fontweight = 'normal'
            if "PRIORSPIN_KSOILC" in col_cas: 
                col_cas = col_cas.replace("_PRIORSPIN_KSOILC","")
                fontweight = 'bold'

            ax.text(xleg[var][reg],yleg[var][reg]-0.05-(dy*i),'%6.2f'%(means[i]),transform = ax.transAxes,  color=colors[col_cas], fontsize=7)
            ax.text(xleg[var][reg]+iX,yleg[var][reg]-0.05-(dy*i),'%6.2f'%(trends[i]),transform = ax.transAxes,  color=colors[col_cas], fontsize=7)
            ax.text(xleg[var][reg]+iX*2,yleg[var][reg]-0.05-(dy*i),'%6.2f'%(iavs[i]),transform = ax.transAxes, color=colors[col_cas], fontsize=7)

        ifig += 1
        
        plt.savefig(os.path.join(path_out,'trendIav_NEE_GPP_NH_tropics_ChapmanPaper.pdf'))



