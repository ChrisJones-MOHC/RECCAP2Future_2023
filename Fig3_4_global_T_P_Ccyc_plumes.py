import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import glob
import os
import sys

# developed and tested at Python version is 3.8.13

def get_var_array(reg, var, table, proc, models, ripf, scenario, years):
    
    var_array_hist = []
    var_array_126  = []
    var_array_370  = []
    
    for m in np.arange(len(models)):
        file_hist = scenario[0]+'/'+'CMIP6_'+models[m]+'_'+table+'_'+scenario[0]+'_'+ripf[m]+'_'+var+'_'+reg+'_'+years[0]+'.txt'
        file_126  = scenario[1]+'/'+'CMIP6_'+models[m]+'_'+table+'_'+scenario[1]+'_'+ripf[m]+'_'+var+'_'+reg+'_'+years[1]+'.txt'
        file_370  = scenario[2]+'/'+'CMIP6_'+models[m]+'_'+table+'_'+scenario[2]+'_'+ripf[m]+'_'+var+'_'+reg+'_'+years[2]+'.txt'

        if (os.path.isfile(in_dir+file_hist)):
            y_hist, val_hist = np.loadtxt(in_dir+file_hist).T
            if (proc == 2):
                off = val_hist[0]
            else:
                off = np.mean(val_hist[0:51])

            val_hist = val_hist - off
            var_array_hist.append(val_hist)
            
        if (os.path.isfile(in_dir+file_126)):
            y_126, val_126 = np.loadtxt(in_dir+file_126).T
            val_126 = val_126 - off
            var_array_126.append(val_126)
            
        if (os.path.isfile(in_dir+file_370)):
            y_370, val_370 = np.loadtxt(in_dir+file_370).T
            val_370 = val_370 - off
            var_array_370.append(val_370)

    return y_hist, y_126, y_370, var_array_hist, var_array_126, var_array_370


# scenarios and variables

var = ['tas', 'pr', 'cVeg', 'cLitter', 'cProduct', 'cSoil', 'cLand', 'gpp', 'npp', 'rh', 'nbp', 'fgco2']
table = ['Amon', 'Amon', 'Lmon', 'Lmon', 'Lmon', 'Emon', 'Emon', 'Lmon', 'Lmon', 'Lmon', 'Lmon', 'Omon']
proc = [1,    4,    2,       2,       2,       2,       2,         3,     3,     3,    3,     3] # controls: 1 = avergae, 2 = carbon store total, 3 = carbon flux: total and scale units
unit = ['K',  'mm day-1', 'PgC', 'PgC', 'PgC', 'PgC', 'PgC', 'PgC yr-1', 'PgC yr-1', 'PgC yr-1', 'PgC yr-1', 'PgC yr-1']
scenario = ['historical', 'ssp126', 'ssp370']
years    = ['1850-2014', '2015-2100', '2015-2100']

models = ['ACCESS-ESM1-5', 'BCC-CSM2-MR', 'BCC-ESM1', 'CAS-ESM2-0', 'CESM2-WACCM', 'CMCC-CM2-SR5', 'CMCC-ESM2', 'CNRM-ESM2-1', 'CanESM5',  'EC-Earth3-Veg', 'GFDL-ESM4', 'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR', 'KIOST-ESM', 'MIROC-ES2L', 'MPI-ESM1-2-LR', 'NorESM2-LM', 'NorESM2-MM', 'UKESM1-0-LL']
ripf =   ['r1i1p1f1',      'r1i1p1f1',    'r1i1p1f1', 'r1i1p1f1',   'r1i1p1f1',    'r1i1p1f1',     'r1i1p1f1',  'r1i1p1f2',    'r1i1p1f1', 'r1i1p1f1',      'r1i1p1f1',  'r1i1p1f1',  'r1i1p1f1',  'r1i1p1f1',     'r1i1p1f1',  'r1i1p1f2',   'r1i1p1f1',      'r1i1p1f1',   'r1i1p1f1', 'r1i1p1f2']

