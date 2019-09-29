# Aligning ALS (Milan, May-06-2018) and UAV (Mavic Pro 2, Aug 2019)
We will use a precise airborne lidar dataset (ALS) with a high point density as reference dataset. We will align a UAV (Mavic Pro 2, nadir and 15-degree oblique imagery, processing with Agisoft Metashape/PhotoScan). You will note a doming effect of the UAV dataset - we will explore these further by fitting a sphere.

Alignment and Visualization is done in CloudCompare (can be done in PDAL or python as well)

1. *Load in data*. First load in ALS (reference PC) first. THEN load in second point cloud (Mavic Pro 2), make sure you use the same reference frame (last input and not suggested).
![Make sure to select 'last input' when loading the second point cloud.](https://github.com/UP-RS-ESP/PointCloudWorkshop-Oct2019/tree/master/png/last_input.png "Last Input")

2. *ICP Alignment*: Select two point clouds to be aligned, then select Tools->Registration->Fine Registration (ICP).
  - Make sure to store resulting transformation matrix (select in console and copy) - it will be useful to save this.
  - Verify that point clouds are aligned.
![Set overlap to 90% (or something similar) before running the ICP step (unless you can be certain that the extent is exactly the same).](https://github.com/UP-RS-ESP/PointCloudWorkshop-Oct2019/tree/master/png/registration1.png "ICP Alignment")

3. *Calculate Cloud-to-Cloud Distance*: Select two point clouds, Tools->Distances->Cloud/Cloud Distance. Make sure to split into X, Y, Z direction
![Cloud2Cloud Distance Computation Parameters 1](https://github.com/UP-RS-ESP/PointCloudWorkshop-Oct2019/tree/master/png/cloud2cloud_distance.png "C2C Distance 1") ![Cloud2Cloud Distance Computation Parameters 2](https://github.com/UP-RS-ESP/PointCloudWorkshop-Oct2019/tree/master/png/cloud2cloud_distance2.png "C2C Distance 2")

4. *Ground-Point Cloud Classification* (optional but useful): Using Plugin Cloth Simulation Filter (CSF) and perform Cloth Simulation Filter Classification with resolution r=1 using Plugins->CSF Filter (Will not work well for UAV dataset).
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")
  - Classify both datasets (1. ALS dataset and 2. registered, c2c dataset)
  - Are there problems with the classification? Is bare earth/ground properly detected?

  ![Cloth Simulation Filter (CSF) Classification](https://github.com/UP-RS-ESP/PointCloudWorkshop-Oct2019/tree/master/png/csf1.png "CSF1") ![Cloth Simulation Filter (CSF) Classification](https://github.com/UP-RS-ESP/PointCloudWorkshop-Oct2019/tree/master/png/csf2.png "CSF2")

5. Save UAV ground and off-ground points, make sure to save additional fields. This will store a UAV (Mavic Pro 2) LAZ file with ground points and X, Y, Z, and total distance. *Note: Some OS/installations have problems reading LAZ files, it may be useful to store as LAS file (without compression), if you have trouble).*

  - Additionally, the classified ALS dataset can be stored.
