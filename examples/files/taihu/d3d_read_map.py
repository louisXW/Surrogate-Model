#!/usr/bin/python

# MIT License
#
# Copyright (c) 2016 Daily Actie
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Author: Quan Pan <quanpan302@hotmail.com>
# License: MIT License
# Create: 2016-12-02

# 0 --py:Success::
# 1 --py:Warning::
# 2 --py:Error::
# --py:Start::['+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+']
# --py:End::  ['+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+']
# --py:Test::

import os, sys, getopt, datetime
import warnings
warnings.filterwarnings(action="ignore", category=Warning)

import matplotlib as mpl
if os.environ.get('DISPLAY','') == '':
    # print('--py:Warning:: No display found. Using non-interactive Agg backend')
    mpl.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

import json

# from surrogate.files.delft3d import Delft3D
# def main(taihuDir, caseName, varName, iseg, itime):

sys.path.append("..")
from surrogate.files.delft3d import Delft3D


def main(argv):
    taihuDir = ''
    caseName = ''
    varName = ''
    iseg = 0
    itime = 0
    try:
        opts, args = getopt.getopt(argv,"hd:c:v:p:t:",["dir=","case=","variable=","point=","time="])
    except getopt.GetoptError:
        print sys.argv[0]+' -d <dir> -c <case> -v <variable> -p <point> -t <time>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print sys.argv[0]+' -d <dir> -c <case> -v <variable> -p <point> -t <time>'
            sys.exit()
        elif opt in ("-d", "--dir"):
            taihuDir = arg
        elif opt in ("-c", "--case"):
            caseName = arg
        elif opt in ("-v", "--variable"):
            varName = arg
        elif opt in ("-p", "--point"):
            iseg = int(arg)
        elif opt in ("-t", "--time"):
            itime = int(arg)

    print '--py:Start::['+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'] '+caseName

    if taihuDir and caseName and varName:
        readD3DWaq(taihuDir, caseName, varName, iseg, itime)

    print '--py:End::  ['+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'] '+caseName


