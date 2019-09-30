Using PC: UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm.laz

1. Obtaining information about PCs:
pdal info UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm.laz
pdal info --boundary UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm.laz

lasinfo -UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm.laz

Using LASTool's lasinfo: lasinfo -cd

2. Filtering PCs::
https://pdal.io/stages/filters.voxelcenternearestneighbor.html
https://pdal.io/stages/filters.voxelcentroidnearestneighbor.html

pdal translate UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm.laz -o UAV_mavicpro2_nadir_15deg_highq_dense_PC_100cm.laz voxelcenternearestneighbor --filters.voxelcenternearestneighbor.cell=1.0

or use pipeline:
```
{
  "pipeline":[
    "mavicpro2_nadir_15deg_highq_dense_PC.laz",
    {
      "type":"filters.voxelcenternearestneighbor",
      "cell":0.1
    },
    "mavicpro2_nadir_15deg_highq_dense_PC_10cm.laz"
  ]
}
```

3.
pdal translate UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm.laz -o UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm_cl2only.laz smrf range --filters.range.limits="Classification[2:2]" -v 4

pdal translate UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm
-o UAV_mavicpro2_nadir_15deg_highq_dense_PC_10cm_filt_cl.laz
outlier smrf range  ^
--filters.outlier.method="statistical" ^
--filters.outlier.mean_k=8 --filters.outlier.multiplier=3.0 ^
--filters.smrf.ignore="Classification[7:7]"  ^
--filters.range.limits="Classification[2:2]" ^
--writers.las.compression=true ^
--verbose 4
