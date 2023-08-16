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

fig, ((ax1, ax2),(ax3, ax4)) = plt.subplots(2, 2, sharex='col', sharey='row', figsize = (14,14))
plt.subplots_adjust(wspace=0, hspace=0)

ts=18
fs=14

for ax in [ax1, ax2, ax3, ax4]:
    ax.set_xlim(0,6)
    ax.set_ylim(0,1280)
    ax.tick_params(axis='y', labelsize=fs)
    ax.set_xticklabels([])

ax1.set_title('a) SSP1-2.6, 2015-2050', x=0.3, y=0.9, fontsize=ts)
ax2.set_title('b) SSP1-2.6, 2015-2100', x=0.3, y=0.9, fontsize=ts)
ax3.set_title('c) SSP3-7.0, 2015-2050', x=0.3, y=0.9, fontsize=ts)
ax4.set_title('d) SSP3-7.0, 2015-2100', x=0.3, y=0.9, fontsize=ts)

ax1.set_ylabel('ppm', fontsize=fs)
ax3.set_ylabel('ppm', fontsize=fs)

# colours
col_co2  = '#d1e0ee'
col_ff   = '#7f3300'
col_land = '#66bf7d'
col_ocn  = '#506fba'

# ssp126, 2015-2050
co2_0 = 399.9
co2_1 = 469.0

dco2 = co2_1 - co2_0
land = 98.9 / 2.12
ocn = 84.9 / 2.12
emiss = dco2 + land + ocn

ax1.bar(0.5, co2_0, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_co2)
ax1.bar(1.5, emiss, width=0.8, bottom=co2_0, align='edge', edgecolor='k', color=col_ff)
ax1.bar(2.5, -land, width=0.8, bottom=co2_0+emiss, align='edge', edgecolor='k', color=col_land)
ax1.bar(3.5, -ocn, width=0.8, bottom=co2_0+emiss-land, align='edge', edgecolor='k', color=col_ocn)
ax1.bar(4.5, co2_1, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_co2)

ax1.text(0.65,300, str(co2_0))
ax1.text(0.65,260, 'ppm')
ax1.text(4.65,400, str(co2_1))
ax1.text(4.65,360, 'ppm')

ax1.text(1.65, co2_0+emiss-100, '+'+str(int(emiss)), color='w')
ax1.text(2.65, co2_0+emiss-100, '-'+str(int(land)), color='k')
ax1.text(3.65, co2_0+emiss-land-100, '-'+str(int(ocn)), color='k')

# ssp126, 2015-2100
co2_0 = 399.9
co2_1 = 445.5

dco2 = co2_1 - co2_0
land = 173.7 / 2.12
ocn = 139.4 / 2.12
emiss = dco2 + land + ocn

ax2.bar(0.5, co2_0, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_co2)
ax2.bar(1.5, emiss, width=0.8, bottom=co2_0, align='edge', edgecolor='k', color=col_ff)
ax2.bar(2.5, -land, width=0.8, bottom=co2_0+emiss, align='edge', edgecolor='k', color=col_land)
ax2.bar(3.5, -ocn, width=0.8, bottom=co2_0+emiss-land, align='edge', edgecolor='k', color=col_ocn)
ax2.bar(4.5, co2_1, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_co2)

ax2.text(0.65,300, str(co2_0))
ax2.text(0.65,260, 'ppm')
ax2.text(4.65,380, str(co2_1))
ax2.text(4.65,340, 'ppm')

ax2.text(1.65, co2_0+emiss-100, '+'+str(int(emiss)), color='w')
ax2.text(2.65, co2_0+emiss-70, '-'+str(int(land)), color='k')
ax2.text(3.65, co2_0+emiss-land-60, '-'+str(int(ocn)), color='w')

# ssp370, 2015-2050
co2_0 = 399.9
co2_1 = 540.0

dco2 = co2_1 - co2_0
land = 92.8 / 2.12
ocn = 112.3 / 2.12
emiss = dco2 + land + ocn

ax3.bar(0.5, co2_0, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_co2)
ax3.bar(1.5, emiss, width=0.8, bottom=co2_0, align='edge', edgecolor='k', color=col_ff)
ax3.bar(2.5, -land, width=0.8, bottom=co2_0+emiss, align='edge', edgecolor='k', color=col_land)
ax3.bar(3.5, -ocn, width=0.8, bottom=co2_0+emiss-land, align='edge', edgecolor='k', color=col_ocn)
ax3.bar(4.5, co2_1, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_co2)

ax3.text(0.65,300, str(co2_0))
ax3.text(0.65,260, 'ppm')
ax3.text(4.65,480, str(co2_1))
ax3.text(4.65,440, 'ppm')

ax3.text(1.65, co2_0+emiss-100, '+'+str(int(emiss)), color='w')
ax3.text(2.65, co2_0+emiss-100, '-'+str(int(land)), color='k')
ax3.text(3.65, co2_0+emiss-land-100, '-'+str(int(ocn)), color='k')

# ssp126, 2015-2050
co2_0 = 399.9
co2_1 = 866.2

dco2 = co2_1 - co2_0
land = 227.8 / 2.12
ocn = 316.1 / 2.12
emiss = dco2 + land + ocn

ax4.bar(0.5, co2_0, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_co2)
ax4.bar(1.5, emiss, width=0.8, bottom=co2_0, align='edge', edgecolor='k', color=col_ff)
ax4.bar(2.5, -land, width=0.8, bottom=co2_0+emiss, align='edge', edgecolor='k', color=col_land)
ax4.bar(3.5, -ocn, width=0.8, bottom=co2_0+emiss-land, align='edge', edgecolor='k', color=col_ocn)
ax4.bar(4.5, co2_1, width=0.8, bottom=0, align='edge', edgecolor='k', color=col_co2)

ax4.text(0.65,300, str(co2_0))
ax4.text(0.65,260, 'ppm')
ax4.text(4.65,800, str(co2_1))
ax4.text(4.65,760, 'ppm')

ax4.text(1.65, co2_0+emiss-100, '+'+str(int(emiss)), color='w')
ax4.text(2.65, co2_0+emiss-80, '-'+str(int(land)), color='k')
ax4.text(3.65, co2_0+emiss-land-100, '-'+str(int(ocn)), color='w')


# key
ax1.bar(.8, 180, width=4.2, bottom=860, align='edge', edgecolor='k', color='w')
ax1.bar( 1, 100, width=0.8, bottom=900, align='edge', edgecolor='k', color=col_co2)
ax1.bar( 2, 100, width=0.8, bottom=900, align='edge', edgecolor='k', color=col_ff)
ax1.bar( 3, 100, width=0.8, bottom=900, align='edge', edgecolor='k', color=col_land)
ax1.bar( 4, 100, width=0.8, bottom=900, align='edge', edgecolor='k', color=col_ocn)

ax1.text(1.1, 940, 'CO$_2$', fontsize=fs)
ax1.text(2.1, 940, 'Emiss', fontsize=fs, color='w')
ax1.text(3.1, 940, 'Land', fontsize=fs)
ax1.text(4.1, 940, 'Ocean', fontsize=fs, color='w')

ax3.text(.4, -80, 'Atmos in 2015', fontsize=fs)
ax3.text(4, -80, 'Atmos in 2050', fontsize=fs)
ax4.text(.4, -80, 'Atmos in 2015', fontsize=fs)
ax4.text(4, -80, 'Atmos in 2100', fontsize=fs)

plt.savefig('Fig5_Global_waterfall.jpg')

plt.close()
