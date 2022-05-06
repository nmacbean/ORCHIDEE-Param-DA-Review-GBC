"""
Script for plotting GPP barplots from NEE, NDVI and GOME-2 SIF optimizations for GBC ORCH DA review paper
"""

__author__ = "Natasha MacBean"
__version__ = "1.0 (01.29.2021)"
__email__ = "nlmacbean@gmail.com"


import matplotlib
matplotlib.use("Agg")
import numpy as np, netCDF4, matplotlib.pyplot as plt
import pandas as pd
import sys

# - set-up
years = '2000_2009'	#'1990_2012'
infile = 'regional_GPP_Prior_NEE_NDVI_SIF_Jung.csv'
outdir = './'
labels = ["Prior", "FLUXNET\nNEE", "MODIS\nNDVI", "GOME-2\nSIF", "Upscaled\nFLUXNET"]


# - read in data
data = pd.read_csv(infile, index_col=0)
highs = data.NH.tolist()
mids = data.Tropics.tolist()
lows = data.SH.tolist()

# - plot
fig = plt.figure()
ax = fig.add_subplot(111)
ax.bar(range(len(labels)), highs, width = 0.5, color = "#006DDB", edgecolor = "none", label="N.hemis")
ax.bar(range(len(labels)), mids,  width = 0.5, color = "#EE3333", edgecolor = "none", label="Tropics", bottom = highs)
ax.bar(range(len(labels)), lows,  width = 0.5, color = "#66AA55", edgecolor = "none", label="S.hemis", bottom = np.array(highs) + np.array(mids))
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels)
ax.set_ylabel("Mean GPP [PgC/yr] (2000-2009)")
ax.legend(loc = "upper left", bbox_to_anchor = (0.7, 1.0))
ax.vlines(3.5,0,175, linewidth=0.5)
ax.yaxis.grid(alpha=0.5)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.savefig(outdir+'mean_GPP_assim_comparison_'+years+'.png', dpi = 120)

