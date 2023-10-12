# <img src="https://github.com/sducournau/consolidate_networks/blob/main/icon.png?raw=true" width="50" height="50"> Consolidate Networks

**A Qgis plugin toolset for consolidate your network data**


*This plugin provides processing algorithms that allow you to manipulate the vertices of a line layer.
You can repair topological problems and clean your data.*

******

<br>

# Preview :

<img src=".\ressources\comparaison_ban.png">



# List of cn provider algorithms' :

## 1. Consolidate
 
  * **CalculateDbscan() :** 
  <img src=".\ressources\CalculateDbscan.png">
  Calculate dbscan clusters of lines from a layer source.
  

  * **ConsolidateWithDbscan() :** 
  <img src=".\ressources\CalculateDbscan2.png">s
  Snap lines to each other splitting by their clusters from a layer source resulted from CalculateDbscan().

  * **MakeIntersectionsVertexes() :**  
  Insert missing vertices from a source layer.

## 2. Snapping layer (from himself)

  * **EndpointsStrimmingExtending() :** 
  ![Alt](/ressources/EndpointsStrimmingExtending.png)
  Cut and extend end lines from a layer source.

  * **EndpointsSnapping() :** 
  <img src=".\ressources\EndpointsSnapping.png">
  Snap lines endpoints' to each other's from a layer source.

  * **HubSnapping() :** 
  <img src=".\ressources\HubSnapping.png">
  Align lines vertices' hubs on top of each other within a buffer.

## 3. Snapping layer (from another layer)

  * **SnapEndpointsToLayer() :**
  Snap lines endpoints' to each other's from an other layer source.

  * **SnapHubsPointsToLayer() :** 
  Align lines vertices' hubs on top of a point layer within a buffer.
