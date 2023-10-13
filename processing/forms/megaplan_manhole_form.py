from qgis.PyQt import QtGui, QtWidgets, QtCore
from qgis.PyQt.QtWidgets import QWidget, QPlainTextEdit, QPushButton,QTextEdit,QFileDialog, QLineEdit, QLabel
from  qgis.gui import QgsFileWidget, QgsExternalResourceWidget
import json
from functools import partial
import re
import webbrowser
import sys
from qgis.utils import iface
from PIL import ImageGrab
import os
import subprocess
from qgis.core import *


layer = iface.activeLayer()
project_folder = QgsExpressionContextUtils.layerScope(layer).variable('project_folder')
photos_folder = QgsExpressionContextUtils.layerScope(layer).variable('photos_folder')



def take_screenshot(layer, photo_path, feature):


    geom = feature.geometry()

    name = str(geom.asWkt())
    os.system('SnippingTool.exe')




    im = ImageGrab.grabclipboard()
    im.save(photos_folder + os.sep + name + '.png','PNG')
    photo_path.setDocumentPath(photos_folder + os.sep + name + '.png')


    #pixmap  = QtGui.QPixmap(data_dir + os.sep + str(int(self.feature['id'])) + '.png')
    #self.image.setPixmap(pixmap)

    iface.messageBar().pushMessage("Success",'File writed', level=Qgis.Success)




def init_form(dialog, layer, feature):




    dialog.showButtonBox()

    #dialog.disconnectButtonBox()



    photo_path = dialog.findChild(QgsExternalResourceWidget , "PHOTO")

    #control_image = dialog.findChild(QWidget, "pushButton_photo")
    print(feature.id())

    label = QLabel('Screenshot')
    photo = QPushButton('Take Screenshot')


    try:
        if feature.id() > -9000000:
            photo_data =  feature['PHOTO']
        else:
            photo_data =  ''
    except:
        photo_data =  ''

    photo_path.setDocumentPath(photo_data)



    dialog.layout().addWidget(photo)



    photo.clicked.connect(lambda: take_screenshot(layer, photo_path, feature))
