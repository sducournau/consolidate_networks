# -*- coding: utf-8 -*-

"""
/***************************************************************************

                                 Convert Json To TKI


                              -------------------
        begin                : 2021-11-15
        copyright            : (C) 2021 by a
        email                : a
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
import os
from os import listdir
from os.path import isfile, join
from qgis.utils import iface
from qgis.PyQt.QtCore import QCoreApplication, QVariant
from qgis.core import (QgsProject,
                       QgsProcessing,
                       QgsFeatureSink,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsFeatureRequest,
                       QgsProcessingParameterFeatureSink,
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFolderDestination,
                       QgsProcessingOutputMultipleLayers,
                       QgsProcessingContext,
                       QgsProcessingOutputNumber,
                       QgsFeature,
                       QgsField,
                       QgsFields,
                       edit,
                       QgsProcessingParameterVectorLayer,
                       QgsExpression)
from qgis import processing
import math
import json

class UpdateJson(QgsProcessingAlgorithm):
    """
    This is an example algorithm that takes a vector layer and
    creates a new identical one.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the QgsProcessingAlgorithm
    class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.
    INPUT = 'INPUT'
    OUTPUT = 'OUTPUT'


    def tr(self, string):
        """
        Returns a translatable string with the self.tr() function.
        """
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return UpdateJson()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'updatejson'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Update your Json data')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('Tki')

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'tki'

    def shortHelpString(self):
        """
        Returns a localised short helper string for the algorithm. This string
        should provide a basic description about what the algorithm does and the
        parameters and outputs associated with it..
        """
        return self.tr("Update your Json data")

    def initAlgorithm(self, config=None):
        """
        Here we define the inputs and output of the algorithm, along
        with some other properties.
        """
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.INPUT,
                self.tr('INPUT'),
                [QgsProcessing.TypeVectorLine]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('OUTPUT')
            )
        )




    def iterateOverChild(self, data, parameters, context, feedback):


        feats = []

        if data['Type'] == 'Single Duct':

            for child in data['Children']:
                feats.append(self.iterateOverChild(child, parameters, context, feedback))



            if 'MAX_DUCTS' not in data:
                data['MAX_DUCTS'] = 0


            data['Children'] = feats



        elif data['Type'] == 'Virtual Duct':

            if 'MAX_DUCTS' not in data:
                data['MAX_DUCTS'] = 0


            data['Children'] = feats

        elif data['Type'] == 'Multiduct':

            for child in data['Children']:
                feats.append(self.iterateOverChild(child, parameters, context, feedback))


            if 'MAX_CABLE' not in data:
                data['MAX_CABLE'] = len([subchild for subchild in data['Children'] if not subchild['Occupied']])
            if 'MAX_DUCTS' not in data:
                data['MAX_DUCTS'] = 0

            data['Children'] = feats


        elif data['Type'] == 'Pipe':
            pass

        elif data['Type'] == 'Cable Blocks':

            for child in data['Children']:
                feats.append(self.iterateOverChild(child, parameters, context, feedback))



            if 'MAX_DUCTS' not in data:
                data['MAX_DUCTS'] = 1 if not data['Occupied'] else 0


            data['Children'] = feats


        return data


    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        self.field_id = 'fid'
        self.source = self.parameterAsVectorLayer(parameters, self.INPUT, context)



        (sink_output, dest_output) = self.parameterAsSink(parameters, self.OUTPUT,
                context, self.source.fields(), self.source.wkbType(), self.source.sourceCrs())

        #print(source.featureCount())
        for y, feature in enumerate(self.source.getFeatures()):

            data = json.loads(feature['JSON'])
            updated_features = []

            for child in data['Graben']['Children']:
                updated_features.append(self.iterateOverChild(child, parameters, context, feedback))


            data['Graben']['Children'] = updated_features
            feature['JSON'] = json.dumps(data)
            sink_output.addFeature(feature, QgsFeatureSink.FastInsert)





        return {'OUTPUT': self.OUTPUT}
