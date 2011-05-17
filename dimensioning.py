from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import sys, os, time
import resources
import tools.utils

from tools.vertexfindertool import VertexFinderTool
from tools.dimensioninggui import DimensioningGui
from tools.rectangularpoint import RectangularPoint


class Dimensioning:

    def __init__(self, iface):
        ## Save reference to the QGIS interface.
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
          
        ## Get the saved settings.
#        self.settings = QSettings("CatAIS","freeframe")      

        self.p1 = None
        self.p2 = None
        
    
    def initGui(self):
        self.action_select2vertex = QAction(QIcon(":/plugins/dimensioning/icons/select2vertex.png"), "Select two vertex points", self.iface.mainWindow())
        self.action_select2vertex.setCheckable(True)      
        self.action_dimensioning= QAction(QIcon(":/plugins/dimensioning/icons/dimensioning.png"),  "Draw dimensioning",  self.iface.mainWindow())
        
        QObject.connect(self.action_select2vertex, SIGNAL("triggered()"), self.select2vertex)
        QObject.connect(self.action_dimensioning,  SIGNAL("triggered()"),  self.showDialog) 
        QObject.connect(self.canvas, SIGNAL("mapToolSet(QgsMapTool*)"), self.deactivate)
        
        self.iface.addPluginToMenu(self.action_select2vertex.tr("Dimensioning"), self.action_select2vertex)
        self.iface.addPluginToMenu(self.action_dimensioning.tr("Dimensioning"), self.action_dimensioning)        
        
        self.toolBar = self.iface.addToolBar("Dimensioning")
        self.toolBar.setObjectName("Dimensioning")
        self.toolBar.addAction(self.action_select2vertex)       
        self.toolBar.addAction(self.action_dimensioning)    
        
        
    def select2vertex(self):
        mc = self.canvas
        layer = mc.currentLayer()

        self.tool = VertexFinderTool(self.canvas)                 
        mc.setMapTool(self.tool)
        self.action_select2vertex.setChecked(True)      
        
        QObject.connect(self.tool, SIGNAL("vertexFound(PyQt_PyObject)"), self.storePoints)                
    

    def storePoints(self, result):
        print result
        self.p1 = result[0]
        self.p2 = result[1]        
        
    
    def showDialog(self):
        if self.p1 == None or self.p2 == None:
            QMessageBox.information(None,  "Cancel",  "No points selected.")
        else:        
            print "showDialog"
            self.ctrl = DimensioningGui(self.iface.mainWindow())
            self.ctrl.initGui()
            self.ctrl.show()

            QObject.connect(self.ctrl, SIGNAL("dimensioningOffsets(double, double, double, int, bool)"), self.calculateDimensioning)
            QObject.connect(self.ctrl, SIGNAL("closeDimensioningGui()"), self.deactivate)            
            QObject.connect(self.ctrl, SIGNAL("unsetTool()"), self.unsetTool)        
    
    def calculateDimensioning(self, length, startOffset, endOffset, layer_id, invert):
        print length
        print startOffset
        print endOffset
        print invert
        
        pt1 = QgsPoint()
        pt1.setX(self.p1.x())
        pt1.setY(self.p1.y())
        pt2 = QgsPoint()
        pt2.setX(self.p2.x())
        pt2.setY(self.p2.y())              
        
        # Distanz zwischen beiden Punkten
        dist = pt1.sqrDist(pt2)**0.5
        print dist
        
        # Hilfslinien berechnen
        if length != 0:
        
            # Punkte fuer pt1
            if startOffset == 0:
                pt1HelperStart = QgsPoint()
                pt1HelperStart.setX(pt1.x())
                pt1HelperStart.setY(pt1.y())
            else:
                pt1HelperStart = RectangularPoint.point(pt1, pt2, 0, startOffset, invert)
            pt1HelperEnd = RectangularPoint.point(pt1, pt2, 0, startOffset+length, invert)
            
            # Punkte fuer pt2
            if startOffset == 0:
                pt2HelperStart = QgsPoint()
                pt2HelperStart.setX(pt2.x())
                pt2HelperStart.setY(pt2.y())
            else:
                pt2HelperStart = RectangularPoint.point(pt1, pt2, dist, startOffset, invert)
            pt2HelperEnd = RectangularPoint.point(pt1, pt2, dist, startOffset+length, invert)
            
            
            if pt1HelperStart == 0 or pt1HelperEnd == 0 or pt2HelperStart == 0 or pt2HelperEnd == 0:
                mc = self.canvas
                mc.unsetMapTool(self.tool)             
                return
            else:
                f = tools.utils.createHelpFeature( QgsGeometry.fromPolyline([pt1HelperStart, pt1HelperEnd]), 0, layer_id )
                tools.utils.addGeometryToDimensionLayer( f, "help" )
                
                f = tools.utils.createHelpFeature( QgsGeometry.fromPolyline([pt2HelperStart, pt2HelperEnd]), 0, layer_id )                
                tools.utils.addGeometryToDimensionLayer( f, "help")   
                
                self.canvas.refresh()
        
        
        # Hauptlinie berechnen
        # StartOffset wird beruecksichtigt, EndOffset ignoriert.
        if startOffset == 0 and length == 0:
            f = tools.utils.createMainFeature( QgsGeometry.fromPolyline([pt1, pt2]), 202, round(float(dist), 3) )
            tools.utils.addGeometryToDimensionLayer( f, "main" )
        
        else:
            ptMainStart = RectangularPoint.point(pt1, pt2, 0, startOffset + length - endOffset, invert)
            ptMainEnd = RectangularPoint.point(pt1, pt2, dist, startOffset + length - endOffset, invert)
            
            f = tools.utils.createMainFeature( QgsGeometry.fromPolyline([ptMainStart, ptMainEnd]), layer_id, round(float(dist), 3) )        
            tools.utils.addGeometryToDimensionLayer( f, "main" )
        
        self.p1 = pt1
        self.p2 = pt2
        
        
    def unsetTool(self):
        mc = self.canvas
        mc.unsetMapTool(self.tool)                  
        
        
    def deactivate(self):
        self.action_select2vertex.setChecked(False)      
       
        self.p1 = None
        self.p2 = None       


    def unload(self):
        print "unload plugin dimensioning"
        self.iface.removePluginMenu(self.action_select2vertex.tr("Dimensioning"), self.action_select2vertex)
        self.iface.removeToolBarIcon(self.action_select2vertex)
        
        self.iface.removePluginMenu(self.action_dimensioning.tr("Dimensioning"), self.action_dimensioning)        
        self.iface.removeToolBarIcon(self.action_dimensioning)
