#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on the 23 March 2017
author : olivier regniers (i-sea)
Application : reads metadata, applies coastline mask, performs atmospheric correction using DOS1 approach and export result in outFolder, estimates Turbidity with method from Dogliotti 2015 based on Red and NIR reflectance and exports result as an image, writes an xml file containing metadata about the image and statistics on estimated turbidity 
example : python C:\Users\ucfadko\Desktop\SEODWARF_S2_TURB_fMask.py -inFolder C:\Users\ucfadko\Desktop\S2A_MSIL1C_20170203T083141_N0204_R021_T36SWD_20170203T083527 -outFolder C:\Users\ucfadko\Desktop\S2_Results
Milto's example: python C:\Users\Milto\Documents\TEPAK\RISE\SEO_DWARF_algorithms\Code\SEODWARF_S2_TURB_fMask.py -inFolder C:\Users\Milto\Documents\TEPAK\RISE\TestData\S2A_MSIL1C_20170225T091021_N0204_R050_T35SLA_20170225T091220 -outFolder C:\Users\Milto\Documents\TEPAK\RISE\TestResults

note1 : classical folder and files structure for raw L1C S2 data has to be conserved for the code to run properly
note2 : code needs a coastline shapefile to apply land/water mask, check within the code if path to shapefile is correct (around line 170)
note 3 : code needs fmask to perform cloud masking, check within the code if path to fmask python functions is correct (around line 126) or add directory to working path
"""

import os
import sys
import gdal, ogr
from gdalconst import *
import argparse
import subprocess
import numpy 
import math
import xml.etree.ElementTree as ET
import glob
import re

 # argument parser
parser = argparse.ArgumentParser()
parser.add_argument("-inFolder",
     required=True,
     help="path to folder containing S2 data (first folder, not IMG_DATA)",
     metavar='<string>')
parser.add_argument("-outFolder",
     required=True,
     help="path to folder where results are stored",
     metavar='<string>')
params = vars(parser.parse_args())
inFolder = params['inFolder']
outFolder = params['outFolder']


# recover list of bands to be processed
bandNum10m = [4,3,2,8]
bandNumAll = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B10', 'B11', 'B12']
bandList = []
allFiles = glob.glob(inFolder + '\*\GRANULE\*\IMG_DATA\*.jp2') 
for b in range(len(bandNumAll)):
 for file in allFiles:
  if file.endswith('_%s.jp2' % bandNumAll[b]):
   bandList.append(file)  

# recover metadata file
os.listdir(inFolder + '/GRANULE/')

MTD_MSIL1C = inFolder + '/MTD_MSIL1C.xml'
MTD_TL = inFolder + '/GRANULE/' + os.listdir(inFolder + '/GRANULE/')[0]  + '/MTD_TL.xml'


# --- read metadata ---

print('Read metadata files')

# search tile name in input folder
match = re.search('([A-Z][1-9][1-9][A-Z][A-Z][A-Z])', inFolder)
tile = match.group(0)
EPSG_code = 'EPSG_326' + tile[1:3]

dataset = gdal.Open('SENTINEL2_L1C:%s:10m:%s' % (MTD_MSIL1C, EPSG_code), GA_ReadOnly)
if dataset is None:
 print('Unable to open image')
 sys.exit(1)
MTD = dataset.GetMetadata()
wkt_projection =dataset.GetProjection()
geotransform = dataset.GetGeoTransform()
# print MTD

# read metadata per band
bandB = dataset.GetRasterBand(3)
bandG = dataset.GetRasterBand(2)
bandR = dataset.GetRasterBand(1)
bandIR = dataset.GetRasterBand(4)
MTD_B = bandB.GetMetadata()
MTD_G = bandG.GetMetadata()
MTD_R = bandR.GetMetadata()
MTD_IR = bandIR.GetMetadata()

# --- recover values from metadata ---
ULX = geotransform[0]
ULY = geotransform[3]
pixelWidth = geotransform[1]
pixelHeight = geotransform[5]
nl = dataset.RasterYSize
nc = dataset.RasterXSize

DATE = MTD['GENERATION_TIME'][0:10]
HOUR = MTD['GENERATION_TIME'][11:16]

if MTD['DATATAKE_1_SPACECRAFT_NAME'] == 'Sentinel-2A':
 sensor = 'S2A'
elif MTD['DATATAKE_1_SPACECRAFT_NAME'] == 'Sentinel-2B':
 sensor = 'S2B'

imageNameLong = MTD['PRODUCT_URI']
# pos_ = [pos for pos, char in enumerate(imageNameLong) if char == '_']
# tile = imageNameLong[pos_[4]+1:pos_[4]+7]
dst_earth_sun = float(MTD['REFLECTANCE_CONVERSION_U'])
QUANT = int(MTD['QUANTIFICATION_VALUE'])
ESUN = [MTD_R['SOLAR_IRRADIANCE'], MTD_G['SOLAR_IRRADIANCE'], MTD_B['SOLAR_IRRADIANCE'], MTD_IR['SOLAR_IRRADIANCE']]

# read xml file and get extra metadata
root = ET.parse(MTD_TL).getroot()
tmp = root.find('.//Mean_Sun_Angle/ZENITH_ANGLE')
thetas = 90 - float(tmp.text)

print('DONE\n')

# --- fMask cloud masking ---

# print('Cloud mask with fMask')

# create ouput image name and output folder
imageName = sensor + '_' + DATE + '_' + tile
outFolder2 = outFolder + '/' + imageName

"""
if not os.path.exists(outFolder2):
 os.mkdir(outFolder2)


