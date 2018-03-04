'''
Maya command line tool by Carlos Breban

	Reads contents of Maya file and generates a report for several useful stats
Usage: 
in a windows command prompt:
	mayapy maya_get_file_stats.py folderorfilepath statoption
	
Where "folderorfilepath" would be the location of the maya file(s) 
and "statoption" is the filter for the report that you want printed back to the command line
These options include:

meshcount - total meshes in scene
polycount - total triangles in all meshes in scene
skincount - total unique skinClusters connected to meshes 
jointcount - total joits in scene (connected to skin clusters)
meshnames - all mesh names in scene
meshstatic - all non-skinned meshes in scene`
meshskinned - all skinned meshes in scene
skinnames - all skin cluster names in scene (connected to meshes)
jointnames - all joint names in scene (connected to skin clusters)

	
'''

import os
import maya.standalone
from sys import argv
import sys
maya.standalone.initialize()
import maya.cmds as cmds


'''

function to read stats from file and save CSV
from provided maya file

'''
def QueryFileStats(mayaFile):
	geoBank = []
	geoGet = cmds.ls( geometry=True)
	for i in range(0,len(geoGet)):
		if(cmds.objectType(geoGet[i]) == "mesh"):
			grpChk = cmds.listConnections(geoGet[i],d=True, s=False)
			if(cmds.objectType(grpChk[0]) != "groupParts"):	
				geoBank.append(geoGet[i]) 
	meshNameBank = cmds.listRelatives(geoBank, parent=True)	
	triangleBank = []
	skinClusterBank = []
	skinClusterJointBank = []
	meshSkinClusterBank = []
	jointsBank = []
	jointSkinClusterBank = []
	
	for current in geoBank:
		triangleBank.append(cmds.polyEvaluate( current, triangle=True )) 	
		skinC = cmds.listConnections( current, type="skinCluster")		
		if(skinC):		
			if skinC not in skinClusterBank:
				skinClusterBank.append(skinC)			
				curJoints = cmds.listConnections( skinC, type="joint")
				skinClusterJointBank.append(len(curJoints))				
				for curJoint in curJoints: 				
					if curJoint not in jointsBank:
						jointsBank.append(curJoint)
						jointSkinClusterBank.append(skinC)
		meshSkinClusterBank.append(skinC)
		
	fileLength = (len(meshNameBank) + len(skinClusterBank) + len(jointsBank) + 8)	
		
	totalTris = 0
	for i in range(0,len(triangleBank)):
		totalTris += triangleBank[i]	

	filePath = mayaFile[0:(len(mayaFile)-2)] + "csv"
	
	outputFile = open(filePath, 'w')

	outputFile.write("File Name:" + "," + mayaFile + ",\n")
	outputFile.write("Meshes:" + "," + str(len(meshNameBank)) + ",\n")
	outputFile.write("Triangles:" + "," + str(totalTris) + ",\n")
	outputFile.write("Skin Clusters:" + "," + str(len(skinClusterBank)) + ",\n")	
	outputFile.write("Bones:" + "," + str(len(jointsBank)) + ",\n")		
	outputFile.write(",,\n")
		
	outputFile.write("Mesh Name:" + "," + "Triangle Count:" + "," + "Skin Cluster Name:" + ",\n")	
	for i in range(0,len(meshNameBank)):
		if(meshSkinClusterBank[i] != None):
			outputFile.write(meshNameBank[i] + "," + str(triangleBank[i]) + "," + str((meshSkinClusterBank[i][0]).encode("utf-8")) + ",\n")
		else:
			outputFile.write(meshNameBank[i] + "," + str(triangleBank[i]) + "," + "" + ",\n")
	
	outputFile.write(",,\n")
	outputFile.write("Skin Cluster Name:" + "," + "Joint Count:" + ",\n")	
	for i in range(0,len(skinClusterBank)):
		outputFile.write(str(skinClusterBank[i][0]) + "," + str(skinClusterJointBank[i]) + ",\n")
		
	outputFile.write(",,\n")
	outputFile.write("Joint Name:" + "," + "Skin Cluster Name:" + ",\n")	
	for i in range(0,len(jointsBank)):
		outputFile.write(jointsBank[i] + "," + str(jointSkinClusterBank[i][0]) + ",\n")
		
	outputFile.close()
	
	return filePath

