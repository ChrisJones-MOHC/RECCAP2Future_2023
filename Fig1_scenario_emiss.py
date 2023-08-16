import numpy as np
import matplotlib.pyplot as plt
import iris
import iris.plot as iplt
import iris.quickplot as qplt
import glob
import os
import sys

# developed and tested at Python version is 3.8.13

# SSP future CO2 emissions taken from IIASA web page:
# https://tntcat.iiasa.ac.at/SspDb/dsd?Action=htmlpage&page=50
'''
World 	AIM/CGE - SSP3-70 (Baseline) 	CMIP6 Emissions|CO2 	Mt CO2/yr 	39148.758 	44808.038 	52847.359 	58497.970 	62904.059 	66568.368 	70041.979 	73405.226 	77799.049 	82725.833
World 	IMAGE - SSP1-26 	CMIP6 Emissions|CO2 	Mt CO2/yr 	39152.726 	39804.013 	34734.424 	26509.183 	17963.539 	10527.979 	4476.328 	-3285.043 	-8385.183 	-8617.786
'''

y = np.array([2015, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100])
e_370 = np.array([39148.758, 44808.038, 52847.359, 58497.970, 62904.059, 66568.368, 70041.979, 73405.226, 77799.049, 82725.833])
e_126 = np.array([39152.726, 39804.013, 34734.424, 26509.183, 17963.539, 10527.979, 4476.328, -3285.043, -8385.183, -8617.786])

e_370 = e_370*12./44. * 1e-3
e_126 = e_126*12./44. * 1e-3

# historical emissions stored locally:
y_hist,e_hist = np.loadtxt('DATA/Fig1_emiss.dat',skiprows=1).T

# land-use emissions available from C4MIP website:
# https://c4mip.net/cmip6-experiments
LU_emiss = iris.load('DATA/CMIP6_C4MIP_landuse_emissions.nc')[0]

# create hist anthro emissions
e_hist_tot = e_hist+LU_emiss.data[1:]*1e-12

# add extra year to end of hist to avoid gap in plotting

y_hist = np.append(y_hist, y[0])
e_hist_tot = np.append(e_hist_tot, e_370[0])

# Plot figure
fig = plt.figure(figsize=(14, 8))

plt.plot(y,e_370, 'r', label='SSP3-7.0')
plt.plot(y,e_126, 'b', label='SSP1-2.6')
plt.plot(y_hist,e_hist_tot, 'k', label='historical')

plt.fill_between([2040,2060], [-5,-5], [25,25], facecolor='#999999', alpha=0.3)
plt.fill_between([2080,2100], [-5,-5], [25,25], facecolor='#999999', alpha=0.3)

plt.axhline(0, color='k', lw=0.2)
plt.legend(fontsize=18)

plt.title('CO$_2$ emissions', fontsize=28)
plt.ylabel('PgC / yr', fontsize=20)
plt.xlabel('year', fontsize=20)

ax=plt.gca()
ax.tick_params(labelsize=18)

plt.xlim(1960,2102)
plt.ylim(-5,25)

plt.savefig('Fig1_scenario_emiss.jpg')
