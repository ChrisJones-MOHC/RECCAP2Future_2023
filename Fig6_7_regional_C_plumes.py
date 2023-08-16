import numpy as np
import matplotlib.pyplot as plt
import os.path as path

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


def get_var_array(reg, var, table, proc, models, ripf, scenario, years):
    
    var_array_hist = []
    var_array_126  = []
    var_array_370  = []
    
    for m in np.arange(len(models)):
        file_hist = scenario[0]+'/'+'CMIP6_'+models[m]+'_'+table+'_'+scenario[0]+'_'+ripf[m]+'_'+var+'_'+reg+'_'+years[0]+'.txt'
        file_126  = scenario[1]+'/'+'CMIP6_'+models[m]+'_'+table+'_'+scenario[1]+'_'+ripf[m]+'_'+var+'_'+reg+'_'+years[1]+'.txt'
        file_370  = scenario[2]+'/'+'CMIP6_'+models[m]+'_'+table+'_'+scenario[2]+'_'+ripf[m]+'_'+var+'_'+reg+'_'+years[2]+'.txt'

        if (path.isfile(in_dir+file_hist)):
            #print(file_hist)
            y_hist, val_hist = np.loadtxt(in_dir+file_hist).T
            if (proc == 2):
                off = val_hist[0]
            else:
                off = np.mean(val_hist[0:51])

            val_hist = val_hist - off
            var_array_hist.append(val_hist)
            
        if (path.isfile(in_dir+file_126)):
            #print(file_126)
            y_126, val_126 = np.loadtxt(in_dir+file_126).T
            val_126 = val_126 - off
            var_array_126.append(val_126)
            
        if (path.isfile(in_dir+file_370)):
            #print(file_370)
            y_370, val_370 = np.loadtxt(in_dir+file_370).T
            val_370 = val_370 - off
            var_array_370.append(val_370)

    return y_hist, y_126, y_370, var_array_hist, var_array_126, var_array_370



#
#--------------------------------------------------------------------
#

var = ['tas', 'pr', 'cVeg', 'cLitter', 'cProduct', 'cSoil', 'cLand', 'gpp', 'npp', 'rh', 'nbp']
table = ['Amon', 'Amon', 'Lmon', 'Lmon', 'Lmon', 'Emon', 'Emon', 'Lmon', 'Lmon', 'Lmon', 'Lmon']
proc = [1,    4,    2,       2,       2,       2,       2,         3,     3,     3,    3,     3] # controls: 1 = avergae, 2 = carbon store total, 3 = carbon flux: total and scale units
unit = ['K',  'mm day-1', 'PgC', 'PgC', 'PgC', 'PgC', 'PgC', 'PgC yr-1', 'PgC yr-1', 'PgC yr-1', 'PgC yr-1']
scenario = ['historical', 'ssp126', 'ssp370']
years    = ['1850-2014', '2015-2100', '2015-2100']

models = ['ACCESS-ESM1-5', 'BCC-CSM2-MR', 'BCC-ESM1', 'CAS-ESM2-0', 'CESM2-WACCM', 'CMCC-CM2-SR5', 'CMCC-ESM2', 'CNRM-ESM2-1', 'CanESM5',  'EC-Earth3-Veg', 'GFDL-ESM4', 'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KIOST-ESM', 'MIROC-ES2L', 'MPI-ESM1-2-LR', 'NorESM2-LM', 'NorESM2-MM', 'UKESM1-0-LL']
ripf =   ['r1i1p1f1',      'r1i1p1f1',    'r1i1p1f1', 'r1i1p1f1',   'r1i1p1f1',    'r1i1p1f1',     'r1i1p1f1',  'r1i1p1f2',    'r1i1p1f1', 'r1i1p1f1',      'r1i1p1f1',  'r1i1p1f1',  'r1i1p1f1',  'r1i1p1f1',     'r1i1p1f1',  'r1i1p1f2',   'r1i1p1f1',      'r1i1p1f1',   'r1i1p1f1', 'r1i1p1f2']


