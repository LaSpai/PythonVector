import os
os.chdir('/home/user/git/geoScripting/PythonVector/data')

## Loading osgeo
try:
  from osgeo import ogr, osr
  print 'Import of ogr and osr from osgeo worked.  Hurray!\n'
except:
  print 'Import of ogr and osr from osgeo failed\n\n'

## Is the ESRI Shapefile driver available?
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

## choose your own name
## make sure this layer does not exist in your 'data' folder
fn = "Assignment.shp"
layername = "assignmentLayer"

## Create shape file
ds = drv.CreateDataSource(fn)
print ds.GetRefCount()

# Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')


## Create Layer
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
print(layer.GetExtent())

## Create a point
point1 = ogr.Geometry(ogr.wkbPoint)
point2 = ogr.Geometry(ogr.wkbPoint)

## Add points
point1.AddPoint(5.6660, 51.9872)
point2.AddPoint(5.6643, 51.9668)


#Export to KML
print point1.ExportToKML()
print point2.ExportToKML()

## Feature is defined from properties of the layer:e.g:

layerDefinition = layer.GetLayerDefn()
feature1 = ogr.Feature(layerDefinition)
feature2 = ogr.Feature(layerDefinition)

## Lets add the points to the feature
feature1.SetGeometry(point1)
feature2.SetGeometry(point2)

## Lets store the feature in a layer
layer.CreateFeature(feature1)
layer.CreateFeature(feature2)


print "The new extent"
print layer.GetExtent()

ds.Destroy()

qgis.utils.iface.addVectorLayer("Assignment.shp", "assignmentLayer", "ogr") 
aLayer = qgis.utils.iface.activeLayer()
print aLayer.name()

# Create Map
import os,os.path
import mapnik

#file with symbol for point
file_symbol=os.path.join("locationphoto.png")

#First we create a map
map = mapnik.Map(800, 400) #This is the image final image size

#Lets put some sort of background color in the map
map.background = mapnik.Color("steelblue") # steelblue == #4682B4 

#Create the rule and style obj
r = mapnik.Rule()
s = mapnik.Style()

polyStyle= mapnik.PolygonSymbolizer(mapnik.Color("grey"))
pointStyle = mapnik.PointSymbolizer(mapnik.PathExpression(file_symbol))
r.symbols.append(polyStyle)
r.symbols.append(pointStyle)

s.rules.append(r)
map.append_style("mapStyle", s)

# Adding point layer
layerPoint = mapnik.Layer("pointLayer")
layerPoint.datasource = mapnik.Shapefile(file=os.path.join("Assignment.shp"))

layerPoint.styles.append("mapStyle")

#adding polygon
layerPoly = mapnik.Layer("polyLayer")
layerPoly.datasource = mapnik.Shapefile(file=os.path.join("ne_110m_land.shp"))
layerPoly.styles.append("mapStyle")

#Add layers to map
map.layers.append(layerPoly)
map.layers.append(layerPoint)

#Set boundaries 
boundsLL = (1.3,51.979, 8.306,53.162) #(minx, miny, maxx,maxy)
map.zoom_to_box(mapnik.Box2d(*boundsLL)) # zoom to bbox


mapnik.render_to_file(map, os.path.join("Assignmentmap.png"), "png")
print "All done - check content"

#After talking with Jorge he told me that there is a problem in the boundaries function
#This problem occured also last year.
