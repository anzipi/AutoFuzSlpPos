#! /usr/bin/env python
#coding=utf-8
# Revised: 5/12/2015  Removing 

from Nomenclature import *
from Util import *
import TauDEM
import time
from Config import *
from shutil import copy2
# Stage 1: Preprocessing for Slope, Curvature, RPI
def PreProcessing(model):
    startT = time.time()
    logStatus = open(log_preproc, 'w')
    if model == 0:
        logStatus.write("Preprocessing based on D8 flow model.\n")
    elif model ==1:
        logStatus.write("Preprocessing based on D-infinity flow model.\n")
    logStatus.flush()
    logStatus.write("[Preprocessing] [1/7] Converting DEM file format to GeoTiff...\n")
    logStatus.flush()
    TIFF2GeoTIFF(rawdem, dem)
#    logStatus.write("[Preprocessing] [2/7] Generating negative DEM file for ridge sources extraction...\n")
#    logStatus.flush()
#    NegativeDEM(dem,negDEM) 
    logStatus.write("[Preprocessing] [2/7] Removing pits...\n")
    logStatus.flush()
    TauDEM.pitremove(rawdem,inputProc,demfil,exeDir)
    #TauDEM.pitremove(negDEM,inputProc,negDEMfil,exeDir)
    logStatus.write("[Preprocessing] [3/7] Flow direction and slope in radian...\n")
    logStatus.flush()
    TauDEM.D8FlowDir(demfil,inputProc,D8FlowDir,D8Slp,exeDir)
#    if model == 0:
#        TauDEM.D8FlowDir(negDEMfil,inputProc,negD8FlowDir,negD8Slp,exeDir)
    if model == 1:
        TauDEM.DinfFlowDir(demfil,inputProc,DinfFlowDir,DinfSlp,exeDir)
        #TauDEM.DinfFlowDir(negDEMfil,inputProc,negDinfFlowDir,negDinfSlp,exeDir)
    #logStatus.write("[Preprocessing] [4/7] Move outlet to initially stream and Generating flow accumulation with Peuker Douglas stream sources as weightgrid...\n")
    logStatus.write("[Preprocessing] [4/7] Move outlet to initially stream and Generating flow accumulation...\n")
    logStatus.flush()    
    #TauDEM.PeukerDouglas(demfil,centerweight,sideweight,diagonalweight,inputProc,PkrDglStream,exeDir)
    #TauDEM.PeukerDouglas(negDEMfil,centerweight,sideweight,diagonalweight,inputProc,negPkrDglStream,exeDir)
    #TauDEM.AreaD8(D8FlowDir,'',PkrDglStream,'false',inputProc,D8ContriArea,exeDir)
    TauDEM.AreaD8(D8FlowDir,'','','false',inputProc,D8ContriArea,exeDir)
    maxAccum, minAccum, meanAccum, STDAccum = GetRasterStat(D8ContriArea)
    TauDEM.Threshold(D8ContriArea,'',meanAccum,inputProc,D8Stream,exeDir)
    TauDEM.MoveOutletsToStreams(D8FlowDir,D8Stream,outlet,maxMoveDist,inputProc,outletM, exeDir)
#    if model == 0:
#        TauDEM.AreaD8(negD8FlowDir,'',negPkrDglStream,'false',inputProc,negD8ContriArea,exeDir)
    #TauDEM.AreaD8(D8FlowDir,outletM,PkrDglStream,'false',inputProc,D8ContriArea,exeDir)
    if model == 1:
        TauDEM.AreaDinf(DinfFlowDir,'','','false',inputProc,DinfContriArea,exeDir)
        #TauDEM.AreaDinf(DinfFlowDir,outletM,PkrDglStream,'false',inputProc,DinfContriArea,exeDir)
        #TauDEM.AreaDinf(negDinfFlowDir,'',negPkrDglStream,'false',inputProc,negDinfContriArea,exeDir)
    if model ==0:
        logStatus.write("[Preprocessing] [5/7] Generating stream source raster based on Drop Analysis...\n")
    elif model == 1:
        logStatus.write("[Preprocessing] [5/7] Generating stream source raster based on Threshold derived from D8 flow model drop analysis or assigned...\n")
    logStatus.flush()
    global D8StreamThreshold
    if D8StreamThreshold == 0:
        ## both D8 and D-infinity need to run drop analysis
        maxAccum, minAccum, meanAccum, STDAccum = GetRasterStat(D8ContriArea) #print maxAccum, minAccum, meanAccum, STDAccum
        if meanAccum - STDAccum < 0:
            minthresh = meanAccum
        else:
            minthresh = meanAccum - STDAccum
        maxthresh = meanAccum + STDAccum
        TauDEM.DropAnalysis(demfil,D8FlowDir,D8ContriArea,D8ContriArea,outletM,minthresh,maxthresh,numthresh,logspace,inputProc,drpFile, exeDir)
        drpf = open(drpFile,"r")
        tempContents=drpf.read()
        (beg,d8drpThreshold)=tempContents.rsplit(' ',1)
        drpf.close()
        D8StreamThreshold = d8drpThreshold
    TauDEM.Threshold(D8ContriArea,'',D8StreamThreshold,inputProc,D8Stream,exeDir)
    if model == 1:
        global DinfStreamThreshold
        if DinfStreamThreshold == 0:
            DinfStreamThreshold = D8StreamThreshold
        TauDEM.Threshold(DinfContriArea,'',DinfStreamThreshold,inputProc,DinfStream,exeDir)
    #logStatus.write("[Preprocessing] [6/7] Delineating sub-basins...\n")
    #logStatus.flush()
    #TauDEM.StreamNet(demfil,D8FlowDir,D8ContriArea,D8Stream,outletM,'false',inputProc,D8StreamOrd,NetTree,NetCoord,D8StreamNet,SubBasin, exeDir)
