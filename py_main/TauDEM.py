# Script Name: TauDEM functions
# 
# Created By:  David Tarboton
# Date:        9/28/11
# Revised By:  Liangjun Zhu (zlj@lreis.ac.cn)
# Date:        3/5/15
# Modified  :  Integrate to one file. Run without arcpy. Same name with executable files.
# Revised By:  Liangjun Zhu
# Date:        4/14/15
# Modified  :  add path to TauDEM executable program


# Program: TauDEM and extensions based on TauDEM parallelized framework
# 
# Revised By:  Liangjun Zhu
# Date From :  3/20/15
# Email     :  zlj@lreis.ac.cn
#

# Import modules
import os,platform
import sys
import time
import string
import subprocess
from Util import WriteLog,WriteTimeLog
from Nomenclature import Log_all,Log_runtime

sysstr = platform.system()
if sysstr == "Windows":
    LF = '\r'
elif sysstr == "Linux":
    LF = '\n'

## Basic Grid Analysis
def pitremove(inZfile,inputProc,outFile, mpiexeDir = None, exeDir=None):
    print "PitRemove......"
    print "Input Elevation file: "+inZfile
    print "Input Number of Processes: "+str(inputProc)
    print "Output Pit Removed Elevation file: "+outFile
    # Construct the taudem command line.  Put quotes around file names in case there are spaces
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' pitremove -z ' + '"' + inZfile + '"' + ' -fel ' + '"' + outFile + '"'
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'pitremove -z ' + '"' + inZfile + '"' + ' -fel ' + '"' + outFile + '"'
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    print "Command Line: "+cmd
    ##os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "PitRemove"
    contentList.append('\n')
    contentList.append("#### PitRemove ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
def pitremoveplanchon(inZfile,deltaElev,inputProc,outFile,mpiexeDir=None,exeDir=None):
    print "PitRemove(Planchon and Darboux, 2001)......"
    print "Input Elevation file: "+inZfile
    print "Input Number of Processes: "+str(inputProc)
    print "Mininum increment of elevation when filling depression: "+str(deltaElev)
    print "Output Pit Removed Elevation file: "+outFile
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(1) + ' pitremoveplanchon -z ' + '"' + inZfile + '"' + ' -fel ' + '"' + outFile + '"' + ' -delta ' + str(deltaElev)
    else:
        cmd = 'mpiexec -n ' + str(1) + ' ' + exeDir + os.sep + 'pitremoveplanchon -z ' + '"' + inZfile + '"' + ' -fel ' + '"' + outFile + '"'+ ' -delta ' + str(deltaElev)
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    print "Command Line: "+cmd
    ##os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "PitRemove"
    contentList.append('\n')
    contentList.append("#### PitRemove(Planchon and Darboux, 2001) ####")
    
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
def ConnectDown(ad8,outlet,inputProc,mpiexeDir = None, exeDir=None):
   print "Generating outlet shapefile from areaD8......"
   print "Input areaD8 file: "+ad8
   print "Input Number of Processes: "+str(inputProc)
   print "Output outlet File: "+outlet

   # Construct command
    
   if exeDir is None:
       cmd = 'mpiexec -n ' + str(inputProc) + ' connectdown -ad8 ' + '"' + ad8 + '"' + ' -o ' + '"' + outlet + '"'
   else:
       cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir  + os.sep + 'connectdown -ad8 ' + '"' + ad8 + '"' + ' -o ' + '"' + outlet + '"'
   if mpiexeDir is not None:
       cmd = mpiexeDir + os.sep + cmd
   print "Command Line: "+cmd
   ##os.system(cmd)
   process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
   contentList = []
   timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
   timeDict['name'] = "ConnectDown"
   contentList.append('\n')
   contentList.append("#### Generating outlet shapefile from areaD8 ####")
   for line in process.stdout.readlines():
       contentList.append(line.split(LF)[0])
       #print line
       if line.find("Read time") >= 0:
           timeDict['readt'] = line.split(LF)[0].split(':')[-1]
       elif line.find("Compute time") >= 0:
           timeDict['computet'] = line.split(LF)[0].split(':')[-1]
       elif line.find("Write time") >= 0:
           timeDict['writet'] = line.split(LF)[0].split(':')[-1]
       elif line.find("Total time") >= 0:
           timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
   WriteLog(Log_all,contentList)
   WriteTimeLog(Log_runtime,timeDict)
       

def D8FlowDir(fel,inputProc,p,sd8, mpiexeDir = None, exeDir=None):
    print "Calculating D8 flow direction......"
    print "Input Pit Filled Elevation file: "+fel
    print "Input Number of Processes: "+str(inputProc)
    print "Output D8 Flow Direction File: "+p
    print "Output D8 Slope File: "+sd8
    # Construct command
     
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' d8flowdir -fel ' + '"' + fel + '"' + ' -p ' + '"' + p + '"' + ' -sd8 ' + '"' + sd8 + '"'
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir  + os.sep + 'd8flowdir -fel ' + '"' + fel + '"' + ' -p ' + '"' + p + '"' + ' -sd8 ' + '"' + sd8 + '"'
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    print "Command Line: "+cmd
    ##os.system(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "D8FlowDir"
    contentList.append('\n')
    contentList.append("#### Calculating D8 flow direction ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    

def DinfFlowDir(fel,inputProc,ang,slp,mpiexeDir = None,  exeDir=None):
    print "Calculating D-infinity direction......"
    print "Input Pit Filled Elevation file: "+fel
    print "Input Number of Processes: "+str(inputProc)
    print "Output Dinf Flow Direction File: "+ang
    print "Output Dinf Slope File: "+slp
    # Construct command 
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' dinfflowdir -fel ' + '"' + fel + '"' + ' -ang ' + '"' + ang + '"' + ' -slp ' + '"' + slp + '"'
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'dinfflowdir -fel ' + '"' + fel + '"' + ' -ang ' + '"' + ang + '"' + ' -slp ' + '"' + slp + '"'
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "DinfFlowDir"
    contentList.append('\n')
    contentList.append("#### Calculating D-infinity direction ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    
        
def AreaD8(p,Shapefile,weightgrid,edgecontamination,inputProc,ad8,mpiexeDir = None,  exeDir=None):
    print "Calculating D8 contributing area......"
    print "Input D8 Flow Direction file: "+p
    if os.path.exists(Shapefile):
        print "Input Outlets Shapefile: "+Shapefile
    if os.path.exists(weightgrid):
        print "Input Weight Grid: "+weightgrid
    print "Edge Contamination: "+edgecontamination
    print "Input Number of Processes: "+str(inputProc)
    print "Output D8 Contributing Area Grid: "+ad8
    # Construct command
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' aread8 -p ' + '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"'
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'aread8 -p ' + '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"'
    if os.path.exists(Shapefile):
        cmd = cmd + ' -o ' + '"' + Shapefile + '"'
    if os.path.exists(weightgrid):
        cmd = cmd + ' -wg ' + '"' + weightgrid + '"'
    if edgecontamination == 'false':
        cmd = cmd + ' -nc '
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "D8 contributing area"
    contentList.append('\n')
    contentList.append("#### Calculating D8 contributing area ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    
        
def AreaDinf(ang,shapefile,weightgrid,edgecontamination,inputProc,sca,mpiexeDir = None,  exeDir=None):
    print "Calculating D-infinity contributing area......"
    print "Input Dinf Flow Direction file: "+ang
    if os.path.exists(shapefile):
        print "Input Outlets Shapefile: "+shapefile
    if os.path.exists(weightgrid):
        print "Input Weight Grid: "+weightgrid
    print "Edge Contamination: "+edgecontamination
    print "Input Number of Processes: "+str(inputProc)
    print "Output Dinf Specific Catchment Area Grid: "+sca
    # Construct command
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' areadinf -ang ' + '"' + ang + '"' + ' -sca ' + '"' + sca + '"'
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'areadinf -ang ' + '"' + ang + '"' + ' -sca ' + '"' + sca + '"'
    if os.path.exists(shapefile):
        cmd = cmd + ' -o ' + '"' + shapefile + '"'
    if os.path.exists(weightgrid):
        cmd = cmd + ' -wg ' + '"' + weightgrid + '"'
    if edgecontamination == 'false':
        cmd = cmd + ' -nc '
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "D-inf contributing area"
    contentList.append('\n')
    contentList.append("#### Calculating D-infinity contributing area ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
 
## Specialized grid analysis

def DinfDistDown(ang,fel,src,statisticalmethod,distancemethod,edgecontamination,wg,inputProc,dd, mpiexeDir = None, exeDir=None):
    print "Calculating distance down to stream based on D-infinity model......"
    print "Input D-Infinity Flow Direction Grid: "+ang
    print "Input Pit Filled Elevation Grid: "+fel
    print "Input Stream Raster Grid: "+src
    print "Statistical Method: "+statisticalmethod
    print "Distance Method: "+distancemethod
    print "Edge Contamination: "+edgecontamination
    if os.path.exists(wg):
        print "Input Weight Path Grid: "+wg
    print "Input Number of Processes: "+str(inputProc)
    print "Output D-Infinity Drop to Stream Grid: "+dd

    # Construct command
    if statisticalmethod == 'Average':
        statmeth = 'ave'
    if statisticalmethod == 'Maximum':
        statmeth = 'max'
    if statisticalmethod == 'Minimum':
        statmeth = 'min'
    if distancemethod == 'Horizontal':
        distmeth = 'h'
    if distancemethod == 'Vertical':
        distmeth = 'v'
    if distancemethod == 'Pythagoras':
        distmeth = 'p'
    if distancemethod == 'Surface':
        distmeth = 's'
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' dinfdistdown -fel ' + '"' + fel + '"' + ' -ang ' + '"' + ang + '"' + ' -src ' + '"' + src + '"' + ' -dd ' + '"' + dd + '"' + ' -m ' + statmeth + ' ' + distmeth
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'dinfdistdown -fel ' + '"' + fel + '"' + ' -ang ' + '"' + ang + '"' + ' -src ' + '"' + src + '"' + ' -dd ' + '"' + dd + '"' + ' -m ' + statmeth + ' ' + distmeth
        
    if os.path.exists(wg):
        cmd = cmd + ' -wg ' + '"' + wg + '"'
    if edgecontamination == 'false':
        cmd = cmd + ' -nc '
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "Calculating Dinf distance down"
    contentList.append('\n')
    contentList.append("#### Calculating distance down to stream based on D-infinity model ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    


def MoveOutletsToStreams(p,src,shapefile,maxdistance,inputProc,om, mpiexeDir = None, exeDir=None):
    print "Moving outlet point(s) to streams......"
    print "Input D8 Flow Direction Grid: "+p
    print "Input Stream Raster Grid: "+src
    print "Input Outlets Shapefile: "+shapefile
    print "Minimum Threshold Value: "+str(maxdistance)
    print "Input Number of Processes: "+str(inputProc)

    print "Output Outlet Shapefile: "+om

    # Construct command
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' moveoutletstostreams -p ' + '"' + p + '"' + ' -src ' + '"' + src + '"' + ' -o ' + '"' + shapefile + '"' + ' -om ' + '"' + om + '"' + ' -md ' + str(maxdistance)
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'moveoutletstostreams -p ' + '"' + p + '"' + ' -src ' + '"' + src + '"' + ' -o ' + '"' + shapefile + '"' + ' -om ' + '"' + om + '"' + ' -md ' + str(maxdistance)
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "Moving outlet point to streams"
    contentList.append('\n')
    contentList.append("#### Moving outlet point(s) to streams ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    


def Threshold(ssa,mask,threshold,inputProc,src, mpiexeDir = None, exeDir=None):
    print "Stream definition according to threshold......"
    print "Input Accumulated Stream Source Grid: "+ssa
    if os.path.exists(mask):        
        print "Input Mask Grid: "+mask
    print "Threshold: "+str(threshold)
    print "Input Number of Processes: "+str(inputProc)

    print "Output Stream Raster Grid: "+src

    # Construct command
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' threshold -ssa ' + '"' + ssa + '"' + ' -src ' + '"' + src + '"' + ' -thresh ' + str(threshold)
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'threshold -ssa ' + '"' + ssa + '"' + ' -src ' + '"' + src + '"' + ' -thresh ' + str(threshold)
        
    if os.path.exists(mask):
        cmd = cmd + ' -mask ' + mask
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "Threshold to define stream"
    contentList.append('\n')
    contentList.append("#### Stream definition according to threshold ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    

def DropAnalysis(fel,p,ad8,ssa,shapefile,minthresh,maxthresh,numthresh,logspace,inputProc,drp, mpiexeDir = None, exeDir=None):
    print "Stream drop analysis for the optimal threshold......"
    print "Input Pit Filled Elevation Grid: "+fel
    print "Input D8 Flow Direction Grid: "+p
    print "Input D8 Contributing Area Grid: "+ad8
    print "Input Accumulated Stream Source Grid: "+ssa
    print "Input Outlets Shapefile: "+shapefile
    print "Minimum Threshold Value: "+str(minthresh)
    print "Maximum Threshold Value: "+str(maxthresh)
    print "Number of Threshold Values: "+str(numthresh)
    print "Logarithmic Spacing: "+logspace
    print "Input Number of Processes: "+str(inputProc)

    print "Output Drop Analysis Text File: "+drp

    # Construct command
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' dropanalysis -fel ' + '"' + fel + '"' + ' -p ' + '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"' + ' -ssa ' + '"' + ssa + '"' + ' -o ' + '"' + shapefile + '"' + ' -drp ' + '"' + drp + '"' + ' -par ' + str(minthresh) + ' ' + str(maxthresh) + ' ' + str(numthresh) + ' '
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'dropanalysis -fel ' + '"' + fel + '"' + ' -p ' + '"' + p + '"' + ' -ad8 ' + '"' + ad8 + '"' + ' -ssa ' + '"' + ssa + '"' + ' -o ' + '"' + shapefile + '"' + ' -drp ' + '"' + drp + '"' + ' -par ' + str(minthresh) + ' ' + str(maxthresh) + ' ' + str(numthresh) + ' '
    if logspace == 'false':    
        cmd = cmd + '1'
    else:
        cmd = cmd + '0'
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "Drop Analysis"
    contentList.append('\n')
    contentList.append("#### Stream drop analysis for the optimal threshold ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    


####   Functions added by Liangjun Zhu    ####

def D8DistDownToStream(p,fel,src,dist,distancemethod,thresh,inputProc,mpiexeDir = None, exeDir=None):
    
    print "Calculating distance down to stream based on D8 model......"
    print "Input D8 Flow Direction Grid: "+p
    print "Input filled DEM: "+fel
    print "Input Stream Raster Grid: "+src
    print "Distance calculating method: "+distancemethod
    print "Threshold: "+str(thresh)
    print "Input Number of Processes: "+str(inputProc)

    print "Output Distance To Streams: "+dist
    if distancemethod == 'Horizontal':
        distmeth = 'h'
    if distancemethod == 'Vertical':
        distmeth = 'v'
    if distancemethod == 'Pythagoras':
        distmeth = 'p'
    if distancemethod == 'Surface':
        distmeth = 's'
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' d8distdowntostream -p ' + '"' + p + '"' + ' -fel ' + '"' +fel+ '"' +' -src ' + '"' + src + '"' + ' -dist ' + '"' + dist + '"' +' -m '+distmeth+ ' -thresh ' + str(thresh)
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'd8distdowntostream -p ' + '"' + p + '"' + ' -fel ' + '"' +fel+ '"' +' -src ' + '"' + src + '"' + ' -dist ' + '"' + dist + '"' +' -m '+distmeth+ ' -thresh ' + str(thresh)
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "D8 distance down"
    contentList.append('\n')
    contentList.append("#### Calculating distance down to stream based on D8 model ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    

def D8DistUpToRidge(p,fel,du,distancemethod,statisticalmethod,inputProc,rdg=None,mpiexeDir = None, exeDir=None):
    print "Calculating distance up to ridges based on D8 model......"
    print "Input D8 Flow Direction Grid: "+p
    print "Input Pit Filled Elevation Grid: "+fel
    if not rdg is None:
        print "Input Ridge Source Grid: "+rdg
    print "Statistical Method: "+statisticalmethod
    print "Distance Method: "+distancemethod
    print "Input Number of Processes: "+str(inputProc)
    print "Output D-Infinity Distance Up: "+du

    # Construct command
    if statisticalmethod == 'Average':
        statmeth = 'ave'
    if statisticalmethod == 'Maximum':
        statmeth = 'max'
    if statisticalmethod == 'Minimum':
        statmeth = 'min'
    if distancemethod == 'Horizontal':
        distmeth = 'h'
    if distancemethod == 'Vertical':
        distmeth = 'v'
    if distancemethod == 'Pythagoras':
        distmeth = 'p'
    if distancemethod == 'Surface':
        distmeth = 's'
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' d8distuptoridge -p '
    else:
        cmd = 'mpiexec -n ' + str(inputProc) +  ' ' + exeDir + os.sep + 'd8distuptoridge -p '
    if not rdg is None:
        cmd = cmd + '"' + p + '"' +' -fel ' + '"' + fel + '"' + ' -rdg ' + '"' + rdg + '"' + ' -du ' + '"' + du + '"' + ' -m ' + statmeth + ' ' + distmeth
    else:
        cmd = cmd + '"' + p + '"' +' -fel ' + '"' + fel + '"' + ' -du ' + '"' + du + '"' + ' -m ' + statmeth + ' ' + distmeth
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "D8 distance up"
    contentList.append('\n')
    contentList.append("#### Calculating distance up to ridges based on D8 model ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    

def DinfDistUpToRidge(ang,fel,slp,propthresh,statisticalmethod,distancemethod,edgecontamination,inputProc,du,rdg=None, mpiexeDir = None, exeDir=None):
    print "Calculating distance up to ridges based on D-infinity model......"
    print "Input D-Infinity Flow Direction Grid: "+ang
    print "Input Pit Filled Elevation Grid: "+fel
    print "Input Slope Grid: "+slp
    if not rdg is None:
        print "Input Ridge Source Grid: "+rdg
    print "Input Proportion Threshold: "+str(propthresh)
    print "Statistical Method: "+statisticalmethod
    print "Distance Method: "+distancemethod
    print "Edge Contamination: "+edgecontamination
    print "Input Number of Processes: "+str(inputProc)

    print "Output D-Infinity Distance Up: "+du

    # Construct command
    if statisticalmethod == 'Average':
        statmeth = 'ave'
    if statisticalmethod == 'Maximum':
        statmeth = 'max'
    if statisticalmethod == 'Minimum':
        statmeth = 'min'
    if distancemethod == 'Horizontal':
        distmeth = 'h'
    if distancemethod == 'Vertical':
        distmeth = 'v'
    if distancemethod == 'Pythagoras':
        distmeth = 'p'
    if distancemethod == 'Surface':
        distmeth = 's'
    if exeDir is None:
        cmd = 'mpiexec -n ' + str(inputProc) + ' dinfdistuptoridge '
    else:
        cmd = 'mpiexec -n ' + str(inputProc) + ' ' + exeDir + os.sep + 'dinfdistuptoridge '
    if not rdg is None:
        cmd = cmd +' -ang ' + '"' + ang + '"'+' -fel '+ '"' + fel + '"' + ' -slp ' + '"' + slp + '"' +' -rdg ' + '"' + rdg + '"' +  ' -du ' + '"' + du + '"' + ' -m ' + statmeth + ' ' + distmeth + ' -thresh ' + str(propthresh)
    else:
        cmd = cmd +' -ang ' + '"' + ang + '"'+' -fel '+ '"' + fel + '"' + ' -slp ' + '"' + slp + '"' + ' -du ' + '"' + du + '"' + ' -m ' + statmeth + ' ' + distmeth + ' -thresh ' + str(propthresh)
    if edgecontamination == 'false':
        cmd = cmd + ' -nc '
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    #os.system(cmd)
    process=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "Dinf distance up"
    contentList.append('\n')
    contentList.append("#### Calculating distance up to ridges based on D-infinity model ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    

def Curvature(inputProc,fel,prof=None,plan=None,horiz=None,unspher=None,ave=None,max=None,min=None,mpiexeDir = None, exeDir=None):
    if exeDir is None:
        cmd = 'mpiexec -n '+str(inputProc)+' curvature'
    else:
        cmd = 'mpiexec -n '+str(inputProc)+ ' ' + exeDir + os.sep + 'curvature'
    if prof is None and plan is None and horiz is None and unspher is None and ave is None and max is None and min is None:
        cmd = cmd +' -fel ' + '"' + fel + '"'
    else:
        cmd = cmd +' -fel ' + '"' + fel + '"'+ ' -out '
    print "Input Pit Filled Elevation Grid: "+fel
    if not prof is None:
        print "Output Profile Curvature Grid: "+prof
        cmd = cmd +' -prof '+'"' + prof + '" '
    if not plan is None:
        print "Output Plan Curvature Grid: "+plan
        cmd = cmd +' -plan '+'"' + plan + '" '
    if not horiz is None:
        print "Output Horizontal Curvature Grid: "+horiz
        cmd = cmd +' -horiz '+'"' + horiz + '" '
    if not unspher is None:
        print "Output Nnsphericity Grid: "+unspher
        cmd = cmd +' -unspher '+'"' + unspher + '" '
    if not ave is None:
        print "Output Average Curvature Grid: "+ave
        cmd = cmd +' -ave '+'"' + ave + '" '
    if not max is None:
        print "Output Maximum Curvature Grid: "+max
        cmd = cmd +' -max '+'"' + max + '" '
    if not min is None:
        print "Output Minimum Curvature Grid: "+min
        cmd = cmd +' -min '+'"' + min + '" '
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    print "Input Number of Processes: "+str(inputProc)
    #os.system(cmd)
    process = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "Curvature"
    contentList.append('\n')
    contentList.append("#### Curvature ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    
def SelectTypLocSlpPos(inputConf,outputConf,inputProc,outlog=None,mpiexeDir = None, exeDir=None):
    print "Selecting Typical Slope Position Location and Calculating Fuzzy Inference Parameters"
    print "    Input configuration file: "+inputConf
    print "    Output configuration file: "+outputConf
    if outlog is not None:
        print "    Output Log file: "+outlog
    
    if exeDir is None:
        cmd = 'mpiexec -n '+str(inputProc)+' selecttyplocslppos ' + '"' + inputConf + '"' + ' "' + outputConf + '" '
    else:
        cmd = 'mpiexec -n '+str(inputProc)+ ' ' + exeDir + os.sep + 'selecttyplocslppos ' + '"' + inputConf + '"' + ' "' + outputConf + '" '
    if outlog is not None:
        cmd = cmd + ' "' + outlog + '" '
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    print "Input Number of Processes: "+str(inputProc)
    ##os.system(cmd)
    process = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "SelectTypLocSlpPos %s" % inputConf.rpartition(os.sep)[-1]
    contentList.append('\n')
    contentList.append("#### Select Typical Location of %s ####" % inputConf.rpartition(os.sep)[-1])
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    
def FuzzySlpPosInference(config,inputProc,values = None, mpiexeDir = None, exeDir=None):
    print "Fuzzy Slope Position Inference"
    print "    Configuration file: "+config
    if exeDir is None:
        cmd = 'mpiexec -n '+str(inputProc)+' fuzzyslpposinference ' + '"' + config + '"'
    else:
        cmd = 'mpiexec -n '+str(inputProc)+ ' ' + exeDir + os.sep + 'fuzzyslpposinference ' + '"' + config + '"'
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    if values is not None:
        cmd = cmd + ' -val ' + '"' + values + '"'
    
    print "Command Line: "+cmd
    print "Input Number of Processes: "+str(inputProc)
    ##os.system(cmd)
    process = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "FuzzySlpPosInference %s" % config.rpartition(os.sep)[-1]
    contentList.append('\n')
    contentList.append("#### Fuzzy Slope Position Inference of %s ####" % config.rpartition(os.sep)[-1])
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    

    
def HardenSlpPos(rdg,shd,bks,fts,vly,inputProc,hard,maxsimi,sechard=None,secsimi=None,spsim=None,spsi=None,mpiexeDir = None, exeDir=None):
    print "Harden Slope Position Inference"
    print "Ridge Similarity file: "+rdg
    print "Shoulder slope similarity file: "+shd
    print "Back slope similarity file: "+bks
    print "Foot slope similarity file: "+fts
    print "Valley similarity file: "+vly
    print "Hard slope position file: "+hard
    print "Maximum similarity: "+maxsimi
    
    if exeDir is None:
        cmd = 'mpiexec -n '+str(inputProc)+' hardenslppos -rdg ' + '"' + rdg + '"' + ' -shd ' + '"' + shd + '"' + ' -bks ' + '"' + bks + '"' + ' -fts ' + '"' + fts + '"' + ' -vly ' + '"' + vly + '"' + ' -maxS ' + '"' + hard + '" ' + '"' + maxsimi + '"'
    else:
        cmd = 'mpiexec -n '+str(inputProc)+ ' ' + exeDir + os.sep + 'hardenslppos -rdg ' + '"' + rdg + '"' + ' -shd ' + '"' + shd + '"' + ' -bks ' + '"' + bks + '"' + ' -fts ' + '"' + fts + '"' + ' -vly ' + '"' + vly + '"' + ' -maxS ' + '"' + hard + '" ' + '"' + maxsimi + '"'
    if (not sechard is None) and (not secsimi is None):
        print "Second Hard slope position file: "+sechard
        print "Second Maximum similarity: "+secsimi
        cmd = cmd + ' -secS ' + '"' + sechard + '" ' + '"' + secsimi + '"'
        if (not spsim is None) and (not spsi is None):
            print "Slope Position Sequence Index: "+spsi
            cmd = cmd + ' -m '+str(spsim)+' "'+spsi+'"'
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    print "Input Number of Processes: "+str(inputProc)
    ##os.system(cmd)
    process = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "HardenSlpPos"
    contentList.append('\n')
    contentList.append("#### Harden classification ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    
    
def SimpleCalculator(inputa,inputb,output,operator,inputProc,mpiexeDir = None, exeDir=None):
    if exeDir is None:
        cmd = 'mpiexec -n '+str(inputProc)+' simplecalculator -in '+ '"' + inputa + '"' + ' "' + inputb + '"' +' -out '+ '"' + output + '"' + ' -op '+ str(operator)
    else:
        cmd = 'mpiexec -n '+str(inputProc)+ ' ' + exeDir + os.sep + 'simplecalculator -in '+ '"' + inputa + '"' + ' "' + inputb + '"' +' -out '+ '"' + output + '"' + ' -op '+ str(operator)
    if mpiexeDir is not None:
        cmd = mpiexeDir + os.sep + cmd
    
    print "Command Line: "+cmd
    print "Input Number of Processes: "+str(inputProc)
    ##os.system(cmd)
    process = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    contentList = []
    timeDict = {'name':None,'readt':0,'writet':0,'computet':0,'totalt':0}
    timeDict['name'] = "SimpleCalculator"
    contentList.append('\n')
    contentList.append("#### Simple Calculator ####")
    for line in process.stdout.readlines():
        contentList.append(line.split(LF)[0])
        #print line
        if line.find("Read time") >= 0:
            timeDict['readt'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Compute time") >= 0:
            timeDict['computet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Write time") >= 0:
            timeDict['writet'] = line.split(LF)[0].split(':')[-1]
        elif line.find("Total time") >= 0:
            timeDict['totalt'] = line.split(LF)[0].split(':')[-1]
    WriteLog(Log_all,contentList)
    WriteTimeLog(Log_runtime,timeDict)
    
    
        
####           END DEFINITION             ####
