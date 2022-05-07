"""
Script for plotting NBP barplots from stepwise and simultaneous optimizations 
with NEE, NDVI and atmospheric CO2 data cf CAMS inversion and GCB 
for GBC ORCH DA review paper
"""

__author__ = "Vladislav Bastrikov"
__version__ = "4.0 (05.05.2022)"
__email__ = "vladislav.bastrikov@lsce.ipsl.fr"


import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

red = "#EE3333"
green = "#66AA55"
blue = "#006DDB"
width = 0.4
data = np.zeros((6,3))

data[0] = np.array([-0.06783101, -0.26974791,  0.03496701]) # prior
data[1] = np.array([-0.41741104, -1.23415691, -0.01929178]) # stepwise terrestrial flux
data[2] = np.array([-1.18534595, -1.11952039, -0.03422025]) # simult terrestrial flux
bb = np.array([-0.00865385, 0.89919175, -0.00219209]) # biomass burning flux
data[3] = data[1] + bb # stepwise total land flux
data[4] = data[2] + bb # simult total land flux
data[5] = np.array([-2.66160878, 0.52807692, -0.09834274]) # CAMS

fig, ax = plt.subplots()
h1=ax.bar([-10],[-10], color = blue, label="N.hemis")
h2=ax.bar([-10],[-10], color = red, label="Tropics")
h3=ax.bar([-10],[-10], color = green, label="S.hemis")
xs = 0.5 + np.arange(len(data))
ax.bar(xs, [(data[idx,2]+data[idx,1]+data[idx,0] if np.sign(data[idx,2]) == np.sign(data[idx,1]) == np.sign(data[idx,0]) else data[idx,2]+data[idx,1] if np.sign(data[idx,2]) == np.sign(data[idx,1]) else data[idx,2]+data[idx,0] if np.sign(data[idx,2]) == np.sign(data[idx,0]) else data[idx,2]) for idx in range(len(data))], width, color = green, edgecolor = "none")
ax.bar(xs, [(data[idx,1]+data[idx,0] if np.sign(data[idx,1]) == np.sign(data[idx,0]) else data[idx,1]) for idx in range(len(data))], width, color = red, edgecolor = "none")
ax.bar(xs, data[:,0], width, color = blue, edgecolor = "none")

h4=ax.errorbar(0.4, -2.9, yerr=0.9, fmt='o', color="grey", capsize=7)
h4=ax.errorbar(1.4, -2.9, yerr=0.9, fmt='o', color="grey", capsize=7)
h4=ax.errorbar(2.4, -2.9, yerr=0.9, fmt='o', color="grey", capsize=7)
h5=ax.errorbar(0.6, -2.7, yerr=0.7, fmt='o', color="#DBD100", capsize=7)
h5=ax.errorbar(1.6, -2.7, yerr=0.7, fmt='o', color="#DBD100", capsize=7)
h5=ax.errorbar(2.6, -2.7, yerr=0.7, fmt='o', color="#DBD100", capsize=7)
h6=ax.errorbar(3.4, -1.6, yerr=0.6, fmt='o', color="k", capsize=7)
h6=ax.errorbar(4.4, -1.6, yerr=0.6, fmt='o', color="k", capsize=7)
h6=ax.errorbar(5.5, -1.6, yerr=0.6, fmt='o', color="k", capsize=7)
h7=ax.errorbar(3.6, -1.3, yerr=0.5, fmt='o', color="orange", capsize=7)
h7=ax.errorbar(4.6, -1.3, yerr=0.5, fmt='o', color="orange", capsize=7)

ax.plot([0,1], [data[0].sum(), data[0].sum()], color="k", linestyle="--")
ax.plot([1,2], [data[1].sum(), data[1].sum()], color="k", linestyle="--")
ax.plot([2,3], [data[2].sum(), data[2].sum()], color="k", linestyle="--")
ax.plot([3,4], [data[3].sum(), data[3].sum()], color="k", linestyle="--")
ax.plot([4,5], [data[4].sum(), data[4].sum()], color="k", linestyle="--")
ax.plot([5,6], [data[5].sum(), data[5].sum()], color="k", linestyle="--")

ax.axvline(3, color="k", linewidth=0.5, linestyle="--")
ax.axvline(5, color="k", linewidth=0.5)
ax.set_xlim([0,len(data)])
ax.set_ylim([-4.8,0.7])
ax.set_xticks(xs)
ax.set_xticklabels(["Prior", "Stepwise\nterrestrial\nflux", "Simult\nterrestrial\nflux", "Stepwise\ntotal land\nflux", "Simult\ntotal land\nflux", "CAMS\natmospheric\ninversion"], fontsize=8)
ax.set_ylabel("Mean NBP [PgC/yr] (2000-2009)")
ax.yaxis.grid()
ax.legend([h1,h2,h3,h4,h5,h6,h7], ["Northern Hemisphere","Tropics","Southern Hemisphere","GCB residual $\mathsf{S}_\mathsf{LAND}$","DGVM $\mathsf{S}_\mathsf{LAND}$","GCB total land flux","DGVM total land flux"], loc = 'lower right', fontsize=9)
plt.tight_layout()
plt.savefig("mean_NBP_assim_comparison_2000_2009.png", dpi=150)

