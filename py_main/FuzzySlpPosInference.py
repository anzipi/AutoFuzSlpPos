#! /usr/bin/env python
# coding=utf-8
# @Description: Prepare configure file for fuzzy slope position inference program
# @Author: Liang-Jun Zhu
#
import TauDEM
from Nomenclature import *
from Util import *


def FuzzySlpPosInference():
    if AutoInfParams:
        RPIRangeDict = dict()
        for slppos in SlpPosItems:
            RPIRangeDict[slppos] = ValueRanges[slppos][0]
        # print RPIRangeDict
        # InferParams = [] for each slope position
        for i in range(len(SlpPosItems)):
            curRng = RPIRangeDict[SlpPosItems[i]]
            if i == 0:  # for Ridge, S: w1 = Rdg.max-Shd.max
                nextRng = RPIRangeDict[SlpPosItems[i+1]]
                tempw1 = curRng[2] - nextRng[2]
                InferParams[SlpPosItems[i]].append(['rpi', 'S', tempw1, 2, 0.5, 1, 0, 1])
            elif i == len(SlpPosItems) - 1:  # for Valley, Z: w2 = Fts.max-Vly.max
                beforeRng = RPIRangeDict[SlpPosItems[i-1]]
                tempw2 = beforeRng[2] - curRng[2]
                InferParams[SlpPosItems[i]].append(['rpi', 'Z', 1, 0, 1, tempw2, 2, 0.5])
            else:  # for other slope positions, B: w1 = w2 = min(cur.min-next.max, before.min-cur.max)
                nextRng = RPIRangeDict[SlpPosItems[i+1]]
                beforeRng = RPIRangeDict[SlpPosItems[i-1]]
                tempw = min(curRng[1] - nextRng[2], beforeRng[1] - curRng[2])
                InferParams[SlpPosItems[i]].append(['rpi', 'B', tempw, 2, 0.5, tempw, 2, 0.5])

        # RPIExtInfo = [RdgExtractionInfo[0], ShdExtractionInfo[0], BksExtractionInfo[0], FtsExtractionInfo[0],
        #               VlyExtractionInfo[0]]
        # tempw1 = RPIExtInfo[0][1] - RPIExtInfo[1][2]
        # RdgInferenceInfo.append(['RPI', 'S', tempw1, 2, 0.5, 1, 0, 1])  # Ridge:S: w1 = Rdg.min-Shd.max
        # tempw = min(RPIExtInfo[1][1] - RPIExtInfo[2][2], RPIExtInfo[0][1] - RPIExtInfo[1][2])
        # ShdInferenceInfo.append(['RPI', 'B', tempw, 2, 0.5, tempw, 2,
        #                          0.5])  # Shoulder slope:B: w1 = w2 = min(Shd.min-Bks.max, Rdg.min-Shd.max)
        # tempw = min(RPIExtInfo[2][1] - RPIExtInfo[3][2], RPIExtInfo[1][1] - RPIExtInfo[2][2])
        # BksInferenceInfo.append(['RPI', 'B', tempw, 2, 0.5, tempw, 2,
        #                          0.5])  # Back slope:B: w1 = w2 = min(Bks.min-Fts.max, Shd.min-Bks.max)
        # tempw = min(RPIExtInfo[3][1] - RPIExtInfo[4][2], RPIExtInfo[2][1] - RPIExtInfo[3][2])
        # FtsInferenceInfo.append(['RPI', 'B', tempw, 2, 0.5, tempw, 2,
        #                          0.5])  # Foot slope:B: w1 = w2 = min(Fts.min-Vly.max, Bks.min-Fts.max)
        # tempw2 = RPIExtInfo[3][1] - RPIExtInfo[4][2]
        # VlyInferenceInfo.append(['RPI', 'Z', 1, 0, 1, tempw2, 2, 0.5])  # Valley:Z: w2 = Fts.min-Vly.max
    # ##else:
    # ##    XXXInferenceInfo is user-defined in Config.py

    # SlpPosItems = [
    #     [RdgInfConfig, RdgTyp, RdgTag, RdgInferenceInfo, DistanceExponentForIDW, RdgInf, RdgInfRecommend, RdgExtLog], \
    #     [ShdInfConfig, ShdTyp, ShdTag, ShdInferenceInfo, DistanceExponentForIDW, ShdInf, ShdInfRecommend, ShdExtLog], \
    #     [BksInfConfig, BksTyp, BksTag, BksInferenceInfo, DistanceExponentForIDW, BksInf, BksInfRecommend, BksExtLog], \
    #     [FtsInfConfig, FtsTyp, FtsTag, FtsInferenceInfo, DistanceExponentForIDW, FtsInf, FtsInfRecommend, FtsExtLog], \
    #     [VlyInfConfig, VlyTyp, VlyTag, VlyInferenceInfo, DistanceExponentForIDW, VlyInf, VlyInfRecommend, VlyExtLog]]
    for slppos in SlpPosItems:
        if not AutoInfParams:  ## if not use automatically recommended parameters
            if not ModifyInfConfFile:
                configInfo = open(InfConfigDict[slppos], 'w')
                configInfo.write("PrototypeGRID\t%s\n" % TypDict[slppos])
                configInfo.write("ProtoTag\t%s\n" % str(TagDict[slppos]))
                configInfo.write("ParametersNUM\t%s\n" % str(len(InferParams[slppos])))
                for param in InferParams[slppos]:
                    configInfo.write("Parameters\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    param[0], TerrainAttrDict[param[0]], param[1], str(param[2]), str(param[3]), str(param[4]),
                    str(param[5]), str(param[6]), str(param[7])))
                configInfo.write("DistanceExponentForIDW\t%s\n" % str(DistanceExponentForIDW))
                configInfo.write("OUTPUT\t%s\n" % InfFileDict[slppos])
                configInfo.flush()
                configInfo.close()
        else:
            paramsConfList = []
            for line in open(InfRecommendDict[slppos]):
                paramsConfList.append(line)
            configInfo = open(InfConfigDict[slppos], 'w')
            configInfo.write("PrototypeGRID\t%s\n" % TypDict[slppos])
            configInfo.write("ProtoTag\t%s\n" % str(TagDict[slppos]))
            configInfo.write("ParametersNUM\t%s\n" % str(len(paramsConfList) + 1))
            for param in InferParams[slppos]:
                if param[0] == 'rpi':
                    configInfo.write("Parameters\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                    param[0], TerrainAttrDict[param[0]], param[1], str(param[2]), str(param[3]), str(param[4]),
                    str(param[5]), str(param[6]), str(param[7])))
            for paramline in paramsConfList:
                configInfo.write("%s" % paramline)
            configInfo.write("DistanceExponentForIDW\t%s\n" % str(DistanceExponentForIDW))
            configInfo.write("OUTPUT\t%s\n" % InfFileDict[slppos])
            configInfo.close()
        TauDEM.FuzzySlpPosInference(InfConfigDict[slppos], inputProc, mpiexeDir=mpiexeDir,
                                    exeDir=exeDir, hostfile=hostfile)

    if not CalSecHardSlpPos:
        global SecHardenSlpPos
        SecHardenSlpPos = None
        global SecMaxSimilarity
        SecMaxSimilarity = None
        if not CalSPSI:
            global SPSIfile
            SPSIfile = None
    TauDEM.HardenSlpPos(RdgInf, ShdInf, BksInf, FtsInf, VlyInf, inputProc, HardenSlpPos, MaxSimilarity,
                        sechard=SecHardenSlpPos, secsimi=SecMaxSimilarity, spsim=SPSImethod, spsi=SPSIfile,
                        mpiexeDir=mpiexeDir, exeDir=exeDir, hostfile=hostfile)
if __name__ == '__main__':
    ini, proc, root = GetInputArgs()
    LoadConfiguration(ini, proc, root)
    FuzzySlpPosInference()
