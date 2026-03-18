# ----------------------------------------------------
# PROGRAM TO MERGE 2MASS AND VISTA/UKIDSS DATA
# ----------------------------------------------------

#!/usr/bin/env python3
"""
Merge 2MASS (K<12.5) and VISTA/UKIDSS (K>12.5) data for a cluster.
Matches by coordinates and J/H/K (with uncertainties),
removes duplicates near K~12, always keeping 2MASS when matched.

2MASS J H and Ks photometry should be converted to the VISTA/UKIDSS system prior to running this code.
"""

import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
from astropy import units as u

# -------------------------------------------------------------------------
# Function check if two magnitudes agree within combined uncertainty
# -------------------------------------------------------------------------
def within_error(m1, e1, m2, e2, nsig=3.0):
    """Return True if |m1 - m2| <= nsig * sqrt(e1^2 + e2^2)."""
    if np.isnan(m1) or np.isnan(m2):
        return False
    if np.isnan(e1):
        e1 = 0.0
    if np.isnan(e2):
        e2 = 0.0
    combined_err = np.sqrt(e1**2 + e2**2)
    if combined_err == 0:
        combined_err = 0.02
    return abs(m1 - m2) <= nsig * combined_err


#
# ----------------------------------------------------
# 1. USER SETTINGS: column names for each catalogue
# ----------------------------------------------------
#IMPORTANT: 2MASS JHK colours and uncertainites should be converted to VISTA/UKIDSS system prior to running code.

#You will need to change the column names to match those in your files

# 2MASS column names
cols_2mass = {
    "ra": "RA",#RA in degress, J2000
    "dec": "DEC",#Dec in J2000
    "J": "J_mag",# J mag
    "H": "H_mag",# H mag
    "K": "K_mag",# K mag
    "e_J": "Jmag_u",#uncertainity in J
    "e_H": "Hmag_u",#uncertainity in H
    "e_K": "Kmag_u"#uncertainity in K
}

# VISTA or UKIDSS column names
cols_vu = {
    "ra": "RA",#RA in degress, J2000
    "dec": "DEC",#Dec in J2000
    "J": "J_mag",# J mag
    "H": "H_mag",# H mag
    "K": "K_mag",# K mag
    "e_J": "Jmag_u",#uncertainity in J
    "e_H": "Hmag_u",#uncertainity in H
    "e_K": "Kmag_u"#uncertainity in K
}

# Your input files
file_2mass = "./my_2mass_converted.csv" #2MASS file
file_vu = "./my_ukidss_or_vista.csv" #VISTA/UKIDSS file


# ----------------------------------------------------
# 2. READ AND RENAME COLUMNS TO COMMON NAMES
# ----------------------------------------------------
t = pd.read_csv(file_2mass, index_col=False)
vu = pd.read_csv(file_vu, index_col=False)

print(vu)

t = t.rename(columns={t_old: t_new for t_new, t_old in cols_2mass.items()})
vu = vu.rename(columns={vu_old: vu_new for vu_new, vu_old in cols_vu.items()})


# ----------------------------------------------------
# 3. BUILD SkyCoord OBJECTS
# ----------------------------------------------------

# Select radius to cross match 2MASS and VISTA/UKIDSS point sources
match_radius=0.5 * u.arcsec # recommended: Globulars 0.3-0.5", Open 0.8-1.0"

# Build SkyCoord objects for both catalogues
tcoord = SkyCoord(t["ra"].values * u.deg, t["dec"].values * u.deg)
vucoord = SkyCoord(vu["ra"].values * u.deg, vu["dec"].values * u.deg)

# Cross-match VISTA/UKIDSS sources to 2MASS sources
idx, sep2d, _ = vucoord.match_to_catalog_sky(tcoord)
is_pos_match = sep2d < match_radius

# Initialise array to mark VISTA/UKIDSS sources to drop
drop_vu = np.zeros(len(vu), dtype=bool)


# ----------------------------------------------------
# 5. LOOP AND REMOVE DUPLICATES (ALWAYS KEEP 2MASS)
# ----------------------------------------------------

for j, matched in enumerate(is_pos_match):
    if not matched:
        continue

    i = idx[j]
    trow = t.iloc[i]
    vrow = vu.iloc[j]

    # Check agreement in J, H, K (within photometric errors)
    j_match = within_error(trow["J"], trow["e_J"], vrow["J"], vrow["e_J"])
    h_match = within_error(trow["H"], trow["e_H"], vrow["H"], vrow["e_H"])
    k_match = within_error(trow["K"], trow["e_K"], vrow["K"], vrow["e_K"])

    # Require agreement in at least two bands to call it a duplicate
    matches = [j_match, h_match, k_match]
    nmatch = sum(matches)

    if nmatch >= 2:
        drop_vu[j] = True  # duplicate found -> drop the UKIDSS entry


# ----------------------------------------------------
# 6. MERGE AND SAVE
# ----------------------------------------------------
print(f"Number of duplicates found {int(drop_vu.sum())}")

vu_keep = vu.loc[~drop_vu].copy()

# Tag the catalogue origin for clarity
t["cat"] = "2MASS"
vu_keep["cat"] = "VISTA/UKIDSS"

# Combine, sort, and save
merged = pd.concat([t, vu_keep], ignore_index=True)
merged = merged.sort_values(by="K").reset_index(drop=True)

merged.to_csv("my_merged_catalogue.csv", index=False)
print(f"Merged catalogue written with {len(merged)} sources (duplicates removed).")