def readD3DWaq(taihuDir, caseName, varName, iseg=0, itime=0):
    print '--py:Test:: ['+ taihuDir+', '+caseName+', '+varName+', '+str(iseg)+', '+str(itime)+']'
    z_min = 0.0
    z_max = 3.5

    dx = 500.0 # meter
    dy = 500.0 # meter
    hour2sec = 24*3600

    gridFname = taihuDir+'/delcoupl/couplnef.txt'
    mapFname  = taihuDir+'/'+caseName+'/taihu.map'

    d3d = Delft3D(gridFname=gridFname, mapFname=mapFname)
    moname, varlist, maptime, nseg, nvar, ntime = d3d.initWaqMap()
    # for i in range(len(maptime)):
    #     print '--py:Test:: '+str(i)+':\t'+str(maptime[i])
    # for i in range(len(varlist)):
    #     print '--py:Test:: '+str(i)+':\t'+varlist[i]

    if iseg>=nseg:
        print '--py:Error:: iseg='+str(iseg)+' > nseg='+str(nseg)
        sys.exit(1)

    if varName in varlist:
        ivar = varlist.index(varName)
    else:
        print '--py:Error:: varName='+varName+' is not in the varlist.'
        for i in range(len(varlist)):
            print str(i)+'\t'+varlist[i]
        sys.exit(1)

    if itime>=ntime:
        print '--py:Error:: itime='+str(itime)+' > ntime='+str(ntime)
        for i in range(len(maptime)):
            print str(i)+'\t'+str(maptime[i])
        sys.exit(1)


    print '--py:Test:: Data size [nseg='+str(nseg)+',nvar='+str(nvar)+',ntime='+str(ntime)+']'
    print '--py:Test:: Data read [iseg='+str(iseg)+',ivar='+str(ivar)+',itime='+str(itime)+']'

    objfunFname = taihuDir+'/'+caseName+'/taihu_objfun.txt'

    strHisTitle = caseName+'/his_'+varlist[ivar]+'_s'+str(iseg)
    strMapTitle = caseName+'/map_'+varlist[ivar]+'_t'+str(itime)
    # strMapTitle = caseName+'/map_'+varlist[ivar]+'_t'+str(maptime[itime])
    hisFigFname = taihuDir+'/'+strHisTitle+'.png'
    mapFigFname = taihuDir+'/'+strMapTitle+'.png'
    mapJsonFname= taihuDir+'/'+strMapTitle+'.json'

    dataHis = []
    dataMap = []
    jsonData = {'legend': '', 'iseg': -9999, 'itime': -9999, 'x': [], 'y': [], 'z': [], 'zMin': z_min, 'zMax': z_max}

    # d3d = Delft3D(gridFname=gridFname, mapFname=mapFname)
    # moname, varlist, maptime, nseg, nvar, ntime = d3d.initWaqMap()
    # # for i in range(len(maptime)):
    # #     print '--py:Test:: '+str(i)+':\t'+str(maptime[i])
    # # for i in range(len(varlist)):
    # #     print '--py:Test:: '+str(i)+':\t'+varlist[i]
    #
    # nrow, ncol, gridX, gridY, gridIndex = d3d.getWaqGrid()
    # maptime = [x/hour2sec for x in maptime]

    # dataOffset = d3d.getWaqMapDataAtOffset(iseg=iseg,ivar=ivar,itime=itime) # ok
    # # print dataOffset

    # dataTime = d3d.getWaqMapDataAtTime(itime=itime) # ok
    # # print dataTime[iseg][ivar][0]

    # dataSeg = d3d.getWaqMapDataAtSegment(iseg=iseg) # ok
    # print dataSeg[0][ivar][itime]
    # print dataSeg[0][ivar][:]
    # for i in range(len(maptime)):
    #     print '--py:Test:: '+varlist[ivar]+':\t'+str(maptime[i])+'\t'+str(dataSeg[0][ivar][i])
    # dataHis = dataSeg[0][ivar][:]

    # dataVar = d3d.getWaqMapDataAtVariable(ivar=ivar) # ok
    # # print dataVar[iseg][0][itime]
    # # print dataVar[iseg][0][:]
    # dataHis = dataVar[iseg][0][:]

    nrow, ncol, gridX, gridY, gridIndex = d3d.getWaqGrid()
    maptime = [x/hour2sec for x in maptime]

    if iseg==-9999 and itime==-9999:
        # 20170601-update original code
        print '--py:Test:: Old iseg='+str(iseg)+' itime='+str(itime)+' any time'

        checkData = -999999.99
        for jitime in range(ntime):
            tempDataZ = d3d.getWaqMapDataAtVariableTime(ivar=ivar, itime=jitime) # ok
            for i in range(nrow):
                for j in range(ncol):
                    if gridIndex[i][j]>0:
                        if tempDataZ[gridIndex[i][j]][0] > checkData:
                            checkData = tempDataZ[gridIndex[i][j]][0]
                            jseg  = gridIndex[i][j]
                            jtime = jitime
        print '--py:Test:: New iseg='+str(jseg)+' itime='+str(jtime)

    elif iseg==-9999 and itime>=0:
        # 20170601-update original code
        print '--py:Test:: Old iseg='+str(iseg)+' any seg'
        jtime = itime

        tempDataZ = d3d.getWaqMapDataAtVariableTime(ivar=ivar, itime=jtime) # ok
        checkData = -999999.99
        for i in range(nrow):
            for j in range(ncol):
                if gridIndex[i][j]>0:
                    if tempDataZ[gridIndex[i][j]][0] > checkData:
                        checkData = tempDataZ[gridIndex[i][j]][0]
                        jseg = gridIndex[i][j]
        print '--py:Test:: New iseg='+str(jseg)

    elif iseg>=0 and itime==-9999:
        # 20170601-update original code
        print '--py:Test:: Old itime='+str(itime)+' any time'
        jseg = iseg

        tempDataSeg = d3d.getWaqMapDataAtSegment(iseg=jseg) # ok
        tempDataHis = tempDataSeg[0][ivar][:]
        tempDataHis = np.array(tempDataHis)
        jtime = np.nanargmax(tempDataHis)
        print '--py:Test:: New itime='+str(jtime)

    elif iseg>=0 and itime>=0:
        # 20170601-original code
        print '--py:Test:: Old iseg='+str(iseg)+' itime='+str(itime)
        jseg = iseg
        jtime = itime
        print '--py:Test:: New iseg='+str(jseg)+' itime='+str(jtime)

    else:
        print '--py:Error:: iseg='+str(iseg)+' itime='+str(itime)
        sys.exit(1)


    strHisTitle = caseName+'/his_'+varlist[ivar]+'_s'+str(jseg)
    strMapTitle = caseName+'/map_'+varlist[ivar]+'_t'+str(jtime)

    jsonData['legend'] = varlist[ivar]
    jsonData['iseg']   = jseg
    jsonData['itime']  = jtime


    dataSeg = d3d.getWaqMapDataAtSegment(iseg=jseg) # ok
    dataHis = dataSeg[0][ivar][:]
    dataHis = np.array(dataHis)

    dataZ = d3d.getWaqMapDataAtVariableTime(ivar=ivar, itime=jtime) # ok
    for i in range(nrow):
        dataMap.append([dataZ[gridIndex[i][j]][0] if gridIndex[i][j]>0 else 0 for j in range(ncol)])
    dataMap = np.array(dataMap)

    for i in range(nrow):
        for j in range(ncol):
            if gridIndex[i][j]>0:
                jsonData['x'].append(gridX[i][j])
                jsonData['y'].append(gridY[i][j])
                jsonData['z'].append(dataZ[gridIndex[i][j]][0])
    # import random
    # jsonDataDF = {'legend': varlist[ivar], 'x': [], 'y': [], 'z': [], 'zMin': 0.4, 'zMax': 1.0}
    # for i in range(0,nrow,5):
    #     for j in range(0,ncol,5):
    #         if gridIndex[i][j]>0:
    #             jsonDataDF['x'].append(gridX[i][j])
    #             jsonDataDF['y'].append(gridY[i][j])
    #             jsonDataDF['z'].append(random.uniform(0.5, 0.55))
    # saveJsonMap(taihuDir+'/df.json', jsonDataDF)

    gridY = np.array(gridY)
    gridX = np.array(gridX)
    gridY = gridY*dy
    gridX = gridX*dx

    dataMap[gridX==0] = np.NaN
    gridY[gridX==0]   = np.NaN
    gridX[gridX==0]   = np.NaN

    # gridIndex = np.array(gridIndex)
    # dataMap[gridIndex==9969] = np.NaN

    dataMap = np.ma.masked_invalid(dataMap)
    gridY   = np.ma.masked_invalid(gridY)
    gridX   = np.ma.masked_invalid(gridX)

    # z_min, z_max = np.nanmin(z), np.nanmax(z)

    # method-01
    savePlotHis(hisFigFname, maptime, dataHis, varlist, ivar, strHisTitle)
    savePlotMap(mapFigFname, gridX, gridY, dataMap, z_min, z_max, strMapTitle)
    saveJsonMap(mapJsonFname, jsonData)
    if not os.path.isfile(objfunFname):
        saveObj(objfunFname, dataMap, dataHis, jseg, jtime)

    # # method-02
    # if not os.path.isfile(hisFigFname):
    #     savePlotHis(hisFigFname, maptime, dataHis, varlist, ivar, strHisTitle)
    # if not os.path.isfile(mapFigFname):
    #     savePlotMap(mapFigFname, gridX, gridY, dataMap, z_min, z_max, strMapTitle)
    # if not os.path.isfile(mapJsonFname):
    #     saveJsonMap(mapJsonFname, jsonData)
    # if not os.path.isfile(objfunFname):
    #     saveObj(objfunFname, dataMap, dataHis, jseg, jtime)

    # # method-03
    # if os.path.isfile(objfunFname):
        # if not os.path.isfile(hisFigFname):
        #     savePlotHis(hisFigFname, maptime, dataHis, varlist, ivar, strHisTitle)
        #
        # if not os.path.isfile(mapFigFname):
        #     savePlotMap(mapFigFname, gridX, gridY, dataMap, z_min, z_max, strMapTitle)
        #
        # # saveJsonMap(mapJsonFname, jsonData)
        # if not os.path.isfile(mapJsonFname):
        #     saveJsonMap(mapJsonFname, jsonData)
    # else:
    #     saveObj(objfunFname, dataMap, dataHis, jseg, jtime)