for v in [2,5]:
    out_file = 'Fig_6_7_'+var[v]+'_plume.jpg' 
    fig, axes = plt.subplots(3, 4, figsize = (16,12))
    
    for ax in axes[-1,:]:
        ax.set_xlabel('year', fontsize=14)
        
    for ax in axes[:,0]:    
        ax.set_ylabel(unit[v], fontsize=14)
            
# loop over regions
    reg_list_oneAfrica = [1,2,3,13,6,7,8,9,10,11]
    for reg_list in reg_list_oneAfrica:
        reg = names(reg_list)
        ax_pointer = reg_list-1
        if reg_list >3: ax_pointer = reg_list-2
        if reg_list == 13: ax_pointer = 3
        
        #print(reg_list, ax_pointer)
        ax = np.ravel(axes)[ax_pointer]
        if (reg_list == 6):
            ax.set_title('Russia', fontsize=16)    # prefered over "Oceania as used for all the analysis to date"
        elif (reg_list == 11):
            ax.set_title('Australasia', fontsize=16)    # prefered over "Oceania as used for all the analysis to date"
        else:
            ax.set_title(names(reg_list, tidy=True), fontsize=16)
        
        
        in_dir = 'DATA/Processed/' + reg+'/' 
        y_hist, y_126, y_370, var_array_hist, var_array_126, var_array_370 = \
            get_var_array(reg, var[v], table[v], proc[v], models, ripf, scenario, years)
        
        var_mean_hist = np.mean(var_array_hist,0)
        var_25_hist   = np.percentile(var_array_hist,25,0)
        var_75_hist   = np.percentile(var_array_hist,75,0)
        var_10_hist   = np.percentile(var_array_hist,10,0)
        var_90_hist   = np.percentile(var_array_hist,90,0)
        
        var_mean_126 = np.mean(var_array_126,0)
        var_25_126   = np.percentile(var_array_126,25,0)
        var_75_126   = np.percentile(var_array_126,75,0)
        var_10_126   = np.percentile(var_array_126,10,0)
        var_90_126   = np.percentile(var_array_126,90,0)
            
        var_mean_370 = np.mean(var_array_370,0)
        var_25_370   = np.percentile(var_array_370,25,0)
        var_75_370   = np.percentile(var_array_370,75,0)
        var_10_370   = np.percentile(var_array_370,10,0)
        var_90_370   = np.percentile(var_array_370,90,0)
        
        ax.fill_between(y_hist, var_10_hist, var_90_hist, facecolor='k', alpha=0.2)
        ax.fill_between(y_126, var_10_126, var_90_126, facecolor='b', alpha=0.2)
        ax.fill_between(y_370, var_10_370, var_90_370, facecolor='r', alpha=0.2)
        
        for t in var_array_hist:
            ax.plot(y_hist,t, 'k', lw=0.1)
        for t in var_array_126:
            ax.plot(y_126,t, 'b', lw=0.1)
        for t in var_array_370:
            ax.plot(y_370,t, 'r', lw=0.1)
            
        ax.plot(y_370, var_mean_370, 'r', lw=3, label='SSP3-7.0')
        ax.plot(y_126, var_mean_126, 'b', lw=3, label='SSP1-2.6')
        ax.plot(y_hist, var_mean_hist, 'k', lw=3, label='Historical')
        ax.axhline(ls='--', color='k', lw=.5)
    
        # set common y-range
        if v == 2 : ax.set_ylim(-35,70)
        if v == 5 : ax.set_ylim(-20,40)
        
        if reg_list == 1 :
            ax.legend(fontsize=14)
        
    # don't show axes of final 2
    ax = np.ravel(axes)[10]; ax.axis('off')
    ax = np.ravel(axes)[11]; ax.axis('off')
        
    plt.savefig(out_file)
    plt.close()
