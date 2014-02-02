dimensioning
============

QGIS plugin for dimensioning.

Help
====

Select two points, then choose the length of the help lines and a start and/or endoffset. The startoffset is the distance between the start of
the help lines (or the main/dimension line if the length of the help lines is 0). The endoffset is used for the displacement of the main line
(if there are some help lines). The offsets and the length of the help lines are defined in map units.

The lines are stored in two layers in a spatialite database. You can use a layer_id (an integer value) to arrange them a bit. 

There are two simple styles in the plugin directory. 
The default one: black lines, main line with arrows and the length of the line is written
on top of the line. 
The red one: ditto in red.

Known Issues
============

* It won't work with on-the-fly transformation enabled.
* Everything is static. Once you created the lines the won't move if you change the points/vertex they are assigned to.