def saveObj(objfunFname, dataMap, dataHis, iseg, itime):
    with open(objfunFname,'wt') as objfunFref:
        obj1 = objfunMean(data=dataMap)
        obj2 = objfunMax(data=dataHis)
        objfunFref.write('%.6f\t%.6f\t%i\t%i\n' % (obj1, obj2, iseg, itime))

def objfunMean(data):
    obj = np.nanmean(data)
    return obj

def objfunMax(data):
    obj = np.nanmax(data)
    return obj

def savePlotHis(hisFigFname, x, z, varlist, ivar, strHisTitle):
    print '--py:Start:: Plot his.'
    plt.plot(x,z)
    plt.title(strHisTitle)
    plt.xlabel('time [day]')
    plt.ylabel(varlist[ivar]+' [g/m^3]')
    plt.savefig(hisFigFname)
    # plt.show()
    plt.clf()

def savePlotMap(mapFigFname, x, y, z, z_min, z_max, strMapTitle):
    print '--py:Start:: Plot map.'
    plt.pcolor(x, y, z, cmap='jet', vmin=z_min, vmax=z_max)
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.colorbar()
    plt.title(strMapTitle)
    plt.xlabel('x [m]')
    plt.ylabel('y [m]')
    plt.savefig(mapFigFname)
    # plt.show()
    plt.clf()

def saveJsonMap(mapJsonFname, jsonData):
    print '--py:Start:: JSON map.'

    jsonFref = open(mapJsonFname,'wt')
    json.dump(jsonData, jsonFref, indent=4)
    jsonFref.close()


if __name__ == "__main__":
    # icaseStart = 0
    # icaseEnd = 2
    #
    # taihuDir = '../../../examples/files/taihu'
    # caseName=''
    # varName='GREENS'
    # iseg=0
    # itime=0
    #
    # # # caseName = "s%08d" % 0
    # # iseg=10011
    # # ivar=79 # 79	GREENS
    # # itime=120
    # #
    # # # caseName = "s%08d" % 1
    # # iseg=10011
    # # ivar=46 # 46	GREENS
    # # itime=29
    #
    # # --py:[icaseStart = 0, icaseEnd = 2] => [s00000000, s00000001]
    # for icase in range(icaseStart,icaseEnd):
    #     caseName = "s%08d" % icase
    #     main(taihuDir, caseName, varName, iseg, itime)

    # # --sh:[icaseStart = 1, icaseEnd = 2] => [t00000001, t00000002]
    # # python ./test_delft3d.py -d "$taihuDir" -c "$caseName" -v "$varName" -p "$iseg" -t "$itime"
    main(sys.argv[1:])