reg = 'Global'
in_dir = 'DATA/Processed/' + reg+'/' 

#########################################################
#
# Fig 2. Global tas and pr


f, (ax1, ax2) = plt.subplots(1,2, figsize = (16,8))

# titles and x/y labels etc
ts = 24
fs = 20
ax1.set_title("a) Global surface air temperature", fontsize=ts)
ax2.set_title("b) Global precipitation", fontsize=ts)

ax1.set_xlabel('year', fontsize=fs)
ax2.set_xlabel('year', fontsize=fs)
ax1.set_ylabel('K', fontsize=fs)
ax2.set_ylabel('mm / day', fontsize=fs)

for a in [ax1, ax2]:
    a.tick_params(axis='both', labelsize=fs)
    a.axhline(color='grey', ls='--', lw=1)

# panel 1: tas
v = 0 # tas

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

ax1.fill_between(y_hist, var_10_hist, var_90_hist, facecolor='k', alpha=0.2)
ax1.fill_between(y_126, var_10_126, var_90_126, facecolor='b', alpha=0.2)
ax1.fill_between(y_370, var_10_370, var_90_370, facecolor='r', alpha=0.2)

for t in var_array_hist:
    ax1.plot(y_hist,t, 'k', lw=0.1)
for t in var_array_126:
    ax1.plot(y_126,t, 'b', lw=0.1)
for t in var_array_370:
    ax1.plot(y_370,t, 'r', lw=0.1)

ax1.plot(y_370, var_mean_370, 'r', lw=3, label='SSP3-7.0')
ax1.plot(y_126, var_mean_126, 'b', lw=3, label='SSP1-2.6')
ax1.plot(y_hist, var_mean_hist, 'k', lw=3, label='Historical')

# panel 2: pr
v = 1 # pr

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

ax2.fill_between(y_hist, var_10_hist, var_90_hist, facecolor='k', alpha=0.2)
ax2.fill_between(y_126, var_10_126, var_90_126, facecolor='b', alpha=0.2)
ax2.fill_between(y_370, var_10_370, var_90_370, facecolor='r', alpha=0.2)

for t in var_array_hist:
    ax2.plot(y_hist,t, 'k', lw=0.1)
for t in var_array_126:
    ax2.plot(y_126,t, 'b', lw=0.1)
for t in var_array_370:
    ax2.plot(y_370,t, 'r', lw=0.1)

ax2.plot(y_370, var_mean_370, 'r', lw=3, label='SSP3-7.0')
ax2.plot(y_126, var_mean_126, 'b', lw=3, label='SSP1-2.6')
ax2.plot(y_hist, var_mean_hist, 'k', lw=3, label='Historical')


ax1.legend(fontsize=fs)
#plt.savefig('Fig3_global_tas_pr_plumes.png')
plt.savefig('Fig3_global_tas_pr_plumes.jpg')



#########################################################
#
# Fig 3. Global C-cycle

f, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize = (16,10))
plt.subplots_adjust(wspace=0, hspace=0)

# titles and x/y labels etc
ts = 18
fs = 14
ax1.set_title("a) Vegetation carbon", x=0.3, y=0.9, fontsize=ts)
ax2.set_title("b) Soil carbon", x=0.2, y=0.9, fontsize=ts)
ax3.set_title("c) net Land flux", x=0.2, y=0.9, fontsize=ts)
ax4.set_title("d) net Ocean flux", x=0.25, y=0.9, fontsize=ts)

ax3.set_xlabel('year', fontsize=fs)
ax4.set_xlabel('year', fontsize=fs)
ax1.set_ylabel('PgC', fontsize=fs)
ax3.set_ylabel('PgC yr$^{-1}$', fontsize=fs)

for a in [ax1, ax2, ax3, ax4]:
    a.tick_params(axis='both', labelsize=fs)
    a.axhline(color='grey', ls='--', lw=1)

ax3.set_ylim(-4,10)

# panel 1: cVeg
v = 2

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

