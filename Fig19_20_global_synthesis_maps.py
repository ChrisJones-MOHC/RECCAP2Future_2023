import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
import cartopy.crs as ccrs
import pandas as pd
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import glob
import os
import sys

# developed and tested at Python version is 3.8.13

def ext(x,region):
    return x.intersection(longitude=(region[0], region[2]), latitude=(region[1], region[3]))


# colours
col_co2  = '#d1e0ee'
col_ff   = '#7f3300'
col_land = '#66bf7d'
col_ocn  = '#506fba'

# map mask
mask = iris.load('DATA/RECCAP_AfricaSplit_MASK11_Mask_regridded.nc')[0]

# colour map
from matplotlib.colors import ListedColormap
# use colours from cmap "Set3" but add white to the end:
cmap = ListedColormap([(0.5529411764705883, 0.8274509803921568, 0.7803921568627451),
 (1.0, 1.0, 0.7019607843137254),
 (0.7450980392156863, 0.7294117647058823, 0.8549019607843137),
 (0.984313725490196, 0.5019607843137255, 0.4470588235294118),
 (0.984313725490196, 0.5019607843137255, 0.4470588235294118),
 (0.5019607843137255, 0.6941176470588235, 0.8274509803921568),
 (0.9921568627450981, 0.7058823529411765, 0.3843137254901961),
 (0.7019607843137254, 0.8705882352941177, 0.4117647058823529),
 (0.9882352941176471, 0.803921568627451, 0.8980392156862745),
 (0.6509803921568627, 0.6509803921568627, 0.6509803921568627),
 (0.7372549019607844, 0.5019607843137255, 0.7411764705882353),
 (0.8, 0.9215686274509803, 0.7725490196078432),
# (1.0, 0.9294117647058824, 0.43529411764705883),
 '#ffffff'])

var_levs = np.arange(12)
norm = mpl.colors.BoundaryNorm(var_levs,len(var_levs))

# extract map to crop below 60S
m2 = ext(mask,[-180,-60,180,90])

def plot_bar_axis(ax, reg, ssp126, ssp370):
# colours
    col_co2  = '#d1e0ee'
    col_ff   = '#7f3300'
    col_land = '#66bf7d'
    col_ocn  = '#506fba'

# ssp126
    foss_126 = ssp126[0]
    veg_126 = ssp126[1]
    soil_126 = ssp126[2]

# ssp370
    foss_370 = ssp370[0]
    veg_370 = ssp370[1]
    soil_370 = ssp370[2]

# limits
    ymax = np.max([foss_126, foss_370]) * 1.5
    if reg=='North_Asia': ymax = ymax+10
    ymin = np.min([0,foss_126-veg_126-soil_126, foss_370-veg_370-soil_370]) * 1.1
    incr = (ymax - ymin)/10.

    ax.set_xlim(0,8)
    ax.set_ylim(ymin,ymax)
    ax.axhline(color='k', linestyle='--')

    ax.bar(0.5, foss_126, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_ff)
    ax.bar(1.5, -veg_126, width=0.8, bottom=foss_126, align='edge', edgecolor='k', color=col_land)
    ax.bar(2.5, -soil_126, width=0.8, bottom=foss_126-veg_126, align='edge', edgecolor='k', color=col_land)

    ax.bar(4.5, foss_370, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_ff)
    ax.bar(5.5, -veg_370, width=0.8, bottom=foss_370, align='edge', edgecolor='k', color=col_land)
    ax.bar(6.5, -soil_370, width=0.8, bottom=foss_370-veg_370, align='edge', edgecolor='k', color=col_land)
    
    ax.text(0.65,foss_126+incr/2, 'fossil')
    ax.text(1.65,foss_126-veg_126-incr, 'veg')
    ax.text(2.65,foss_126-veg_126-soil_126-incr, 'soil')
    
    ax.text(4.65,foss_370+incr/2, 'fossil')
    ax.text(5.65,foss_370-veg_370-incr, 'veg')
    ax.text(6.65,foss_370-veg_370-soil_370-incr, 'soil')

    ax.text(1.2, ymax - incr*2, 'SSP1-2.6', color='b', fontsize=12)
    ax.text(5.2, ymax - incr*2, 'SSP3-7.0', color='r', fontsize=12)


# set up grid to get ready for bars all around the map
#
fig = plt.figure(figsize=(18,12))

