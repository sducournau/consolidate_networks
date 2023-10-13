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

class ConvertJsonToTKI(QgsProcessingAlgorithm):
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
        return ConvertJsonToTKI()

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'convertjsontotki'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr('Convert your Json data to TKI input')

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr('TKI')

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
        return self.tr("Convert your Json data to TKI input")

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

    def runArrayOffsetLines(self, parameters, context, feedback, feature, count):
        outputs = {}

        layer = self.source.materialize(QgsFeatureRequest().setFilterFids([feature.id()]))
        #print(layer.featureCount())
        print(count)

        alg_params_arrayoffsetlines_left = {
            'COUNT': math.floor(count/2) if count%2 == 1 else count/2,
            'INPUT': layer,
            'JOIN_STYLE': 1,
            'MITER_LIMIT': 2,
            'OFFSET': 0.05,
            'SEGMENTS': 8,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        outputs['alg_params_arrayoffsetlines_left'] = processing.run('qgis:arrayoffsetlines', alg_params_arrayoffsetlines_left, context=context, feedback=feedback)


        alg_params_arrayoffsetlines_right = {
            'COUNT': math.ceil(count/2) if count%2 == 1 else count/2,
            'INPUT': layer,
            'JOIN_STYLE': 1,
            'MITER_LIMIT': 2,
            'OFFSET': -0.05,
            'SEGMENTS': 8,
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }
        outputs['alg_params_arrayoffsetlines_right'] = processing.run('qgis:arrayoffsetlines', alg_params_arrayoffsetlines_right, context=context, feedback=feedback)
        with edit(outputs['alg_params_arrayoffsetlines_right']['OUTPUT']):
            outputs['alg_params_arrayoffsetlines_right']['OUTPUT'].deleteFeature(1)
            outputs['alg_params_arrayoffsetlines_right']['OUTPUT'].deleteFeature(outputs['alg_params_arrayoffsetlines_right']['OUTPUT'].featureCount()+1)
        #print([feat.id() for feat in outputs['alg_params_arrayoffsetlines']['OUTPUT'].getFeatures()])

        alg_params_merge = {
            'LAYERS': [outputs['alg_params_arrayoffsetlines_left']['OUTPUT'],outputs['alg_params_arrayoffsetlines_right']['OUTPUT']],
            'CRS': self.source.sourceCrs(),
            'OUTPUT': 'TEMPORARY_OUTPUT'
        }

        outputs['alg_params_merge'] = processing.run("qgis:mergevectorlayers", alg_params_merge)



        return outputs['alg_params_merge']['OUTPUT']


    def iterateOverChild(self, data, parameters, context, feedback):

        features_to_create = []
        feats = []

        if 'Type' in data:
            if data['Type'] == 'Single Duct':

                for child in data['Children']:
                    feats += self.iterateOverChild(child, parameters, context, feedback)



                if data['MAX_DUCTS'] != 0:

                    features_to_create += [{'Rohr-Typ':data['Bezeichnung'],'MAX_DUCTS':data['MAX_DUCTS'],'Type':data['Type'], 'Netzebene':data['Netzebene']}]
                    features_to_create += feats



            elif data['Type'] == 'Virtual Duct':

                for child in data['Children']:
                    feats += self.iterateOverChild(child, parameters, context, feedback)



                if data['MAX_DUCTS'] != 0:

                    features_to_create += [{'Rohr-Typ':data['Bezeichnung'],'MAX_DUCTS':data['MAX_DUCTS'],'Type':data['Type'], 'Netzebene':data['Netzebene']}]
                    features_to_create += feats

            elif data['Type'] == 'Multiduct':

                for child in data['Children']:
                     feats += self.iterateOverChild(child, parameters, context, feedback)


                if  not data['Occupied'] or (data['Occupied'] and len([feat for feat in feats if feat['Occupied']]) < len([feat for feat in feats])):
                    features_to_create  += [{'Rohr-Typ':data['Bezeichnung'],'MAX_DUCTS':data['MAX_DUCTS'], 'MAX_CABLE':len([subchild for subchild in data['Children'] if not subchild['Occupied']]),'Type':data['Type'], 'Netzebene':data['Netzebene']}]
                    features_to_create += feats


            elif data['Type'] == 'Pipe':
                pass

            elif data['Type'] == 'Cable Blocks':
                for child in data['Children']:
                    feats += self.iterateOverChild(child, parameters, context, feedback)



                if data['MAX_DUCTS'] != 0:

                    features_to_create += [{'Rohr-Typ':data['Bezeichnung'],'MAX_DUCTS':data['MAX_DUCTS'],'Type':data['Type'], 'Netzebene':data['Netzebene']}]
                    features_to_create += feats


        return features_to_create


    def processAlgorithm(self, parameters, context, feedback):
        """
        Here is where the processing itself takes place.
        """

        # Retrieve the feature source and sink. The 'dest_id' variable is used
        # to uniquely identify the feature sink, and must be included in the
        # dictionary returned by the processAlgorithm function.
        self.field_id = 'fid'
        self.source = self.parameterAsVectorLayer(parameters, self.INPUT, context)
        new_fields = QgsFields()
        new_fields.append(QgsField('id', QVariant.Int))
        new_fields.append(QgsField('MAX_DUCTS', QVariant.Int))
        new_fields.append(QgsField('MAX_CABLE', QVariant.Int))
        new_fields.append(QgsField('Rohr-Typ', QVariant.String))
        new_fields.append(QgsField('Netzebene', QVariant.String))
        new_fields.append(QgsField('RohrTyp-Be', QVariant.String))

        outputs = {}


        (sink_output, dest_output) = self.parameterAsSink(parameters, self.OUTPUT,
                context, new_fields, self.source.wkbType(), self.source.sourceCrs())

        #print(source.featureCount())
        for y, feature in enumerate(self.source.getFeatures()):

            data = json.loads(feature['JSON'])
            features_to_create = []

            for child in data['Graben']['Children']:
                features_to_create += self.iterateOverChild(child, parameters, context, feedback)

            if len(features_to_create) == 1:
                output_feature = QgsFeature(new_fields)
                output_feature['Rohr-Typ'] = features_to_create[0]['Rohr-Typ']
                output_feature['MAX_DUCTS'] = features_to_create[0]['MAX_DUCTS']
                if 'MAX_CABLE' in features_to_create[0]:
                    output_feature['MAX_CABLE'] = features_to_create[0]['MAX_CABLE']
                output_feature.setGeometry(feature.geometry())
                sink_output.addFeature(output_feature, QgsFeatureSink.FastInsert)

            elif len(features_to_create) > 1:




                new_features = self.runArrayOffsetLines(parameters, context, feedback, feature, len(features_to_create))
                #print(y,new_features.featureCount())
                #print(len(features_to_create),new_features.featureCount())
                for i, feat in enumerate(new_features.getFeatures()):
                    output_feature = QgsFeature(new_fields)
                    output_feature['Rohr-Typ'] = features_to_create[i]['Rohr-Typ']
                    output_feature['MAX_DUCTS'] = features_to_create[i]['MAX_DUCTS']
                    output_feature['Netzebene'] = features_to_create[i]['Netzebene']
                    if 'MAX_CABLE' in features_to_create[i]:
                        output_feature['MAX_CABLE'] = features_to_create[i]['MAX_CABLE']
                    output_feature.setGeometry(feat.geometry())
                    sink_output.addFeature(output_feature, QgsFeatureSink.FastInsert)




        return {'OUTPUT': self.OUTPUT}