ax1.fill_between(y_hist, var_10_hist, var_90_hist, facecolor='k', alpha=0.2)
ax1.fill_between(y_126, var_10_126, var_90_126, facecolor='b', alpha=0.2)
ax1.fill_between(y_370, var_10_370, var_90_370, facecolor='r', alpha=0.2)

for t in var_array_hist:
    ax1.plot(y_hist,t, 'k', lw=0.1)
for t in var_array_126:
    ax1.plot(y_126,t, 'b', lw=0.1)
for t in var_array_370:
    ax1.plot(y_370,t, 'r', lw=0.1)

ax1.plot(y_370, var_mean_370, 'r', lw=3, label='SSP3-7.0')
ax1.plot(y_126, var_mean_126, 'b', lw=3, label='SSP1-2.6')
ax1.plot(y_hist, var_mean_hist, 'k', lw=3, label='Historical')

# panel 2: cSoil
v = 5

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

ax2.fill_between(y_hist, var_10_hist, var_90_hist, facecolor='k', alpha=0.2)
ax2.fill_between(y_126, var_10_126, var_90_126, facecolor='b', alpha=0.2)
ax2.fill_between(y_370, var_10_370, var_90_370, facecolor='r', alpha=0.2)

for t in var_array_hist:
    ax2.plot(y_hist,t, 'k', lw=0.1)
for t in var_array_126:
    ax2.plot(y_126,t, 'b', lw=0.1)
for t in var_array_370:
    ax2.plot(y_370,t, 'r', lw=0.1)

ax2.plot(y_370, var_mean_370, 'r', lw=3, label='SSP3-7.0')
ax2.plot(y_126, var_mean_126, 'b', lw=3, label='SSP1-2.6')
ax2.plot(y_hist, var_mean_hist, 'k', lw=3, label='Historical')

# panel 3: nbp
v = 10

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

ax3.fill_between(y_hist, var_10_hist, var_90_hist, facecolor='k', alpha=0.2)
ax3.fill_between(y_126, var_10_126, var_90_126, facecolor='b', alpha=0.2)
ax3.fill_between(y_370, var_10_370, var_90_370, facecolor='r', alpha=0.2)

for t in var_array_hist:
    ax3.plot(y_hist,t, 'k', lw=0.1)
for t in var_array_126:
    ax3.plot(y_126,t, 'b', lw=0.1)
for t in var_array_370:
    ax3.plot(y_370,t, 'r', lw=0.1)

ax3.plot(y_370, var_mean_370, 'r', lw=3, label='SSP3-7.0')
ax3.plot(y_126, var_mean_126, 'b', lw=3, label='SSP1-2.6')
ax3.plot(y_hist, var_mean_hist, 'k', lw=3, label='Historical')

# panel 4: fgco2
v = 11

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

ax4.fill_between(y_hist, var_10_hist, var_90_hist, facecolor='k', alpha=0.2)
ax4.fill_between(y_126, var_10_126, var_90_126, facecolor='b', alpha=0.2)
ax4.fill_between(y_370, var_10_370, var_90_370, facecolor='r', alpha=0.2)

for t in var_array_hist:
    ax4.plot(y_hist,t, 'k', lw=0.1)
for t in var_array_126:
    ax4.plot(y_126,t, 'b', lw=0.1)
for t in var_array_370:
    ax4.plot(y_370,t, 'r', lw=0.1)

ax4.plot(y_370, var_mean_370, 'r', lw=3, label='SSP3-7.0')
ax4.plot(y_126, var_mean_126, 'b', lw=3, label='SSP1-2.6')
ax4.plot(y_hist, var_mean_hist, 'k', lw=3, label='Historical')

# GCP estimates for S_Land, S_Ocean
#
ax3.errorbar(2015, 3.1, yerr=0.6, xerr=5, fmt='o', color='g')
ax4.errorbar(2015, 2.9, yerr=0.4, xerr=5, fmt='o', color='g')

ax2.legend(fontsize=fs)
#plt.savefig('Fig4_global_Ccyc_plumes.png')
plt.savefig('Fig4_global_Ccyc_plumes.jpg')