gs = gridspec.GridSpec(ncols=5, nrows=4)

ax1 = fig.add_subplot(gs[1,0])  # N. America
ax2 = fig.add_subplot(gs[2,0])  # S. America

ax3 = fig.add_subplot(gs[0,1])  # Europe
ax4 = fig.add_subplot(gs[0,2])  # Central Asia
ax5 = fig.add_subplot(gs[0,3])  # N. Asia

ax6 = fig.add_subplot(gs[1,4])  # E. Asia
ax7 = fig.add_subplot(gs[2,4])  # S.E. Asia

ax8 = fig.add_subplot(gs[3,1])  # Africa
ax9 = fig.add_subplot(gs[3,2])  # S. Asia
ax10 = fig.add_subplot(gs[3,3])  # Oceania

axmap = fig.add_subplot(gs[1:3,1:4], projection = ccrs.Robinson(central_longitude= 10))  # Globe
axmap.gridlines()
axmap.coastlines()  
coldata = iplt.contourf(m2, var_levs, cmap = cmap, norm=norm, extend='both')

for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10]:
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.bottom.set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.set_xticklabels([])
    ax.set_xticks([])

axpts = fig.add_subplot(gs[:,:])  # whole grid
axpts.axis('off')


# 2050
plot_bar_axis(ax8, 'Africa', [14.085,9.761456593355177,2.6479267703877527], [20.639, 1.0761726691401634, 13.396081135047293])
plot_bar_axis(ax4, 'Central_Asia', [23.865520355175043, 0.8203568347126406, 1.3576666442121308], [39.44746791440367, 0.8422633467544225, 4.056359731696789])
plot_bar_axis(ax6, 'East_Asia', [90.08351035054483, 7.947606752746317, 3.7000899952111928], [160.7164925931046, 8.872622618425801, 11.13448483373526])
plot_bar_axis(ax3, 'Europe', [26.036887930668403, 3.4299797024007255, 1.938215647377919], [40.802459213176256, 3.753686218669685, 6.701193380579005])
plot_bar_axis(ax1, 'North_America', [43.03430198627354, 14.772678119554087, 5.024520873273567], [72.81028575319203, 12.050536261930148, 26.481856731906653])
plot_bar_axis(ax5, 'North_Asia', [12.146337722762498, 11.946860234266559, 6.030810168014481], [18.114808190932372, 13.553481525684361, 31.649835321052755])
plot_bar_axis(ax10, 'Oceania', [2.710585323724809, 1.09936895630298, 0.7531939343210633], [4.574415776573589, 1.6588895297365305, 3.628343655601216])
plot_bar_axis(ax2, 'South_America', [11.841054215436657, 11.736861792007034, 2.152286316441327], [16.137482176320027, 9.120963294113977, 13.50688946271905])
plot_bar_axis(ax9, 'South_Asia', [27.13924485070802, 1.3945353509703597, 1.139711534998122], [37.315744034531775, 0.8226925097673234, 2.5784860706545256])
plot_bar_axis(ax7, 'South_East_Asia', [13.698486533261226, 4.6262740905649835, 0.5862153390889786], [18.977675044553916, 4.381701167629352, 2.682715167534962])

# add some lines
axpts.set_xlim(0,240)
axpts.set_ylim(0,160)

axpts.plot([35,80],[90,95],'k', lw=2, marker='o', markersize=10)
axpts.plot([40,90],[65,70],'k', lw=2, marker='o', markersize=10)
axpts.plot([85,120],[130,98],'k', lw=2, marker='o', markersize=10)
axpts.plot([120,138],[130,95],'k', lw=2, marker='o', markersize=10)
axpts.plot([175,150],[130,105],'k', lw=2, marker='o', markersize=10)
axpts.plot([205,155],[100,90],'k', lw=2, marker='o', markersize=10)
axpts.plot([203,163],[65,75],'k', lw=2, marker='o', markersize=10)
axpts.plot([85,125],[35,80],'k', lw=2, marker='o', markersize=10)
axpts.plot([120,146],[35,85],'k', lw=2, marker='o', markersize=10)
axpts.plot([170,165],[35,63],'k', lw=2, marker='o', markersize=10)

plt.savefig('Fig19_RECCAP2_global_synthesis_2050.jpg')

# repeat for 2100
#
fig = plt.figure(figsize=(18,12))

