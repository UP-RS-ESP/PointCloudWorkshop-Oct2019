# From point clouds and full-waveform data to DEM analysis (Sep-30 to Oct-4 2019)
Point-cloud workshop at the University of Potsdam with support from the graduate school [StRATEGy](http://www.irtg-strategy.de/index/), the [University of Potsdam](https://up-rs-esp.github.io/), NSF and OpenTopography

## Description
In the past few years, the density and quality of point cloud data from lidar and photogrammetry has massively increased. This has enabled important new understanding in earth surface process science, but also has challenged our analytical tools and computational workflows. The generation of high resolution Digital Elevation Models, flow routing on point clouds, and surface roughness estimation has become more accessible and provides important measures of topography at the fine scale at which the processes operate.  This workshop presents approaches to analyzing point cloud data and producing useful derived products. It also explores future applications in earth surface processes.

The workshop will progress from point cloud analysis to appropriate filtering and gridding and then geomorphic analysis on grids and point clouds. In addition, we will spend one day on explorations of full waveform analyses for a variety of applications as these data are progressively becoming more available and useful for bathymetric, vegetation, surface roughness measurements, and material property mapping. 

This course is intended for graduate students and researchers with interests in surface processes and with experience in programming (Python and Matlab).

## Organization Committee and Instructors
[Bodo Bookhagen](https://bodobookhagen.github.io/), [Wolfgang Schwanghart](https://topotoolbox.wordpress.com/), [Fiona Clubb](https://fclubb.github.io/), [Aljoscha Rheinwalt](https://github.com/Rheinwalt), Ramon Arrowsmith, Chris Crosby


# Tentative Program
*Monday, Sept 30, 2019*
OpenTopography introduction and production implementations
- Point cloud selection and review of basic processiing workflows
- DEM processing using neighborhood and triangulation methods to produce DSM and DTMs
- DEM processing for flow routing using TauDEM HPC
	
Desktop based (Python driven) point cloud classification and filtering, followed by interpolation to grids using the most appropriate methods (from triangulation to IDW and fitting green's functions and splines and other surfaces). 

Airborne lidar to photogrammetric SFM warping example 

*Tuesday, October 1, 2019*
Flow routing on point clouds using TINs
Channel Head identification using point clouds with various densities

*Wednesday, October 2, 2019*
Explain and explore full-waveform data with specific applications for geomorphology (micro-surface roughness, better characterization of ground surface, material-surface characteristics, water-column characteristics, and biomass estimation)

*Thursday, October 3, 2019*
Matlab Topotoolbox, basic data types and structures; steepness indices, 

*Friday, October 4, 2019*
LSD, river-profile clustering, ridge-top curvature, making appealing maps with GMT

