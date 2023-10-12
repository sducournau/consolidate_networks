# -*- coding: utf-8 -*-

"""
/***************************************************************************
 ConsolidateNetwork
                                 A QGIS plugin
 A toolset for consolidate your network data
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2021-11-15
        copyright            : (C) 2021 by Simon Ducournau
        email                : simon.ducournau@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Simon Ducournau'
__date__ = '2021-11-15'
__copyright__ = '(C) 2021 by Simon Ducournau'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

from qgis.core import QgsProcessingProvider
from .consolidate_networks_algorithms import *
from qgis.PyQt.QtGui import QIcon
import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile

class ConsolidateNetworksProvider(QgsProcessingProvider):

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
        Loads all algorithms belonging to this provider.
        """
        self.addAlgorithm(CalculateDbscan())
        self.addAlgorithm(ConsolidateWithDbscan())
        self.addAlgorithm(EndpointsStrimmingExtending())
        self.addAlgorithm(EndpointsSnapping())
        self.addAlgorithm(HubSnapping())
        self.addAlgorithm(SnapHubsPointsToLayer())
        self.addAlgorithm(MakeIntersectionsVertexes())
        self.addAlgorithm(SnapEndpointsToLayer())

        # add additional algorithms here
        # self.addAlgorithm(MyOtherAlgorithm())s

    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'cn'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('Consolidate Networks')

    def icon(self):
        """
        Should return a QIcon which is used for your provider inside
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
