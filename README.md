# <img class="filter-invertfilter" src="https://github.com/sducournau/consolidate_networks/blob/main/ressources/black_icon.png?raw=true" width="50" height="50"> Consolidate Networks


**A Qgis plugin toolset for consolidate your network data**<br>

*This plugin provides processing algorithms that allow you to manipulate the vertices of a line layer.
You can repair topological problems and clean your data.*



******

<br>

# 1. Preview :

![alt preview preview-1](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/comparaison_ban.png?raw=true)


<br>

# 2. Models
#### <ins>**CN | Self-repair Pipeline model**</ins>
`Apply multiple snappings steps and make the use of cn provider algorithms.`<br>


![alt model cn.sefl-repair](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/mode_blueprint_halfsize.png?raw=true)

<br>
<br>
    
******

# 3. List of cn provider algorithms' :

## Consolidate

#### <ins>**CalculateDbscan()**</ins>
`Calculate dbscan clusters of lines from a layer source.`<br>
##### Processing algorithm<br>
~~~~
cn.calculatedbscan
~~~~
##### Paramètres<br>
~~~~
{
'INPUT': QgsVectorLayer,    #vector layer source (line or polygon)
'POINTS_DBSCAN': 0.1,    #a decimal distance in meter between each point, eq to vertices density to do a dbscan (default: 0.1)
'DBSCAN*': False    #consider border points as noise (default: false)
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT    #vector layer computed (same type as input)
}
~~~~
![alt algorithm cn.calculatedbscan](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/CalculateDbscan.png?raw=true)
<br>
<br>
    
******

#### <ins>**ConsolidateWithDbscan()**</ins>
`Snap lines to each other splitting by their clusters from a layer source resulted from CalculateDbscan().`<br>
##### Processing algorithm :<br>
~~~~
cn.consolidatewithdbscan
~~~~
##### Paramètres<br>
~~~~
{
'INPUT': QgsVectorLayer,    #vector layer source (line or polygon)
'BUFFER_DBSCAN': 5.0,    #a decimal buffer radius (default: 5.0)
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT    #vector layer computed (same type as input)
}
~~~~
![alt algorithm cn.consolidatewithdbscan](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/CalculateDbscan2.png?raw=true)
<br>
<br>

******

#### <ins>**MakeIntersectionsVertexes()**</ins>
`Insert missing vertices from a source layer.`<br>
##### Processing algorithm :<br>
~~~~
cn.makeintersectionsvertexes
~~~~
##### Paramètres<br>
~~~~
{
'INPUT': QgsVectorLayer,    #vector layer source (line or polygon)
'BUFFER_REGION': 0.3,   #a decimal buffer radius (default: 0.3)
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT    #vector layer computed (same type as input)
}
~~~~
<br>
<br>


## Snapping layer (from himself)


#### <ins>**EndpointsStrimmingExtending()**</ins>
`Cut and extend end lines from a layer source.`<br>
##### Processing algorithm :<br>
~~~~
cn.endpointstrimmingextending
~~~~
##### Paramètres<br>
~~~~
{
'INPUT': QgsVectorLayer,    #vector layer source (line or polygon)
'BUFFER_TRIM_EXTEND': 4.0,    #a decimal buffer radius (default: 4.0)
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT    #vector layer computed (same type as input)
}
~~~~
![alt algorithm cn.endpointstrimmingextending](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/EndpointsStrimmingExtending.png?raw=true)
<br>
<br>
  
******

#### <ins>**EndpointsSnapping()**</ins>
`Snap lines endpoints' to each other's from a layer source.`<br>
##### Processing algorithm :<br>
~~~~
cn.endpointssnapping
~~~~
##### Paramètres<br>
~~~~
{
'INPUT': QgsVectorLayer,    #vector layer source (line or polygon)
'BUFFER_SNAPPING': 2.0,    #a decimal buffer radius (default: 2.0)
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT    #vector layer computed (same type as input)
}
~~~~
![alt algorithm cn.endpointssnapping](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/EndpointsSnapping.png?raw=true)
<br>
<br>


******

#### <ins>**HubSnapping()**</ins>
`Align lines vertices' hubs on top of each other within a buffer.`<br>
##### Processing algorithm :<br>
~~~~
cn.hubsnapping
~~~~
##### Paramètres<br>
~~~~
{
'INPUT': QgsVectorLayer,    #vector layer source (line or polygon)
'BUFFER_REGION': 1.0,    #a decimal buffer radius (default: 1.0)
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT    #vector layer computed (same type as input)
}
~~~~
![alt algorithm cn.hubsnapping](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/HubSnapping.png?raw=true)
<br>
<br>




## Snapping layer (from another layer)


#### <ins>**SnapEndpointsToLayer()**</ins>
`Snap lines endpoints' to each other's from an other layer source.`<br>
##### Processing algorithm :<br>
~~~~
cn.snapendpointstoLayer
~~~~
##### Paramètres<br>
~~~~
{
'INPUT': QgsVectorLayer,    #vector layer source (line or polygon)
'REF_INPUT': QgsVectorLayer,    #vector layer source (point prefered)
'BUFFER_SNAPPING': 2.0,    #a decimal buffer radius (default: 2.0)
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT    #vector layer computed (same type as input)
}
~~~~
<br>
<br>

******


#### <ins>**SnapHubsPointsToLayer()**</ins>
`Align lines vertices' hubs on top of a point layer within a buffer`<br>
##### Processing algorithm :<br>
~~~~
cn.snaphubspointstolayer
~~~~
##### Paramètres<br>
~~~~
{
'INPUT': QgsVectorLayer,    #vector layer source (line or polygon)
'REF_INPUT': QgsVectorLayer,    #vector layer source (point prefered)
'BUFFER_REGION': 2.0,    #a decimal buffer radius (default: 2.0)
'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT    #vector layer computed (same type as input)
}
~~~~
<br>
<br>  
