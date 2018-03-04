# Python
Sample Python Tools for Maya, Lightwave, etc.

## Maya Get File Stats

Reads contents of Maya file(s) and generates a **.csv** report for several useful stats

in a windows command prompt:
	***mayapy maya_get_file_stats.py folderorfilepath statoption***
	
Where **"folderorfilepath"** would be the location of the maya file(s) 
and **"statoption"** is the filter for the report that you want printed back to the command line

These options include:

**meshcount** - total meshes in scene

**polycount** - total triangles in all meshes in scene

**skincount** - total unique skinClusters connected to meshes 

**jointcount** - total joits in scene (connected to skin clusters)

**meshnames** - all mesh names in scene

**meshstatic** - all non-skinned meshes in scene`

**meshskinned** - all skinned meshes in scene

**skinnames** - all skin cluster names in scene (connected to meshes)

**jointnames** - all joint names in scene (connected to skin clusters)

**Note:** Each csv report will be located next to the maya file
