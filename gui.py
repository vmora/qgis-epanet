# -*- coding: UTF-8 -*-

from SpatialiteAlgorithmProvider import SpatialiteAlgorithmProvider
from EpanetAlgorithmProvider import EpanetAlgorithmProvider
from processing.core.Processing import Processing

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from pylab import *

import os

class Gui:

    def __init__(self, iface):
        self.iface = iface
        self.actions = []
        pass
    
    def initGui(self):

        self.actions.append( QAction(
            QIcon(os.path.dirname(__file__) + "/timeplot.svg"),
            u"timeplot", self.iface.mainWindow()) )
        self.actions[-1].setWhatsThis("timeplot")
        self.actions[-1].triggered.connect(self.timeplot)

        for a in self.actions:
            self.iface.addToolBarIcon(a)

        print "here"
        self.epanetAlgoProvider = EpanetAlgorithmProvider()
        print self.epanetAlgoProvider 
        Processing.addProvider(self.epanetAlgoProvider, True)
        self.spatialiteAlgorithmProvider = SpatialiteAlgorithmProvider()
        Processing.addProvider(self.spatialiteAlgorithmProvider, True)
    
    def unload(self):
        Processing.removeProvider(self.spatialiteAlgorithmProvider)
        Processing.removeProvider(self.epanetAlgoProvider)
        # Remove the plugin menu item and icon
        for a in self.actions:
            self.iface.removeToolBarIcon(a)

    def timeplot(self):
        layer = self.iface.activeLayer()
        print layer.name()
        if layer.name().lower() == 'reservoirs' or layer.name().lower() == 'tanks':
            res = QgsMapLayerRegistry.instance().mapLayersByName('Node output table')
            if res: 
                assert(len(res) == 1)
                fig,p = subplots(1,len(layer.selectedFeatures()))
                for i,s in enumerate(layer.selectedFeatures()):
                    x,y = [],[]
                    for f in res[0].getFeatures(QgsFeatureRequest(QgsExpression("Node = '"+s['ID Noeud']+"'"))):
                        #print s['ID Noeud'],' ',f['Time'],' ',f['Head']
                        t = f['Time'].split(' ')[1].split(':')
                        x.append(int(t[0])*60+int(t[1]))
                        y.append(f['Head'])
                    p[i].plot(x,y)
                    p[i].set_title(layer.name()+' '+s['ID Noeud'])
                    p[i].set_xlabel('Time [min]')
                    p[i].set_ylabel('Head [m]')
                show()

        if layer.name().lower() == 'pumps':
            res = QgsMapLayerRegistry.instance().mapLayersByName('Link output table')
            if res: 
                assert(len(res) == 1)
                nbfeat = len(layer.selectedFeatures())
                fig,p = subplots(1,nbfeat)
                if nbfeat == 1 : p = [p]
                for i,s in enumerate(layer.selectedFeatures()):
                    x,y = [],[]
                    for f in res[0].getFeatures(QgsFeatureRequest(QgsExpression("Link = '"+s['ID Arc']+"'"))):
                        #print s['ID Noeud'],' ',f['Time'],' ',f['Head']
                        t = f['Time'].split(' ')[1].split(':')
                        x.append(int(t[0])*60+int(t[1]))
                        y.append(f['Flow'])
                    p[i].plot(x,y)
                    p[i].set_title(layer.name()+' '+s['ID Arc'])
                    p[i].set_xlabel('Time [min]')
                    p[i].set_ylabel('Flow [m3/h]')
                show()


        pass
