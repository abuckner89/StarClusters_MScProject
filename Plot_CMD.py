#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 24 10:27:27 2026

plots cluster photometry in a near-infrared colour–magnitude diagram and overlays extinction- and distance-corrected isochrones for comparison. It uses user-defined cluster distance and E(B−V) values to convert theoretical absolute magnitudes into apparent JHK magnitudes, helping estimate the cluster age by comparing the observed sequence with stellar evolution models.

NB: Code assumes the isochrones are in absolute J and K magnitudes with Av=0

@author: spxab4
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Cluster JHK photometry 
cluster=pd. read_csv("my_merged_catalogue.csv")
J_cl, K_cl = cluster["J"], cluster["K"]
JK_cl = J_cl - K_cl

#User-defined cluster parameters
d_pc = # cluster distance in parsecs
E_BV = # cluster E(B-V)

#Stellar evolutionary isochrone tracks
iso1 = pd.read_csv("Isochrone_age1.csv")
iso2 = pd.read_csv("Isochrone2_age2.csv")

# distance modulus
mu = 5*np.log10(d_pc/10) 

# Extinction from Table 3 of Rieke & Lebofsky (1985)
R_V = 3.09
A_V = R_V * E_BV # Rv*E(B-V)
A_J=0.282 * A_V 
A_H= 0.175 * A_V
A_K= 0.112 * A_V

# color excess
E_JK = A_J - A_K

# Converting isochrones from absolute to apparent JHK magnitudes
iso1["K_app"] = iso1["Kmag"] + mu + A_K
iso1["JK_app"] = (iso1["Jmag"] - iso1["Kmag"]) + E_JK 

iso2["K_app"] = iso2["Kmag"] + mu + A_K
iso2["JK_app"] = (iso2["Jmag"] - iso2["Kmag"]) + E_JK 

#plotting J-K vs K with isochrones overlaid
plt.scatter(JK_cl, K_cl, s=8, alpha=0.6, label="Cluster stars")
plt.plot(iso1["JK_app"], iso1["K_app"], label="Isochrone 1")
plt.plot(iso2["JK_app"], iso2["K_app"], label="Isochrone 2")
plt.gca().invert_yaxis() #convention of brightest stars being at top of axis
plt.xlabel("J - K")
plt.ylabel("K (mag)")
plt.legend()
plt.show()
