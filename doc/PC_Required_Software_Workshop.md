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

# LSDTopoTools
[LSDTopoTools](https://lsdtopotools.github.io/) will be used on Thursday.

## Required software for LSDTopoTools

1. Download and install Docker. We will assume this actually is working. *You must install docker before Thursday if you want to run it on your own laptop. Otherwise you can use the lab PCs*. If you get stuck, you can find more detailed installation instructions here: https://lsdtopotools.github.io/LSDTT_documentation/LSDTT_installation.html.

2. Once you have installed Docker, create a LSDTopoTools directory on your host operating system that you will share with the LSDTopoTools docker containers.  We will assume you make this in `C:\LSDTopoTools` on Windows or `\LSDTopoTools` on MacOS and Linux.

3. Pull the full LSDTopoTools container and run it with a linked volume. For Windows, open the PowerShell and type:
```
$ docker run --rm -it -v C:/LSDTopoTools:/LSDTopoTools lsdtopotools/lsdtt_pcl_docker
```
Or for MacOS or Linux:
```
$ docker run --rm -it -v /LSDTopoTools:/LSDTopoTools lsdtopotools/lsdtt_pcl_docker
```
Or if you have a different directory to LSDTopoTools data on your host machine:
```
$ docker run --rm -it -v /PATH/TO/YOUR/DATA:/LSDTopoTools lsdtopotools/lsdtt_pcl_docker
```
Once you run this, you will need to run the script:
```
$ Start_LSDTT.sh
```
When you are finished with your docker session type ctrl+d.


## Required software for clustering tutorial

In order to run the clustering tutorial you will need to have Python 3 and several packages. The instructions below show how to do this with an Anaconda/Miniconda distribution. If you would like to use your own laptop, please do this before the session on Thursday. There is a [github repository](https://github.com/UP-RS-ESP/river-clusters) for the river-cluster analysis. This contains a Jupyter notebook with a tutorial:


1. Download Miniconda (Python 3.7)

2. Open Anaconda Prompt and navigate to the directory with the repository

3. Create a new environment:
```
conda create --name river-clusters
```
4. Activate the environment:
```
conda activate river-clusters
```
5. Install required packages
```
conda install -c conda-forge matplotlib numpy pandas scipy shapely fiona descartes statsmodels jupyter pyproj
```
7. Download the repository with the clustering tutorial. Go to the GitHub repository: https://github.com/UP-RS-ESP/river-clusters and either clone it if you use GitHub, or click `Download ZIP` to download it as a ZIP file. If you download as a ZIP file you will then need to extract it.

6. You are now ready to run the Jupyter notebook on your computer. Use the Anaconda Prompt to navigate to the folder that you just downloaded and extracted and then type:
```
jupyter notebook
```
This will open the repository in your browser. Click on the notebook: `river-clustering.ipynb`. We will be working with this notebook during the workshop.
