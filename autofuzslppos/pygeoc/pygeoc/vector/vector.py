#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Vector related Classes and Functions

    author: Liangjun Zhu
    changlog: 12-04-12 jz - origin version
              16-07-01 lj - reorganized for pygeoc
              17-06-25 lj - check by pylint and reformat by Google style
"""

import os
import sys

from osgeo.ogr import wkbLineString
from osgeo.ogr import GetDriverByName as ogr_GetDriverByName
from osgeo.ogr import CreateGeometryFromJson as ogr_CreateGeometryFromJson
from osgeo.ogr import Geometry as ogr_Geometry
from osgeo.ogr import Feature as ogr_Feature

from ..utils.utils import FileClass, UtilClass, sysstr


class VectorUtilClass(object):
    """Utility function to handle vector data."""

    def __init__(self):
        pass

    @staticmethod
    def raster2shp(rasterfile, vectorshp, layername=None, fieldname=None):
        """Convert raster to ESRI shapefile"""
        FileClass.remove_files(vectorshp)
        FileClass.check_file_exists(rasterfile)
        # raster to polygon vector
        exepath = FileClass.get_executable_fullpath("gdal_polygonize.py")
        str_cmd = 'python %s -f "ESRI Shapefile" %s %s' % (exepath, rasterfile, vectorshp)
        if layername is not None and fieldname is not None:
            str_cmd += ' %s %s' % (layername, fieldname)
        print (str_cmd)
        print (UtilClass.run_command(str_cmd))

    @staticmethod
    def convert2geojson(jsonfile, src_srs, dst_srs, src_file):
        """convert shapefile to geojson file"""
        if os.path.exists(jsonfile):
            os.remove(jsonfile)
        if sysstr == 'Windows':
            exepath = '"%s/Lib/site-packages/osgeo/ogr2ogr"' % sys.exec_prefix
        else:
            exepath = FileClass.get_executable_fullpath("ogr2ogr")
        # os.system(s)
        s = '%s -f GeoJSON -s_srs "%s" -t_srs %s %s %s' % (
            exepath, src_srs, dst_srs, jsonfile, src_file)
        UtilClass.run_command(s)

    @staticmethod
    def write_line_shp(line_list, out_shp):
        """Export ESRI Shapefile -- Line feature"""
        print ("Write line shapefile: %s" % out_shp)
        driver = ogr_GetDriverByName("ESRI Shapefile")
        if driver is None:
            print ("ESRI Shapefile driver not available.")
            sys.exit(1)
        if os.path.exists(out_shp):
            driver.DeleteDataSource(out_shp)
        ds = driver.CreateDataSource(out_shp.rpartition(os.sep)[0])
        if ds is None:
            print ("ERROR Output: Creation of output file failed.")
            sys.exit(1)
        lyr = ds.CreateLayer(out_shp.rpartition(os.sep)[2].split('.')[0], None, wkbLineString)
        for l in line_list:
            line = ogr_Geometry(wkbLineString)
            for i in l:
                line.AddPoint(i[0], i[1])
            templine = ogr_CreateGeometryFromJson(line.ExportToJson())
            feature = ogr_Feature(lyr.GetLayerDefn())
            feature.SetGeometry(templine)
            lyr.CreateFeature(feature)
            feature.Destroy()
        ds.Destroy()
