"""
Script for plotting GPP and Reco barplots for GBC ORCH DA review paper
"""

__author__ = "Natasha MacBean"
__version__ = "1.0 (05.06.2021)"
__email__ = "nlmacbean@gmail.com"


import matplotlib
matplotlib.use("Agg")
import numpy as np, netCDF4, matplotlib.pyplot as plt
import pandas as pd
from collections import OrderedDict
import sys


# - Set-up
years = '2000_2009'	#'1990_2012'
infile = 'regional_%s_Prior_Stepwise_Simul.csv'
outdir = './'
xlabels = ['Prior', 'Step-wise', 'Simultaneous']
grossCfluxes = OrderedDict( [ ('GPP', 'GPP'), ('Re', 'R$_{eco}$') ] )
labels = ut.label_generator(case='lower', start='(', end=')')

# - Plot
for ngc, gc in enumerate(grossCfluxes.keys()):

    data = pd.read_csv(infile%(gc), index_col=0)
    
    highs = data.NH.tolist()
    mids = data.Tropics.tolist()
    lows = data.SH.tolist()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.bar(range(len(xlabels)), highs, width = 0.5, color = "#006DDB", edgecolor = "none", label="N.hemis")
    ax.bar(range(len(xlabels)), mids,  width = 0.5, color = "#EE3333", edgecolor = "none", label="Tropics", bottom = highs)
    ax.bar(range(len(xlabels)), lows,  width = 0.5, color = "#66AA55", edgecolor = "none", label="S.hemis", bottom = np.array(highs) + np.array(mids))
    ax.set_xticks(range(len(xlabels)))
    ax.set_xticklabels(xlabels)
    ax.set_ylabel(grossCfluxes[gc]+' (PgC.yr$^{-1}$)')
    ax.legend(loc = "upper left", bbox_to_anchor = (1.05, 1.02))
    ax.yaxis.grid(alpha=0.5)
    ax.set_ylim([0,160])
    ax.text(-0.35,154, next(labels), fontsize=10)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    plt.savefig(outdir+'atmCO2sims_'+gc+'_'+years+'.png', dpi = 120)
