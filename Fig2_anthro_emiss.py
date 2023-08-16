import numpy as np
import numpy.ma as ma
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import glob
import os
import sys

# developed and tested at Python version is 3.9.16

#--------------------------------------------------------------------
#
# functions

'''
outputs the list of region names

provide 2 options - default is for use in filenames, so include underscore "_"
but also have "tidy" version, with a space, for use in plot labels
'''
def names(x, tidy=False):
    if tidy:
        switcher = {
           1: 'North America',
           2: 'South America',
           3: 'Europe',
           4: 'Northern Africa',
           5: 'Southern Africa',
           6: 'North Asia',
           7: 'Central Asia',
           8: 'East Asia',
           9: 'South Asia',
           10: 'South East Asia',
           11: 'Oceania',
           12: 'Oceans',
           13: 'Africa',
           14: 'Australia',
           15: 'New Zealand',
        }
    else:
        switcher = {
           1: 'North_America',
           2: 'South_America',
           3: 'Europe',
           4: 'Northern_Africa',
           5: 'Southern_Africa',
           6: 'North_Asia',
           7: 'Central_Asia',
           8: 'East_Asia',
           9: 'South_Asia',
           10: 'South_East_Asia',
           11: 'Oceania',
           12: 'Oceans',
           13: 'Africa',
           14: 'Australia',
           15: 'New_Zealand',
        }

    return switcher.get(x, "nothing")

#
#--------------------------------------------------------------------
#

out_file = 'Fig2_anthro_emiss.jpg' 
fig, axes = plt.subplots(3, 4, figsize = (16,12))

for ax in axes[-1,:]:
    ax.set_xlabel('year', fontsize=14)
    
for ax in axes[:,0]:
    ax.set_ylabel('PgC / yr', fontsize=14)
    
# loop over regions - need to just get all Africa, not split north/south
reg_list_oneAfrica = [1,2,3,13,6,7,8,9,10,11]

for reg in reg_list_oneAfrica:
    ax_pointer = reg-1
    if reg >3: ax_pointer = reg-2
    if reg == 13: ax_pointer = 3

    ax = np.ravel(axes)[ax_pointer]
    if (reg == 6):
        ax.set_title('Russia', fontsize=16)
    elif (reg == 11):
        ax.set_title('Australasia', fontsize=16)
    else:
        ax.set_title(names(reg, tidy=True), fontsize=16)
    
    in_dir = 'DATA/Processed/' + names(reg)+'/'
    y_hist, val_hist = np.loadtxt(in_dir+'historical/CO2_em_anthro_historical_'+ names(reg) +'_1850-2014.txt').T
    y_126,  val_126  = np.loadtxt(in_dir+'ssp126/CO2_em_anthro_ssp126_'+ names(reg) +'_2015-2100.txt').T
    y_370,  val_370  = np.loadtxt(in_dir+'ssp370/CO2_em_anthro_ssp370_'+ names(reg) +'_2015-2100.txt').T

    ax.plot(y_370, val_370, 'r', lw=3, label='SSP3-7.0')
    ax.plot(y_126, val_126, 'b', lw=3, label='SSP1-2.6')
    ax.plot(y_hist, val_hist, 'k', lw=3, label='Historical')
    ax.axhline(ls='--', color='k', lw=.5)
    
    # set common y-range
    ax.set_ylim(-1,6)
    
    if reg == 1:
        ax.legend(fontsize=14)
        
# don't show axes of final 2
ax = np.ravel(axes)[10]; ax.axis('off')
ax = np.ravel(axes)[11]; ax.axis('off')

plt.savefig(out_file)

plt.close()
