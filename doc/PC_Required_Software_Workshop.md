---
title: "Required and suggested software for the workshop: From point clouds and full waveform data to DEM analysis"
author: B. Bookhagen
date: 20-09-2019
...

We provide 20 fast computers with dual boot (Windows 10 and Ubuntu 18.04). These have all necessary software installed. If you decide to bring your own laptop (which is fine), please make sure to install the software below _before_ your arrival. It will take around 15-25 minutes to install the software. Also, please ensure that your laptop is of sufficiently high quality, has multiple cores, and a decent graphic card - because we will use data with tens to hundreds of millions of points, we want to explore data optimization techniques. Most of the software will also be easily installed on a Mac. _We suggest to use Ubuntu or some other Linux-based distribution as these are the most flexible systems_.

In short, the required software is:

- [CloudCompare](https://www.danielgm.net/cc)
  - Point Cloud analysis and visualization. Includes many useful point-cloud analysis tools, but is slower on the visualization of large pointclouds

- [Displaz](http://c42f.github.io/displaz/)
  - Very fast and versatile viewer. Can be run from python.
  - _Ubuntu Users:_ This likely will need to be compiled on your machine - follow the instructions on the github page
  - _Mac users:_ Due to the recent updates for the X11 Server, this doesn't properly compile. You may end up using CloudCompare instead (which is slower for visualization).

- [Python 3.x](https://www.python.org/), [PDAL](https://pdal.io/), [GDAL](https://gdal.org/), [GMT](http://gmt.soest.hawaii.edu/), [cython](https://cython.org/), [scipy](https://www.scipy.org/), [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), [pylidar](http://www.pylidar.org/en/latest/), [laspy](https://pypi.org/project/laspy/) and several other tools
  - These are several productive tools for programming and Point Cloud analysis. These are usually best installed through a conda/anaconda environment.
  - _Windows Users:_ One option is to install this via [Anaconda](https://www.anaconda.com/) and select the packages **Pylidar, pdal and lastools, numpy, pandas and matplotlib**.
  - _Alternative option Windows Users:_ install [Linux Subsystem on Windows](https://docs.microsoft.com/en-us/windows/wsl/install-win10) and use miniconda (see next section). Installing the Linux subsystem (use Ubuntu 18.04) is generally a useful thing to do for Windows users.
  - _Ubuntu and Mac Users:_ Install [miniconda3](https://docs.conda.io/en/latest/miniconda.html) and the packages via `conda install`. (see below)
  - In short, you download and install the required software via the command line:
    ```
    cd ~
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    sh ./Miniconda3-latest-Linux-x86_64.sh
    ```


    Include additional channels for installation:
    ```
    conda config --prepend channels conda-forge/label/dev
    conda config --prepend channels conda-forge
    ```


    Install the conda packages (will take some time):
    ```
    conda create -y -n PC_py3 python=3.6 pip scipy pandas numpy matplotlib scikit-image gdal pdal xarray packaging ipython multiprocess h5py lastools pykdtree spyder gmt=5* imagemagick
    ```

    Activate the environment `source activate PC_py3` and install laspy with `pip install laspy`
  - If you experience problems installing the conda packages (on some Windows Linux subsystems), use only:
    ```
    conda create -y -n PC_py3 python=3.6 pip scipy pandas numpy matplotlib scikit-image gdal pdal xarray packaging ipython multiprocess h5py lastools pykdtree
    ```
    and then install laspy.

- Building C/C++ code
  - For some examples, we will use OpenMP and it will be useful to have the gcc compiler and additional tools installed. `sudo apt-get install libomp-dev build-essential`

- Editor
  - We will be doing some coding and it may be useful to use an editor to take notes as well. Install your favorite editor - for example [Atom](https://atom.io/) or [Notepad++ on Windows](https://notepad-plus-plus.org/download/) or [Spyder](https://www.spyder-ide.org/). Spyder is included in the Windows Anaconda distribution and is installed via the command line above.
  - _Windows Users:_ There is no X-Windows interface in the Linux/Ubuntu subsystem and you will need to use Spyder from Windows

- [LAStools](https://rapidlasso.com/lastools/)
  - Commercial Software. However, contains several useful and very fast tools for working with Point Cloud data.

- [LSDTopoTools](https://lsdtopotools.github.io/)
  - This will be installed via docker on the day of the workshop.
