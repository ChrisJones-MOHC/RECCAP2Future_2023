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
returns weighted area average of a cube
'''
def area_avg(x):
   # If the cube does not have bounds, add bounds
   if not x.coord('latitude').has_bounds():
        x.coord('latitude').guess_bounds()
   if not x.coord('longitude').has_bounds():
        x.coord('longitude').guess_bounds()
   #Get the area weights using the same cube  
   area = iris.analysis.cartography.area_weights(x, normalize=False)

   #Now collapse the lat and lon to find a global mean over time
   return x.collapsed(['latitude','longitude'], iris.analysis.MEAN, weights=area).data


'''
outputs the list of region names
'''
def names(x):
    switcher = {
       1: 'North America',
       2: 'South America',
       3: 'Europe',
       4: 'Northern Africa',
       5: 'Southern Africa',
       6: 'Russia',
       7: 'Central Asia',
       8: 'East Asia',
       9: 'South Asia',
       10: 'South East Asia',
       11: 'Oceania',
       12: 'Oceans',
       13: 'Africa',
    }

    return switcher.get(x, "nothing")

'''
masks a cube by the input sector number
'''
def reccap_mask(cube, region):
   mask = iris.load('DATA/RECCAP_AfricaSplit_MASK11_Mask_regridded.nc')[0]
   if (region <= 12):
       land_mask = (mask.data != region)
   elif (region == 13):  # glue all Africa together
       land_mask = (mask.data != 4) & (mask.data != 5)

   n = len(cube.coord('time').points)
   b = np.repeat(land_mask[np.newaxis, :, :], n, axis=0)
   cube_masked = cube.copy()
   cube_masked.data = ma.array(cube.data, mask=b)

   return cube_masked

#
#--------------------------------------------------------------------
#

# read in netcdf files of land use (crop and pasture)
dir = 'DATA/CMIP6_LU_Forcing/'
crop_hist = iris.load(dir+'multiple_input4MIPs_landState_CMIP_UofMD-landState-2-1-h_gn_0850-2015_states.nc_1848_2015_crop_frac_noRange_n96e_orca1_ancil.nc')[0]
past_hist = iris.load(dir+'multiple_input4MIPs_landState_CMIP_UofMD-landState-2-1-h_gn_0850-2015_states.nc_1848_2015_pasture_frac_noRange_n96e_orca1_ancil.nc')[0]
crop_370 = iris.load(dir+'LUC_2014_2101_ssp370_time_series_crop_frac_noRange_n96e_orca1_ancil.nc')[0]
past_370 = iris.load(dir+'LUC_2014_2101_ssp370_time_series_pasture_frac_noRange_n96e_orca1_ancil.nc')[0]
crop_126 = iris.load(dir+'LUC_2014_2101_ssp126_time_series_crop_frac_noRange_n96e_orca1_ancil.nc')[0]
past_126 = iris.load(dir+'LUC_2014_2101_ssp126_time_series_pasture_frac_noRange_n96e_orca1_ancil.nc')[0]

# combine to total
lu_hist = crop_hist + past_hist
lu_370 = crop_370 + past_370
lu_126 = crop_126 + past_126

# read in RECCAP2 mask and regrid land-use to it
mask = iris.load('DATA/RECCAP_AfricaSplit_MASK11_Mask_regridded.nc')[0]

# mask needs coord system re-setting:
mask.coord('latitude').coord_system = lu_370.coord('latitude').coord_system
mask.coord('longitude').coord_system = lu_370.coord('longitude').coord_system

lu_hist = lu_hist.regrid(mask, iris.analysis.Linear())
lu_370 = lu_370.regrid(mask, iris.analysis.Linear())
lu_126 = lu_126.regrid(mask, iris.analysis.Linear())

# extract years as array
yhist = np.array([x.year for x in lu_hist.coord('time').units.num2date(lu_hist.coord('time').points)])
yssp  = np.array([x.year for x in lu_370.coord('time').units.num2date(lu_370.coord('time').points)])


# set up plotting and output 
out_file = 'FigS1_LU_ssp.jpg' 

fig, axes = plt.subplots(3, 4, figsize = (16,12))

for ax in axes[-1,:]:
    ax.set_xlabel('year', fontsize=14)
    
for ax in axes[:,0]:
    ax.set_ylabel('frac', fontsize=14)
    
# loop over regions - need to just get all Africa, not split north/south
reg_list_oneAfrica = [1,2,3,13,6,7,8,9,10,11]

for reg in reg_list_oneAfrica:
    ax_pointer = reg-1
    if reg >3: ax_pointer = reg-2
    if reg == 13: ax_pointer = 3

    ax = np.ravel(axes)[ax_pointer]
    if (reg == 11):
        ax.set_title('Australasia', fontsize=16)
    else:
        ax.set_title(names(reg), fontsize=16)
    
    ax.plot(yssp, area_avg(reccap_mask(lu_370,reg)), 'r', lw=3, label='SSP3-7.0')
    ax.plot(yssp, area_avg(reccap_mask(lu_126,reg)), 'b', lw=3, label='SSP1-2.6')
    ax.plot(yhist, area_avg(reccap_mask(lu_hist,reg)), 'k', lw=3, label='Historical')

# set common y-axis for ease of comparison across panels
    ax.set_ylim(0,.6)
    
    if reg == 1:
        ax.legend(fontsize=14)
        
# don't show axes of final 2
ax = np.ravel(axes)[10]; ax.axis('off')
ax = np.ravel(axes)[11]; ax.axis('off')

plt.savefig(out_file)

plt.close()