#    logStatus.write("[Preprocessing] [8/7] Generating ridge source raster based on threshold method...\n")
#    logStatus.flush()
#    if model == 0:
#        global negD8StreamThreshold
#        if negD8StreamThreshold == 0:
#            negD8StreamThreshold = D8StreamThreshold
#        TauDEM.Threshold(negD8ContriArea,'',negD8StreamThreshold,inputProc,negD8Stream,exeDir)
#    elif model ==1:
#        global negDinfStreamThreshold
#        if negDinfStreamThreshold == 0:
#            negDinfStreamThreshold = DinfStreamThreshold
#        TauDEM.Threshold(negDinfContriArea,'',negDinfStreamThreshold,inputProc,negDinfStream,exeDir)
    logStatus.write("[Preprocessing] [6/7] Calculating RPI(Relative Position Index)...\n")
    logStatus.flush()
    if model == 0:
        TauDEM.D8DistDownToStream(D8FlowDir,demfil,D8Stream,D8DistDown,D8DownMethod,D8StreamTag,inputProc,exeDir)
        TauDEM.D8DistUpToRidge(D8FlowDir,demfil,D8DistUp,D8UpMethod,D8UpStats,inputProc,rdg=rdgsrc,exeDir=exeDir)
        TauDEM.D8DistDownToStream(D8FlowDir,demfil,D8Stream,D8DistDown_V,'Vertical',D8StreamTag,inputProc,exeDir)
        TauDEM.SimpleCalculator(D8DistDown,D8DistUp,RPID8,4,inputProc,exeDir)
    elif model == 1:
        #TauDEM.DinfDistDown(DinfFlowDir,demfil,DinfStream,DinfDownStat,DinfDownMethod,'false',DinfDistDownWG,inputProc,DinfDistDown,exeDir)
        TauDEM.DinfDistDown(DinfFlowDir,demfil,D8Stream,DinfDownStat,DinfDownMethod,'false',DinfDistDownWG,inputProc,DinfDistDown,exeDir)
        TauDEM.DinfDistUpToRidge(DinfFlowDir,demfil,DinfSlp,propthresh,DinfUpStat,DinfUpMethod,'false',inputProc,DinfDistUp,rdg=rdgsrc,exeDir=exeDir)
        TauDEM.DinfDistDown(DinfFlowDir,demfil,D8Stream,DinfDownStat,'Vertical','false',DinfDistDownWG,inputProc,DinfDistDown_V,exeDir)
        TauDEM.SimpleCalculator(DinfDistDown, DinfDistUp, RPIDinf, 4,inputProc,exeDir)

    logStatus.write("[Preprocessing] [7/7] Calculating Plan Curvature and Profile Curvature...\n")
    logStatus.flush()
    TauDEM.Curvature(inputProc,demfil,prof=ProfC,horiz=HorizC,exeDir=exeDir)

    if model == 0:
        copy2(D8Slp,Slope)
        copy2(RPID8,RPI)
        copy2(D8DistDown_V,HAND)
    elif model == 1:
        copy2(DinfSlp,Slope)
        copy2(RPIDinf,RPI)
        copy2(DinfDistDown_V,HAND)
    #HANDDict['Min'],HANDDict['Max'],HANDDict['Ave'],HANDDict['STD'] = RasterStatistics(HAND)
#    logStatus.write("[Preprocessing] [9/7] Clip parameter raster to Subbasin's boundary...\n")
#    logStatus.flush()
#    if FlowModel == 0:
#        TauDEM.SimpleCalculator(D8Slp,SubBasin,Slope,5,inputProc,exeDir)
#        TauDEM.SimpleCalculator(RPID8,SubBasin,RPI,5,inputProc,exeDir)
#        TauDEM.SimpleCalculator(ProfC,SubBasin,ProfC_mask,5,inputProc,exeDir)
#        TauDEM.SimpleCalculator(HorizC,SubBasin,HorizC_mask,5,inputProc,exeDir)
#    elif FlowModel == 1:
#        TauDEM.SimpleCalculator(DinfSlp,SubBasin,Slope,5,inputProc,exeDir)
#        TauDEM.SimpleCalculator(RPIDinf,SubBasin,RPI,5,inputProc,exeDir)
#        TauDEM.SimpleCalculator(ProfC,SubBasin,ProfC_mask,5,inputProc,exeDir)
#        TauDEM.SimpleCalculator(HorizC,SubBasin,HorizC_mask,5,inputProc,exeDir)
    logStatus.write("[Preprocessing] Preprocessing succeed!\n")
    logStatus.flush()
    endT = time.time()
    cost = (endT - startT)/60.
    logStatus.write("Time consuming: %.1f min.\n" % cost)
    logStatus.flush()
    logStatus.close()