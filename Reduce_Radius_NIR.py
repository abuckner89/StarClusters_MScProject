# ----------------------------------------------------
# PROGRAM TO RADIALLY TRIM 2MASS+VISTA/UKIDSS DATA
# ----------------------------------------------------

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 16 13:31:00 2026

Applies a radial cut to a photometric catalogue, selecting only sources within a user-specified radius (new_rad_arcmin) from data originally downloaded over a larger radius, and plots the output in Ra/Dec parameter space.

@author: spxab4 (Anne S.M. Buckner)
"""

####################
#packages
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

####################
#radial selection function
def cone_search(df, ra0_deg, dec0_deg, radius_deg, ra_col="ra", dec_col="dec"):
    ra  = np.deg2rad(df[ra_col].to_numpy())
    dec = np.deg2rad(df[dec_col].to_numpy())
    ra0  = np.deg2rad(ra0_deg)
    dec0 = np.deg2rad(dec0_deg)
    r    = np.deg2rad(radius_deg)

    dra  = ra - ra0
    ddec = dec - dec0

    a = np.sin(ddec/2)**2 + np.cos(dec)*np.cos(dec0)*np.sin(dra/2)**2
    ang = 2*np.arcsin(np.sqrt(a))

    return df.loc[ang <= r]

####################
#full data
df_merged=pd.read_csv('./my_merged_catalogue.csv')

#ra and dec of stars in full data
ra_=df_merged['ra']
dec_=df_merged['dec']

#new smaller radius
new_rad_arcmin=
new_rad_degrees=new_rad_arcmin/60.

#central coordiantes
ra_cent=min(ra_)+((max(ra_)-min(ra_))/2.)
dec_cent=min(dec_)+((max(dec_)-min(dec_))/2.)
    
#radial trim of data
df_trimmed= cone_search(df_merged, ra0_deg=ra_cent, dec0_deg=dec_cent, radius_deg=new_rad_degrees)
print('Number of stars (before:)', len(df_merged), '(after:)',len(df_trimmed))
        
#save trimmed data to file
df_trimmed.to_csv('./my_merged_catalogue_rtrim.csv', index=False)
 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#sanity check
ax = plt.subplot()
plt.scatter(ra_, dec_, marker='.', s=2., c='gray', label='before')
plt.scatter(df_trimmed["ra"], df_trimmed["dec"], marker='+', s=20., c='blue', label='after')
plt.xlim(max(ra_), min(ra_))
plt.ylim(min(dec_), max(dec_))
plt.minorticks_on()
plt.xlabel('R.A. [deg]')
plt.ylabel('Dec [deg]')
plt.legend(fontsize='x-small')
plt.savefig('./my_merged_catalogue_rtrim.jpg', dpi=1200., bbox_inches='tight')
plt.clf()
plt.close()
        
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