'''

function to read the CSV and report specific stats	
must provide a string for the part of the report requested (noted on tool description above)
also must provide the path to the csv

'''
def ReadFileStats(readOptions, inputFilePath):
	dataBank = []
	lineBank = []
	outData = []
	lineSplits = []
	readFile = open(inputFilePath, 'r')
	nextLine = readFile.readline()
	i = 0
	while nextLine:
		lineBank = nextLine.split(",")	
		dataBank.append(lineBank)	
		if(len(lineBank[0]) == 0):
			lineSplits.append(i)
		i+=1
		nextLine = readFile.readline()			
	readFile.close()

	if(readOptions == "meshcount"):
		outData = dataBank[1][1]
				
	if(readOptions == "polycount"):
		outData = "".join(dataBank[2][1])
		
	if(readOptions == "skincount"):
		outData = dataBank[3][1]
	
	if(readOptions == "jointcount"):
		outData = dataBank[4][1]		
	
	if(readOptions == "meshnames"):
		i = lineSplits[0]+2
		whileChk = True
		while whileChk:
			outData.append(dataBank[i][0])							
			i+=1
			whileChk = len(dataBank[i][0]) != 0
		if(len(outData) == 0):
			outData.append("No Meshes.")
			
	if(readOptions == "meshstatic"):
		i= lineSplits[0]+2
		whileChk = True
		while whileChk:
			if(len(dataBank[i][2]) == 0):
				outData.append(dataBank[i][0])							
			i+=1
			whileChk = len(dataBank[i][0]) != 0
		if(len(outData) == 0):
			outData.append("No Static Meshes.")
			
	if(readOptions == "meshskinned"):
		i= lineSplits[0]+2
		whileChk = True
		while whileChk:
			if(len(dataBank[i][2]) != 0):
				outData.append(dataBank[i][0])						
			i+=1
			whileChk = len(dataBank[i][0]) != 0			
		if(len(outData) == 0):
			outData.append("No Skinned Meshes.")			

	if(readOptions == "skinnames"):
		i= lineSplits[1]+2
		whileChk = True
		while whileChk:
			if(len(dataBank[i][0]) != 0):
				outData.append(dataBank[i][0])						
			i+=1
			whileChk = len(dataBank[i][0]) != 0		
		if(len(outData) == 0):
			outData.append("No Skin Clusters.")

	if(readOptions == "jointnames"):
		i= lineSplits[2]+2
		whileChk = True
		while whileChk:
			if(len(dataBank[i][0]) != 0):
				outData.append(dataBank[i][0])			
			i+=1	
			if(i < len(dataBank)):
				whileChk = len(dataBank[i][0]) != 0	
			else:
				whileChk = False
		if(len(outData) == 0):
			outData.append("No Joints.")			
	return outData	
	
	
'''
Main function

First Argument: maya folder path OR maya file name 
Second Argument: the string of the part of the report you want printed to the command line	
options are listed in the tool description above

'''	
def main():
	if(len(argv) > 1):
		dir = argv[1]
		mayaFiles = []
		statFiles = []
		
		if(os.path.isdir(dir)):
			for current in os.listdir(dir):
				if current.endswith('.ma') or current.endswith('.mb'):
					mayaFiles.append(dir + current)
					sys.stdout.write(dir + current + "\n")				
		else:
			if dir.endswith('.ma') or current.endswith('.mb'):	
				mayaFiles.append(os.path.abspath(dir))					
				
		for i in range(0,len(mayaFiles)):		
			cmds.file((mayaFiles[i]), force=True, open=True)
			curStatFile = QueryFileStats(mayaFiles[i])
			statFiles.append(curStatFile)
			sys.stdout.write("Report saved to: " + curStatFile + "\n")


		if(len(argv) == 3):	
			reportQuery = argv[2]		
			for i in range(0,len(statFiles)): 
				report = ReadFileStats(reportQuery, statFiles[i])
				sys.stdout.write(mayaFiles[i] + "\n")
				for i in range(0,len(report)):
					sys.stdout.write(report[i] + "\n")
	
if __name__ == "__main__":
	main()
maya.standalone.uninitialize()	