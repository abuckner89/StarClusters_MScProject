# StarClusters_MScProject
Python tools for characterising stellar populations in Galactic clusters through near-infrared photometry, including catalogue merging, photometric-system conversion, CMD generation, and isochrone-based age estimation.

# Stellar Cluster NIR Analysis

Python codes for analysing Galactic open and globular star clusters using near-infrared photometry from 2MASS, VISTA, and UKIDSS. The pipeline combines catalogue photometry, applies photometric-system conversions, constructs colour–magnitude diagrams, and fits stellar isochrones to estimate cluster ages. 

## Project overview

This repository contains code developed for a MSc stellar cluster microproject focused on:
- retrieving and combining J, H, and K-band photometric data,
- merging shallow and deep survey catalogues,
- constructing near-infrared CMDs,
- applying extinction corrections,
- and estimating cluster ages through isochrone fitting.

The scientific aim is to compare open and globular clusters through their photometric properties and infer ages with realistic uncertainty estimates. 

## Main features

- Photometric catalogue handling for 2MASS, VISTA, and UKIDSS
- Cross-matching and merging of survey data
- Photometric-system transformations with uncertainty propagation
- Construction of colour–magnitude and colour–colour diagrams
- Extinction and reddening corrections in the near-infrared
- Isochrone overlay and age estimation
- Basic error analysis and comparison with literature values. 

## Typical workflow

1. Determine cluster centre and radius.
2. Retrieve point-source photometry from survey archives.
3. Apply quality cuts to the catalogues.
4. Convert all photometry onto a consistent system if needed.
5. Merge 2MASS with VISTA/UKIDSS data.
6. Build CMDs and colour–colour diagrams.
7. Apply distance and extinction corrections.
8. Overlay isochrones and estimate cluster ages.
9. Evaluate uncertainties and compare with literature values.

## Requirements

Typical Python packages used in this project include:

- `numpy`
- `pandas`
- `matplotlib`
- `astropy` 

Additional astronomy packages may also be useful depending on your workflow.

## Notes

- Bright stars (Ks<12 mag) are taken from 2MASS, while deeper VISTA/UKIDSS data are used for fainter sources.
- Extinction conversions should be applied consistently within a single extinction law.
- Age estimates depend on photometric quality, reddening, distance modulus, and isochrone choice.

## Acknowledgements

This repository was developed as part of an MSc microproject at Cardiff University focused on estimating the ages of Galactic star clusters from near-infrared photometric data. An earlier version of this project, with some differences in scope and implementation, was originally offered as a third-year BSc/MSci project at the University of Leeds.
