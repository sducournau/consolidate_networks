from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *
from shutil import copyfile
import os
from os import listdir
from os.path import isfile, join
import processing

PROJECT = QgsProject.instance()

class TkiTask(QgsTask):
    """A qgis task running in background for creating the folder structure and the geopackage database"""

    def __init__(self, description, dockwidget, action):

        QgsTask.__init__(self, description,QgsTask.CanCancel)

        self.exception = None
        self.dockwidget = dockwidget
        self.action = action
        self.styles_dir = os.path.dirname(__file__) + os.sep + 'styles'
        self.data_dir = os.path.dirname(__file__) + os.sep + 'data'




    def run(self):

        """We get the different parameters"""
        output = {}
        name = str(self.dockwidget.lineEdit_layer_name.text())
        crs = self.dockwidget.mQgsProjectionSelectionWidget.crs().authid()
        root_folder = self.dockwidget.mQgsFileWidget.filePath()

        """Here we create the folder structure"""
        try:
            os.makedirs(root_folder + os.sep + 'MEGAPLAN', exist_ok = True)
            os.makedirs(root_folder + os.sep + 'MEGAPLAN' + os.sep + 'PHOTOS' + os.sep + name + os.sep + 'DUCTS', exist_ok = True)
            os.makedirs(root_folder + os.sep + 'MEGAPLAN' + os.sep + 'PHOTOS' + os.sep + name + os.sep + 'MANHOLE', exist_ok = True)
        except:
            pass


        """Copy the default data.json and the Rohrdimensionen.xlsm in the project root folder"""
        onlyfiles = [f for f in listdir(self.data_dir) if isfile(join(self.data_dir, f))]
        for file in onlyfiles:
            filepath = self.data_dir + os.sep + file
            copyfile(filepath, root_folder + os.sep + 'MEGAPLAN' + os.sep + file)


        """Creation of the ducts layer"""
        layer_lines =  QgsVectorLayer("LineString?crs={crs}&field=fid:integer(10,0)&field=JSON:string(65535,0)&field=PHOTO:string(5000,0)&index=yes".format(crs=crs),"DUCTS","memory")
        layer_lines.loadNamedStyle(self.styles_dir  + os.sep +  'ducts.qml')

        """We pass the project root folder and the photo folder as variables of the ducts layer"""
        QgsExpressionContextUtils.setLayerVariable(layer_lines,'project_folder', r''+root_folder + os.sep + 'MEGAPLAN')
        QgsExpressionContextUtils.setLayerVariable(layer_lines,'photos_folder', r''+root_folder + os.sep + 'MEGAPLAN'+ os.sep + 'PHOTOS'+ os.sep + name + os.sep + 'DUCTS')


        """Creation of the manhole layer"""
        layer_points =  QgsVectorLayer("Point?crs={crs}&field=fid:integer(10,0)&field=PHOTO:string(5000,0)&index=yes".format(crs=crs),"MANHOLE","memory")
        layer_points.loadNamedStyle(self.styles_dir  + os.sep +  'manhole.qml')

        """We pass the project root folder and the photo folder as variables of the manhole layer"""
        QgsExpressionContextUtils.setLayerVariable(layer_points,'project_folder', r''+root_folder + os.sep + 'MEGAPLAN')
        QgsExpressionContextUtils.setLayerVariable(layer_points,'photos_folder', r''+root_folder + os.sep + 'MEGAPLAN'+ os.sep + 'PHOTOS'+ os.sep + name + os.sep + 'MANHOLE')


        """We export the two memory layers in a same geopackage database in the project root folder"""
        alg_parameters_export = {
            'LAYERS': [layer_lines, layer_points],
            'OVERWRITE':True,
            'SAVE_STYLES':True,
            'OUTPUT':root_folder + os.sep + 'MEGAPLAN' + os.sep +  '{name}.{format}'.format(name=name,format='gpkg')

            }

        output = processing.run("qgis:package", alg_parameters_export)


        return True
