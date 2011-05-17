# -*- coding: latin1 -*-
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math

def addGeometryToDimensionLayer(feat, type):
        
    if feat.geometry().type() != 1:
        return
        
    if type == "main":
        layerName = "Dimension main lines"
        tableName = "lines_main"
    else:
        layerName = "Dimension help lines"
        tableName = "lines_help"

    if getLayerByName(layerName) == None:
        
        uri = QgsDataSourceURI()
        uri.setDatabase(QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/dimensioning/sqlite/dimension.sqlite'))) 
        uri.setDataSource('', tableName, 'geometry')       
        
        vl = QgsVectorLayer(uri.uri(), layerName, 'spatialite')
        
        qml = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/dimensioning/styles/default_' + type + '.qml'))
        vl.loadNamedStyle(qml)        
        
        pr = vl.dataProvider()
        pr.addFeatures([feat])
        vl.updateExtents()
        QgsMapLayerRegistry().instance().addMapLayer(vl, True)
    else:
        layer = getLayerByName(layerName) 
        pr = layer.dataProvider()
        pr.addFeatures([feat])
        layer.updateExtents()


def getLayerByName(layername):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.name() == layername:
            if layer.isValid():
                return layer
            else:
                return None        


def createHelpFeature(geom, main_from, layer_id):
        feat = QgsFeature()
        feat.setGeometry(geom)
        feat.setAttributeMap({ 1 : QVariant(main_from),  2 : QVariant(layer_id)})
        
        return feat


def createMainFeature(geom, layer_id, length):
        feat = QgsFeature()
        feat.setGeometry(geom)
        feat.setAttributeMap({ 1 : QVariant(layer_id),  2 : QVariant(length)})
        
        return feat
           
