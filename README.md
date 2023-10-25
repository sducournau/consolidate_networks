# ![alt title logo](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/logo_black.png?raw=true) Consolidate Networks

**Consolidate Networks is a Qgis plugin toolset that helps you optimize the geometry of your line network.**
<br>
*This plugin provides processing algorithms that allow you to manipulate the vertices of a line layer.
You can repair topological problems and clean your data.*

Github repository : [https://sducournau.github.io/consolidate_networks/](https://github.com/sducournau/consolidate_networks)
<br>
Qgis plugin repository : [https://plugins.qgis.org/plugins/consolidate_networks/](https://plugins.qgis.org/plugins/consolidate_networks/)

******

<br>

# 1. Preview

![alt preview preview-1](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/comparaison_ban.png?raw=true)


<br>

# 2. Models
#### <ins>**CN | Self-repair Pipeline model**</ins>
`Apply multiple snappings steps and make the use of cn provider algorithms.`<br>


![alt model cn.sefl-repair](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/mode_blueprint.png?raw=true)

<br>
<br>
    
******

# 3. List of CN provider algorithms

![alt preview cover](https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/cover_50.png?raw=true)


## DBscan and consolidate

#### <ins>**CalculateDbscan()**</ins>
`Calculate dbscan clusters of lines from a layer source.`<br>
##### Processing algorithm<br>
~~~~
cn.calculatedbscan
~~~~
##### Paramètres<br>
~~~~
{
    "INPUT": QgsVectorLayer,                            # vector layer source (TypeVectorLine)
    "FIX_GEOMETRIES_BEFORE_PROCESSING": true,           # repairs the input layer geometries at the start of processing
    "POINTS_DBSCAN_THRESHOLD_DISTANCE": 0.1,            # a decimal distance in meter between each point, eq to vertices density to do a dbscan
    "DBSCAN*": false,                                   # consider border points as noise
    "PRINT_DEBUG": false,                               # activates debug mode (print readable in the console)
    "OUTPUT": "TEMPORARY_OUTPUT"                        # vector layer computed (TypeVectorLine)
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
    "INPUT": QgsVectorLayer,                            # vector layer source (TypeVectorLine)
    "FIX_GEOMETRIES_BEFORE_PROCESSING": true,           # repairs the input layer geometries at the start of processing
    "BUFFER_DBSCAN": 5.0,                               # a decimal buffer radius to snap groups between them
    "PRINT_DEBUG": false,                               # activates debug mode (print readable in the console)
    "OUTPUT": "TEMPORARY_OUTPUT"                        # vector layer computed (TypeVectorLine)
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
    "INPUT": QgsVectorLayer,                            # vector layer source (TypeVectorLine)
    "FIX_GEOMETRIES_BEFORE_PROCESSING": true,           # repairs the input layer geometries at the start of processing
    "ENTITY_IDENTIFICATION_FIELDS": [],                 # vector layer source fields to brings decomposed entities together, by default all fields are selected
    "PRINT_DEBUG": false,                               # activates debug mode (print readable in the console)
    "OUTPUT": "TEMPORARY_OUTPUT"                        # vector layer computed (TypeVectorLine)
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
    "INPUT": QgsVectorLayer,                            # vector layer source (TypeVectorLine)
    "FIX_GEOMETRIES_BEFORE_PROCESSING": true,           # repairs the input layer geometries at the start of processing
    "BUFFER_TRIM": 3.0,                                 # maximum segment reduction distance
    "BUFFER_EXTEND": 5.0,                               # maximum segment extension distance
    "PREFERRED_BEHAVIOR_FOR_STARTING_EXTREMITIES": 1,   # prefered behaviour for startings enpoints : 'Trim','Extend','None'
    "PREFERRED_BEHAVIOR_FOR_ENDING_EXTREMITIES": 0,     # prefered behaviour for endings enpoints : 'Trim','Extend','None'
    "HAUSDORFF_DISTANCE_LIMIT": 5.0,                    # hausdorff distance limit to avoid calculations between geometries too similar
    "ANGULAR_LIMIT_OF_PARALLEL_GEOMETRIES": 15.0,       # angular limit difference between two geometries
    "EXPLODE_AND_GATHER": false,                        # decomposes each entity into segments composed of two points at the start of processing, then brings them together at the end of processing
    "ENTITY_IDENTIFICATION_FIELDS": [],                 # vector layer source fields to brings decomposed entities together, by default all fields are selected
    "PRINT_DEBUG": false,                               # activates debug mode (print readable in the console)
    "OUTPUT": "TEMPORARY_OUTPUT"                        # vector layer computed (TypeVectorLine)
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
    "INPUT": QgsVectorLayer,                            # vector layer source (TypeVectorLine)
    "FIX_GEOMETRIES_BEFORE_PROCESSING": true,           # repairs the input layer geometries at the start of processing
    "BUFFER_ENDPOINTS_SNAPPING": 5.0,                   # maximum snapping distance
    "PREFERRED_BEHAVIOR_FOR_STARTING_EXTREMITIES": 1,   # prefered behaviour for startings enpoints : 
                                                        # 'Nearest, Minimum angular variation','Farest, Minimum angular variation',
                                                        # 'Nearest, Maximum angular variation','Farest, Maximum angular variation'
    "PREFERRED_BEHAVIOR_FOR_ENDING_EXTREMITIES": 0,     # prefered behaviour for endings enpoints :
                                                        # 'Nearest, Minimum angular variation','Farest, Minimum angular variation',
                                                        # 'Nearest, Maximum angular variation','Farest, Maximum angular variation'
    "HAUSDORFF_DISTANCE_LIMIT": 5.0,                    # hausdorff distance limit to avoid calculations between geometries too similar
    "MIN_ANGULAR_LIMIT_OF_PARALLEL_GEOMETRIES": 0.0,    # minimum angular limit difference between two geometries
    "MAX_ANGULAR_LIMIT_OF_PARALLEL_GEOMETRIES": 180.0,  # mximum angular limit difference between two geometries
    "PREFERS_SAME_GEOMETRY_DIRECTION": true,            # favors entities whose geometry has the same direction
    "EXPLODE_AND_GATHER": false,                        # decomposes each entity into segments composed of two points at the start of processing, then brings them together at the end of processing
    "ENTITY_IDENTIFICATION_FIELDS": [],                 # vector layer source fields to brings decomposed entities together, by default all fields are selected
    "PRINT_DEBUG": false,                               # activates debug mode (print readable in the console)
    "OUTPUT": "TEMPORARY_OUTPUT"                        # vector layer computed (TypeVectorLine)
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
    "INPUT": QgsVectorLayer,                            # vector layer source (TypeVectorLine)
    "FIX_GEOMETRIES_BEFORE_PROCESSING": true,           # repairs the input layer geometries at the start of processing
    "BUFFER_HUB_SNAPPING": 1.5,                         # maximum hub distance between entities
    "HUBPOINT_MUST_BE_AN_EXISTING_VERTEX": true,        # the hub snap point is the closest vertex to the barycenter of the resulting polygon, otherwise it is the barycenter
    "EXPLODE_AND_GATHER": false,                        # decomposes each entity into segments composed of two points at the start of processing, then brings them together at the end of processing
    "ENTITY_IDENTIFICATION_FIELDS": [],                 # vector layer source fields to brings decomposed entities together, by default all fields are selected
    "PRINT_DEBUG": false,                               # activates debug mode (print readable in the console)
    "OUTPUT": "TEMPORARY_OUTPUT"                        # vector layer computed (TypeVectorLine)
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
    "INPUT": QgsVectorLayer,                            # vector layer source (TypeVectorLine)
    "REF_INPUT": QgsVectorLayer,                        # reference vector layer source (TypeVectorLine, TypeVectorPoint)
    "FIX_GEOMETRIES_BEFORE_PROCESSING": true,           # repairs the input layer geometries at the start of processing
    "BUFFER_ENDPOINTS_SNAPPING": 5.0,                   # maximum snapping distance
    "PREFERRED_BEHAVIOR_FOR_STARTING_EXTREMITIES": 1,   # prefered behaviour for startings enpoints : 
                                                        # 'Nearest, Minimum angular variation','Farest, Minimum angular variation',
                                                        # 'Nearest, Maximum angular variation','Farest, Maximum angular variation'
    "PREFERRED_BEHAVIOR_FOR_ENDING_EXTREMITIES": 0,     # prefered behaviour for endings enpoints :
                                                        # 'Nearest, Minimum angular variation','Farest, Minimum angular variation',
                                                        # 'Nearest, Maximum angular variation','Farest, Maximum angular variation'
    "HAUSDORFF_DISTANCE_LIMIT": 5.0,                    # hausdorff distance limit to avoid calculations between geometries too similar
    "MIN_ANGULAR_LIMIT_OF_PARALLEL_GEOMETRIES": 0.0,    # minimum angular limit difference between two geometries
    "MAX_ANGULAR_LIMIT_OF_PARALLEL_GEOMETRIES": 180.0,  # mximum angular limit difference between two geometries
    "PREFERS_SAME_GEOMETRY_DIRECTION": true,            # favors entities whose geometry has the same direction
    "EXPLODE_AND_GATHER": false,                        # decomposes each entity into segments composed of two points at the start of processing, then brings them together at the end of processing
    "ENTITY_IDENTIFICATION_FIELDS": [],                 # vector layer source fields to brings decomposed entities together, by default all fields are selected
    "PRINT_DEBUG": false,                               # activates debug mode (print readable in the console)
    "OUTPUT": "TEMPORARY_OUTPUT"                        # vector layer computed (TypeVectorLine)
}
~~~~
<br>
<br>

******


#### <ins>**SnapHubsPointsToLayer()**</ins>
`Align lines vertices' hubs on top of a point layer within a buffer.`<br>
##### Processing algorithm :<br>
~~~~
cn.snaphubspointstolayer
~~~~
##### Paramètres<br>
~~~~
{
    "INPUT": QgsVectorLayer,                            # vector layer source (TypeVectorLine)
    "REF_INPUT": QgsVectorLayer,                        # reference vector layer source (TypeVectorLine, TypeVectorPoint)
    "FIX_GEOMETRIES_BEFORE_PROCESSING": true,           # repairs the input layer geometries at the start of processing
    "BUFFER_HUB_SNAPPING": 1.5,                         # maximum hub distance between entities
    "HUBPOINT_MUST_BE_AN_EXISTING_VERTEX": true,        # the hub snap point is the closest vertex to the barycenter of the resulting polygon, otherwise it is the barycenter
    "EXPLODE_AND_GATHER": false,                        # decomposes each entity into segments composed of two points at the start of processing, then brings them together at the end of processing
    "ENTITY_IDENTIFICATION_FIELDS": [],                 # vector layer source fields to brings decomposed entities together, by default all fields are selected
    "PRINT_DEBUG": false,                               # activates debug mode (print readable in the console)
    "OUTPUT": "TEMPORARY_OUTPUT"                        # vector layer computed (TypeVectorLine)
}
~~~~
<br>
<br>  