out_cloud_Mask = outFolder2 + '/cloud_FMask.tif' 

if not os.path.isfile(out_cloud_Mask): # if mask doesn't already exist

 os.chdir('C:\Users\Olivier\Anaconda2\Scripts') # change path to fmask folder

 # create virtual raster
 outVRT = outFolder2 + '/allbands.vrt'
 cmd = 'gdalbuildvrt -resolution user -tr 20 20 -separate ' + outVRT
 for b in bandList:
  cmd = cmd + ' ' + b
 subprocess.call(cmd, shell=True)

 # create angle image
 outAngles = outFolder2 + '/angles.img'
 cmd = 'python fmask_sentinel2makeAnglesImage.py -i ' + MTD_TL + ' -o ' + outAngles
 subprocess.call(cmd, shell=True)

 # create mask
 outFMASK = outFolder2 + '/cloud.img'
 cmd = 'python fmask_sentinel2Stacked.py -a ' + outVRT + ' -z ' + outAngles + ' -o ' + outFMASK
 subprocess.call(cmd, shell=True)
 
 # resample mask
 cmd = 'gdalwarp -tr 10 10 -ot Byte ' + outFMASK + ' ' + out_cloud_Mask
 subprocess.call(cmd, shell=True)

 print('DONE\n')
 
else:
 
 print('Cloud masking already done\n')
