import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

plt.ion()

# ==========================
# Visualisation des couleurs
#
# ex: set_colors.display(set_colors.colors['tableau20'])
# --------------------------
def display_bars(colors):

    n=len(colors)
    index = np.arange(n)
    vals = np.ones(n)

    bar_width = 0.5
    opacity = 1

    f=plt.figure(1)
    f.clf()
    for i in index:
        plt.bar(i,vals[i], bar_width, alpha = opacity, color = colors[i], label = str(i) )
    plt.show()


def display(colors):
    n = len(colors)
    x = np.arange(n)+0.5
    y = np.ones(n)

    for i in range(n):
        plt.plot(x[i],y[i], 'o', c=colors[i], markersize=10)
    plt.show()

# ==========================


# ==========================
# Define colors from Rainbow
def colors_from_rainbow(nel):
    cols = []
    for x in np.linspace(0,1, nel):
        rcol = (0.472-0.567*x+4.05*x**2)/(1.+8.72*x-19.17*x**2+14.1*x**3)
        gcol = 0.108932-1.22635*x+27.284*x**2-98.577*x**3+163.3*x**4-131.395*x**5+40.634*x**6
        bcol = 1./(1.97+3.54*x-68.5*x**2+243*x**3-297*x**4+125*x**5)
        cols.append((rcol, gcol, bcol))
    return cols

# ==========================


# ==========================
# Define colors for lines
def color_lines(nel, cmapname):
    cmap = plt.get_cmap(cmapname)
    colors = cmap(np.linspace(0,1,nel))
    return colors
# END color_lines
# ==========================



colors = {}

# http://tableaufriction.blogspot.ro/2012/11/finally-you-can-use-tableau-data-colors.html
colors['tableau20'] = [[31,119,180],
                       [174,199,232],
                       [255,127,14],
                       [255,187,120],
                       [44,160,44],
                       [152,233,138],
                       [214,39,40],
                       [255,152,150],
                       [148,103,189],
                       [197,176,213],
                       [140,86,75],
                       [196,156,148],
                       [227,119,194],
                       [247,182,210],
                       [127,127,127],
                       [199,199,199],
                       [188,189,34],
                       [219,219,141],
                       [23,190,207],
                       [158,218,229]
                       ]

colors['tableau10light'] = [[174,199,232],
                            [255,187,120],
                            [152,223,138],
                            [255,152,150],
                            [197,176,213],
                            [196,156,148],
                            [247,182,210],
                            [199,199,199],
                            [219,219,141],
                            [158,218,229]]
# http://www.sron.nl/~pault/
colors['colorblind10'] = [[51,102,170],
                         [153,34,136],
                         [17,170,153],
                         [238,51,51],
                         [102,170,85],
                         [238,119,34],
                         [204,204,85],
                         [255,238,51],
                         [119,119,119],
                         [60,60,60]]

colors['colorblind12'] = [[120,28,129],
                          [63,78,161],
                          [70,131,193],
                          [87,163,173],
                          [109,179,136],
                          [177,190,78],
                          [223,165,58],
                          [231,116,47],
                          [217,33,32],
                          [238,238,238],
                          [60,60,60]]

colors['colorblind16'] = [[136,46,114],
                          [177,120,166],
                          [214,193,222],
                          [25,101,176],
                          [82,137,199],
                          [123,175,222],
                          [78,178,101],
                          [144,201,135],
                          [202,224,171],
                          [247,238,85],
                          [246,193,65],
                          [241,147,45],
                          [232,96,28],
                          [220,5,12],
                          [119,119,119],
                          [60,60,60]]

colors['colorblind24'] = [[232,236,251],
                          [217,204,227],
                          [202,172,203],
                          [186,141,180],
                          [170,111,158],
                          [153,79,136],
                          [136,46,114],
                          [25,101,176],
                          [67,125,191],
                          [97,149,207],
                          [123,175,222],
                          [78,178,101],
                          [144,201,135],
                          [202,224,171],
                          [247,240,86],
                          [247,203,69],
                          [244,167,54],
                          [238,128,38],
                          [230,85,24],
                          [220,5,12],
                          [165,23,14],
                          [114,25,14],
                          [66,21,10],
                          [119,119,119]]



for key in colors.keys():
    colors[key] = np.array(colors[key])/255.


colors['tab20c']=cm.tab20c.colors
colors['tab20b']=cm.tab20b.colors



# symetrical colorbars
colmaps_sym =  ['BrBG','BrBG_r','PiYG','PiYG_r','PuOr','PuOr_r','Rd_Bu','Rd_Bu_r','bwr','bwr_r','coolwarm','coolwarm_r',
                'seismic','seismic_r']



