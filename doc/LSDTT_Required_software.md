# Required software for LSDTopoTools

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
# Start_LSDTT.sh
```
When you are finished with your docker session type ctrl+d.


# Required software for clustering tutorial

In order to run the clustering tutorial you will need to have Python 3 and several packages. The instructions below show how to do this with an Anaconda/Miniconda distribution. If you would like to use your own laptop, please do this before the session on Thursday.

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
