from qgis.core import QgsProcessingProvider
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsApplication
import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile

class TkiAlgorithmProvider(QgsProcessingProvider):

    def __init__(self):
        """
        Default constructor.
        """
        QgsProcessingProvider.__init__(self)
        self.DIR_PLUGIN = os.path.normpath(os.path.dirname(__file__))
        user_directory = QgsApplication.qgisSettingsDirPath()
        model_directory = user_directory + os.sep + 'processing' +os.sep + 'models'

        onlyfiles = [f for f in listdir(self.DIR_PLUGIN + os.sep + 'models') if isfile(join(self.DIR_PLUGIN + os.sep + 'models', f)) if f.split('.')[-1] == 'model3']
        for file in onlyfiles:
            filepath = self.DIR_PLUGIN + os.sep + 'models' + os.sep + file
            copyfile(filepath, model_directory  + os.sep + file)



    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass


    def loadAlgorithms(self):
        """

        """
        pass

    def id(self):
        """Used for identifying the provider.
        This string should be a unique, short, character only string,
        eg "qgis" or "gdal". This string should not be localised.
        """
        return 'consolidate_networks'

    def name(self):
        """
        This string should be as short as possible (e.g. "Lastools", not
        "Lastools version 1.0.1 64-bit") and localised.
        """
        return self.tr('Consolidate Networks')

    def icon(self):
        """Should return a QIcon which is used for your provider inside
        the Processing toolbox.
        """
        icon = QIcon(self.DIR_PLUGIN + os.sep + "icon.png")
        return icon

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()
