# -*- coding: latin1 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from ui_dimensioning import Ui_Dimensioning

class DimensioningGui(QDialog, QObject, Ui_Dimensioning):
    
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.settings = QSettings("CatAIS","dimensioning")
        self.layerid = self.settings.value("gui/layerid", 0)        
    
    def initGui(self):
        self.sboxStartOffset.setMaximum(10000000)
        self.sboxStartOffset.setMinimum(-10000000)
        self.sboxStartOffset.setDecimals(3)
        
        self.sboxEndOffset.setMaximum(10000000)
        self.sboxEndOffset.setMinimum(-10000000)
        self.sboxEndOffset.setDecimals(3)       
       
        self.sboxLength.setMaximum(10000000)
        self.sboxLength.setMinimum(0)
        self.sboxLength.setDecimals(3)       

        self.sboxLayerId.setMaximum(10000000)
        self.sboxLayerId.setMinimum(0)
        self.sboxLayerId.setProperty("value", self.layerid)
        
    @pyqtSignature("on_btnAdd_clicked()")    
    def on_btnAdd_clicked(self):
        self.emit(SIGNAL("dimensioningOffsets(double, double, double, int, bool)"), self.sboxLength.value(), self.sboxStartOffset.value(),  self.sboxEndOffset.value(), self.sboxLayerId.value(),  self.chckBoxInvert.isChecked())        
        self.settings.setValue("gui/layerid", QVariant( self.sboxLayerId.value() ) )             
#        self.close()
        
    @pyqtSignature("on_btnCancel_clicked()")    
    def on_btnCancel_clicked(self): 
        self.emit(SIGNAL("closeDimensioningGui()"))   
        self.emit(SIGNAL("unsetTool()"))   
        self.close()
