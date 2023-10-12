# <img src="https://github.com/sducournau/consolidate_networks/blob/main/icon.png?raw=true" width="50" height="50"> Consolidate Networks

**A Qgis plugin toolset for consolidate your network data**


*This plugin provides processing algorithms that allow you to manipulate the vertices of a line layer.
You can repair topological problems and clean your data.*

******

<br>

# Preview :

<img src="https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/comparaison_ban.png?raw=true">




# List of cn provider algorithms' :

## 1. Consolidate
 
### *<ins>CalculateDbscan()*</ins>
`Processing algorithm`<br>
`Calculate dbscan clusters of lines from a layer source.`<br>
`Algorithm name : cn.calculatedbscan`<br>
~~~~
INPUT : vector layer source (line or polygon)
POINTS_DBSCAN : a decimal distance in meter between each point, eq to vertices density to do a dbscan (default: 0,1)
DBSCAN* : consider border points as noise (default: false)
OUTPUT : vector layer computed (same type as input)
~~~~
<br>
<img src="https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/CalculateDbscan.png?raw=true">
<br>
<br>
<br>

******

### **<ins>ConsolidateWithDbscan()**</ins>
`Processing algorithm`<br>
`Snap lines to each other splitting by their clusters from a layer source resulted from CalculateDbscan().`<br>
`Algorithm name : cn.consolidatewithdbscan`<br>
~~~~
INPUT : vector layer source (line or polygon)
BUFFER_DBSCAN : a decimal buffer radius (default: 5,0)
OUTPUT : vector layer computed (same type as input)
~~~~
<br>
<img src="https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/CalculateDbscan2.png?raw=true">
<br>
<br>
<br>

******

### **<ins>MakeIntersectionsVertexes()**</ins>
`Processing algorithm`<br>
`Insert missing vertices from a source layer.`<br>
`Algorithm name : cn.makeintersectionsvertexes`<br>
~~~~
INPUT : vector layer source (line or polygon)
BUFFER_REGION : a decimal buffer radius (default: 0,3)
OUTPUT : vector layer computed (same type as input)
~~~~
<br>
<br>
<br>



## 2. Snapping layer (from himself)

### **<ins>EndpointsStrimmingExtending()**</ins>
`Processing algorithm`<br>
`Cut and extend end lines from a layer source.`<br>
`Algorithm name : cn.endpointstrimmingextending`<br>
~~~~
INPUT : vector layer source (line or polygon)
BUFFER_TRIM_EXTEND : a decimal buffer radius (default: 4,0)
OUTPUT : vector layer computed (same type as input)
~~~~
<br>
<img src="https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/EndpointsStrimmingExtending.png?raw=true">
<br>
<br>
<br>
  
******

### **<ins>EndpointsSnapping()**</ins>
`Processing algorithm`<br>
`Snap lines endpoints' to each other's from a layer source.`<br>
`Algorithm name : cn.endpointssnapping`<br>
~~~~
INPUT : vector layer source (line or polygon)
BUFFER_SNAPPING : a decimal buffer radius (default: 2,0)
OUTPUT : vector layer computed (same type as input)
~~~~
<br>
<img src="https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/EndpointsSnapping.png?raw=true">
<br>
<br>
<br>


******

### **<ins>HubSnapping()**</ins>
`Processing algorithm`<br>
`Align lines vertices' hubs on top of each other within a buffer.`<br>
`Algorithm name : cn.hubsnapping`<br>
~~~~
INPUT : vector layer source (line or polygon)
BUFFER_REGION : a decimal buffer radius (default: 1,0)
OUTPUT : vector layer computed (same type as input)
~~~~
<br>
<img src="https://raw.githubusercontent.com/sducournau/consolidate_networks/main/ressources/HubSnapping.png?raw=true">
<br>
<br>
<br>




## 3. Snapping layer (from another layer)

### **<ins>SnapEndpointsToLayer()**</ins>
`Processing algorithm`<br>
`Snap lines endpoints' to each other's from an other layer source.`<br>
`Algorithm name : cn.snaphubspointstolayer`<br>
~~~~
INPUT : vector layer source (line or polygon)
REF_INPUT : vector layer source (point prefered)
BUFFER_SNAPPING : a decimal buffer radius (default: 2,0)
OUTPUT : vector layer computed (same type as input)
~~~~
<br>
<br>
<br>
  
******


### **<ins>SnapHubsPointsToLayer()</ins>**
`Processing algorithm`<br>
`Align lines vertices' hubs on top of a point layer within a buffer`<br>
`Algorithm name : cn.snapendpointstoLayer`<br>
~~~~
INPUT : vector layer source (line or polygon)
REF_INPUT : vector layer source (point prefered)
BUFFER_REGION : a decimal buffer radius (default: 2,0)
OUTPUT : vector layer computed (same type as input)
~~~~
<br>
<br>
<br>
  