gs = gridspec.GridSpec(ncols=5, nrows=4)
#gs = gridspec.GridSpec(ncols=5, nrows=4, wspace=0, hspace=0)

ax1 = fig.add_subplot(gs[1,0])  # N. America
ax2 = fig.add_subplot(gs[2,0])  # S. America

ax3 = fig.add_subplot(gs[0,1])  # Europe
ax4 = fig.add_subplot(gs[0,2])  # Central Asia
ax5 = fig.add_subplot(gs[0,3])  # N. Asia

ax6 = fig.add_subplot(gs[1,4])  # E. Asia
ax7 = fig.add_subplot(gs[2,4])  # S.E. Asia

ax8 = fig.add_subplot(gs[3,1])  # Africa
ax9 = fig.add_subplot(gs[3,2])  # S. Asia
ax10 = fig.add_subplot(gs[3,3])  # Oceania

axmap = fig.add_subplot(gs[1:3,1:4], projection = ccrs.Robinson(central_longitude= 10))  # Globe
axmap.gridlines()
axmap.coastlines()  
coldata = iplt.contourf(m2, var_levs, cmap = cmap, norm=norm, extend='both')

for ax in [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10]:
    ax.spines.right.set_visible(False)
    ax.spines.top.set_visible(False)
    ax.spines.bottom.set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.set_xticklabels([])
    ax.set_xticks([])

axpts = fig.add_subplot(gs[:,:])  # whole grid
axpts.axis('off')

#2100
plot_bar_axis(ax8, 'Africa', [19.963, 14.175894082733976, 4.808392370303893], [77.962, 4.261292749628183, 13.956855092087597])
plot_bar_axis(ax4, 'Central_Asia', [34.5510542470073, 1.18283169620595, 2.3233689708124867], [104.6518472500849, 1.8623547469019028, 6.118164997903127])
plot_bar_axis(ax6, 'East_Asia', [102.58004477721443, 11.914692127800969, 6.965069647269388], [339.6927626937009, 21.272270393945952, 16.709575800399612])
plot_bar_axis(ax3, 'Europe', [31.100780902803596, 4.699557869624648, 3.242708819123098], [94.43482719848149, 8.112764603306907, 8.73386081637348])
plot_bar_axis(ax1, 'North_America', [48.35935335011948, 21.167431148120457, 8.726537102653124], [185.85836999740033, 25.99933338183851, 30.153851502430776])
plot_bar_axis(ax5, 'North_Asia', [15.350647835880505, 18.346474731793712, 12.139320703846357], [42.73644605326042, 30.791842265716745, 39.457685042636655])
plot_bar_axis(ax10, 'Oceania', [2.580279011101011, 1.773396909572238, 1.328317656931117], [11.173628532406585, 3.4004086033528935, 4.697051521191182])
plot_bar_axis(ax2, 'South_America', [7.2578380861723915, 13.905339924669107, 3.2965366636213114], [42.4255974274904, 17.784377940592663, 14.271304565033372])
plot_bar_axis(ax9, 'South_Asia', [37.27945399234956, 2.195827721222198, 1.7767790383323008], [114.09124105127619, 2.750232188241121, 3.6371354105298472])
plot_bar_axis(ax7, 'South_East_Asia', [16.27564536254541, 7.27720622999275, 1.3830138426975347], [54.772477529114354, 12.045548218787339, 4.221042140669206])

# add some lines
axpts.set_xlim(0,240)
axpts.set_ylim(0,160)

axpts.plot([35,80],[90,95],'k', lw=2, marker='o', markersize=10)
axpts.plot([40,90],[65,70],'k', lw=2, marker='o', markersize=10)
axpts.plot([85,120],[130,98],'k', lw=2, marker='o', markersize=10)
axpts.plot([120,138],[130,95],'k', lw=2, marker='o', markersize=10)
axpts.plot([175,150],[130,105],'k', lw=2, marker='o', markersize=10)
axpts.plot([205,155],[100,90],'k', lw=2, marker='o', markersize=10)
axpts.plot([203,163],[65,75],'k', lw=2, marker='o', markersize=10)
axpts.plot([85,125],[35,80],'k', lw=2, marker='o', markersize=10)
axpts.plot([120,146],[35,85],'k', lw=2, marker='o', markersize=10)
axpts.plot([170,165],[35,63],'k', lw=2, marker='o', markersize=10)

plt.savefig('Fig20_RECCAP2_global_synthesis_2100.jpg')