"""
# --- DOS1 correction ---

# rasterize input shapefile mask 

print('DOS1 atmospheric correction')

# check if DOS1 correction has already been applied
if not os.path.exists(outFolder2 + '/TOC'):
 os.mkdir(outFolder2 + '/TOC')
DOS_red = outFolder2+'/TOC/' + imageName + '_B04_TOC.tif'

if not os.path.isfile(DOS_red): # if outFile does not already exist

 pathMaskShp = 'C:/Users/ucfadko/Desktop/Coastline_EUROPE_UTMZ33N/Coastline_EUROPE_UTMZ33N.shp'
 outLW_Mask = outFolder2 + '/LW_mask.tif'
 
 # check if shapefile exists
 if not os.path.isfile(pathMaskShp):
  print('Coastline shapefile is not in the right folder')
  sys.exit(1)

 Xmin = ULX
 Xmax = ULX + nc*pixelWidth
 Ymin = ULY - nl*pixelWidth
 Ymax = ULY
 
 print ('Water/Land mask creation')
 cmd = 'gdal_rasterize -a id -ot Byte -te ' + str(Xmin) + ' ' + str(Ymin) + ' ' + str(Xmax) + ' ' + str(Ymax) + ' -tr ' + str(pixelWidth)+ ' ' + str(pixelWidth) + ' ' + pathMaskShp + ' ' + outLW_Mask
 # print cmd
 subprocess.call(cmd, shell=True)
 print ('DONE\n')

 # read land/water mask
 ds_LW_mask = gdal.Open(outLW_Mask, GA_ReadOnly) 
 if ds_LW_mask is None:
  print('Unable to open land/water mask')
  sys.exit(1)
 LW_mask = ds_LW_mask.GetRasterBand(1).ReadAsArray(0, 0, ds_LW_mask.RasterXSize, ds_LW_mask.RasterYSize)
 
 """
 # read cloud mask
 ds_cloud_mask = gdal.Open(out_cloud_Mask, GA_ReadOnly) 
 if ds_cloud_mask is None:
  print('Unable to open cloud mask')
  sys.exit(1)
 cloud_mask = ds_cloud_mask.GetRasterBand(1).ReadAsArray(0, 0, ds_cloud_mask.RasterXSize, ds_cloud_mask.RasterYSize)
 """
 # loop through bands (beware order of bands is R,G,B,IR - so band[1] is red band
 for b in range( dataset.RasterCount ):
  # read raster band
  band = dataset.GetRasterBand(b+1).ReadAsArray(0, 0, dataset.RasterXSize, dataset.RasterYSize)
  # apply masks
  band = numpy.where((LW_mask==0), band, 0) # we keep pixels flagged as water (cloud_mask==5) and snow (cloud_mask==4) as turbid waters can be flagged as snow
  # PREVIOUS LINE WITH CLOUD MASK : band = numpy.where((( cloud_mask==5) | (cloud_mask==4)) & (LW_mask==0), band, 0) # we keep pixels flagged as water (cloud_mask==5) and snow (cloud_mask==4) as turbid waters can be flagged as snow
  # band = numpy.where(LW_mask==0, band, 0)
  
  
  # convert DN to TOA reflectance
  band = band.astype(float)
  band = band / QUANT
  # convert TOA reflectance to TOA radiance
  band = (band * float(ESUN[b]) * math.cos(math.radians(thetas))) / (math.pi * math.pow(dst_earth_sun,2))
  # convert 2D array to 1D array, discard zeros and estimate 1% percentile calculation
  tmp = band.reshape(-1)
  tmp = tmp[tmp!=0.0]
  Lmin1 = numpy.percentile(tmp,1)
  # calculate path radiance
  Lp = Lmin1 - (0.01 * float(ESUN[b]) * math.cos(math.radians(thetas))) / (math.pi * math.pow(dst_earth_sun,2))
  # calculate corrected reflectance
  band_BOA = (math.pi * (band - Lp) * math.pow(dst_earth_sun,2)) / (float(ESUN[b]) * math.cos(math.radians(thetas)))
  
  # write output data
  outFile = outFolder2+'/TOC/' + imageName + '_B0' + str(bandNum10m[b]) + '_TOC.tif'
  DataType = gdal.GDT_Float32
  driver = gdal.GetDriverByName("GTiff")
  outdata = driver.Create(outFile, nl, nc, 1, DataType)
  outdata.SetGeoTransform((ULX, pixelWidth, 0, ULY, 0, pixelHeight)) # Georeference the image
  outdata.SetProjection(wkt_projection)  # Write projection information
  outdata.GetRasterBand(1).WriteArray(band_BOA)  # Write the array to the file
  outdata = None  

 # clear datasets
 dataset = None
 ds_LW_mask = None
 ds_cloud_mask = None
 
 # remove tmp_mask file
 os.remove(outFolder2 + '/LW_mask.tif')
 
 print('DONE\n')

else:

 print('Atmospheric correction already done\n')

# plt.imshow(bandB_mask)
# plt.show()

# --- Turbidity DOGLIOTTI 2015

print('compute turbidity')

# read red and IR bands
redBOAFile = outFolder2 + '/TOC/' + imageName + '_B04_TOC.tif'
ds_redBOA = gdal.Open(redBOAFile, GA_ReadOnly) 
if ds_redBOA is None:
 print('Unable to open red band')
 sys.exit(1)
redBOA = ds_redBOA.GetRasterBand(1).ReadAsArray(0, 0, ds_redBOA.RasterXSize, ds_redBOA.RasterYSize)

irBOAFile = outFolder2+'/TOC/' + imageName + '_B08_TOC.tif'
ds_irBOA = gdal.Open(irBOAFile, GA_ReadOnly) 
if ds_irBOA is None:
 print('Unable to open ir band')
 sys.exit(1)
irBOA = ds_irBOA.GetRasterBand(1).ReadAsArray(0, 0, ds_irBOA.RasterXSize, ds_irBOA.RasterYSize)

# create numpy array filled with nan for turbidity
TURB = numpy.full(redBOA.shape, numpy.nan)

# dogliotti parameters for S2 red and IR bands obtained from ACOLITE ancilliary data
A_red = 366.14
C_red = 0.19563
A_ir = 1913.65
C_ir = 0.1913

# estimate turbidity with DOGLIOTTI 2015 approach
for i in range(0,nc-1):
 for j in range(0,nl-1):
  if redBOA[i,j] > 0 and irBOA[i,j] > 0: # avoid any pixel with negative or zero value
   if redBOA[i,j] < 0.05:
    TURB[i,j] = (A_red * redBOA[i,j]) / (1 - (redBOA[i,j] / C_red))
   elif redBOA[i,j] > 0.07:
    TURB[i,j] = (A_ir * irBOA[i,j]) / (1 - (irBOA[i,j] / C_ir))
   elif redBOA[i,j] >= 0.05 and redBOA[i,j] <= 0.07:
    w = (0.07 - redBOA[i,j])/(0.07 - 0.05)
    TURB_red = (A_red * redBOA[i,j]) / (1 - (redBOA[i,j] / C_red))
    TURB_ir = (A_ir * irBOA[i,j]) / (1 - (irBOA[i,j] / C_ir))
    TURB[i,j] = w * TURB_red + (1 - w) * TURB_ir
 
 # display progress
 step = round(nc/10)
 if i % step == 0 and i != 0:
  print (str(int(round(i/float(nc)*100))) + '% turbidity completed')

# write output data
if not os.path.exists(outFolder2 + '/TURB'):
 os.mkdir(outFolder2 + '/TURB')
outFile_TURB = outFolder2 + '/TURB/T_DOGLIOTTI2015.tif'
DataType = gdal.GDT_Float32
driver = gdal.GetDriverByName("GTiff")
outdata = driver.Create(outFile_TURB, nl, nc, 1, DataType)
outdata.SetGeoTransform((ULX, pixelWidth, 0, ULY, 0, pixelHeight)) # Georeference the image
outdata.SetProjection(wkt_projection)  # Write projection information
outdata.GetRasterBand(1).WriteArray(TURB)  # Write the array to the file
outdata = None

ds_redBOA = None
ds_irBOA = None

print('DONE\n')
