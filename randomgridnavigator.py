#Ryan Mendes CS 4731 Spring 2015
#Last saved 4:12 PM 1/18

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *

### INSTRUCTIONS:
### 1. Complete myCreatePathNetwork().


################
### RandomNavigator
###
### The RandomNavigator dynamically creates a path network. 
### But when asked to move the agent, it computes a random path through the network and probably fails to reach its destination.
		
class RandomGridNavigator(Navigator):

	def __init__(self):
		Navigator.__init__(self)
		self.cellSize = 0
	
	def setAgent(self, agent):
		Navigator.setAgent(self, agent)
		self.cellSize = agent.getRadius()*2.0

	### Create the pathnode network and pre-compute all shortest paths along the network
	### self: the navigator object
	### world: the world object		
	def createPathNetwork(self, world):
		self.pathnodes, self.pathnetwork = myCreatePathNetwork(world, self.cellSize)
		return None
		
	### Finds the shortest path from the source to the destination.
	### self: the navigator object
	### source: the place the agent is starting from (i.e., it's current location)
	### dest: the place the agent is told to go to
	def computePath(self, source, dest):
		# Make sure that the pathnodes have been created.
		if self.agent != None and self.world != None and self.pathnodes != None:
			start = findClosestUnobstructed(source, self.pathnodes, self.world.getLines())
			end = findClosestUnobstructed(dest, self.pathnodes, self.world.getLines())
			current = start
			path = [current]
			count = 0
			last = current
			while current != end and count < 100:
				count = count + 1
				successors = []
				for l in self.pathnetwork:
					if l[0] == current and l[1] != last:
						successors.append(l[1])
					elif l[1] == current and l[0] != last:
						successors.append(l[0])
				r = random.randint(0, len(successors)-1)
				last = current
				current = successors[r]
				path.append(current)
			self.setPath(path)
			self.source = source
			self.destination = dest
			# Get the first way point
			first = path.pop(0)
			# Tell the agent to move to the first waypoint
			if first is not None:
				self.agent.moveToTarget(first)

	def drawNavMesh(self, surface):
		if self.pathnodes is not None:
			size = self.agent.getRadius()*2.0
			for point in self.pathnodes:
				pygame.draw.line(surface, (0, 255, 0), (point[0]-size/2, point[1]-size/2), (point[0]+size/2, point[1]-size/2), 1)
				pygame.draw.line(surface, (0, 255, 0), (point[0]+size/2, point[1]-size/2), (point[0]+size/2, point[1]+size/2), 1)
				pygame.draw.line(surface, (0, 255, 0), (point[0]+size/2, point[1]+size/2), (point[0]-size/2, point[1]+size/2), 1)
				pygame.draw.line(surface, (0, 255, 0), (point[0]-size/2, point[1]+size/2), (point[0]-size/2, point[1]-size/2), 1)
		# if self.pathnetwork is not None:
		# 	for line in self.pathnetwork:
		# 		pygame.draw.line(surface, (0, 0, 255), (line[0][0], line[0][1]), (line[1][0], line[1][1]))

def matrixPathNetwork(world, cellSize, pathNodes) :
	worldObstacles = list(world.getObstacles)
	rawNetwork = []

	return rawNetwork

def exhaustivePathNetworkBuilder(world, cellSize, pathNodes) :
	worldObstacles = world.getObstacles()
	rawNetwork = []

	for point in pathNodes :
		drawCross(world.debug, point)

	for point in pathNodes :
		otherNodes = list(pathNodes)
		#otherNodes.remove(point)
		for otherPoint in otherNodes :
			if point != otherPoint :
				if withinRange(point, otherPoint, float(cellSize) * 1.4143) :
					newTuple = (point, otherPoint)
					if newTuple not in rawNetwork and reverseLine(newTuple) not in rawNetwork:
						rawNetwork.append(newTuple)
						#rawNetwork.append(reverseLine(newTuple))
	print "Network Length: ", len(rawNetwork)
	# print "Network: ", list(rawNetwork)
	return list(set(rawNetwork))

def pathNetworkBuilder(world, cellSize, pathNodes) :
	threshold = float(cellSize)
	worldObstacles = world.getObstacles()
	rawNetwork = []

	for point in pathNodes :
		drawCross(world.debug, point)

	for point in pathNodes :
		#Check up and to the right
		if (point[0]+threshold,point[1]-threshold) in pathNodes :
			tempTuple = (point, (point[0]+threshold,point[1]-threshold))
			rawNetwork.append(tempTuple)
		#Check up and to the left
		if (point[0]-threshold,point[1]-threshold) in pathNodes :
			tempTuple = (point, (point[0]-threshold,point[1]-threshold))
			rawNetwork.append(tempTuple)
		#Check down and to the right
		if (point[0]+threshold,point[1]+threshold) in pathNodes :
			tempTuple = (point, (point[0]+threshold,point[1]+threshold))
			rawNetwork.append(tempTuple)
		#Check down and to the left
		if (point[0]-threshold,point[1]+threshold) in pathNodes :
			tempTuple = (point, (point[0]-threshold,point[1]+threshold))
			rawNetwork.append(tempTuple)
		#Check directly above
		if (point[0],point[1]-threshold) in pathNodes :
			tempTuple = (point, (point[0],point[1]-threshold))
			rawNetwork.append(tempTuple)
		#Check directly below
		if (point[0],point[1]+threshold) in pathNodes :
			tempTuple = (point, (point[0],point[1]+threshold))
			rawNetwork.append(tempTuple)
		#Check directly left
		# if (point[0]-threshold,point[1]) in pathNodes :
		# 	tempTuple = (point, (point[0]-threshold,point[1]))
		# 	rawNetwork.append(tempTuple)
		#Check directly right
		if (point[0]+threshold,point[1]) in pathNodes :
			tempTuple = (point, (point[0]+threshold,point[1]))
			rawNetwork.append(tempTuple)
	#What's up with this point?
	# thisLine = (pathNodes[1],pathNodes[20])
	# rawNetwork.append(thisLine)
	return rawNetwork


def myCreatePathNetwork(world, cellsize):
	pathnodes = []
	pathnetwork = []

	threshold = float(cellsize)
	worldPoints = world.getPoints() #Corners are (0,0) (1024,0) (1024,768) (0,768), in that order
	worldLines = world.getLines()
	worldObstacles = world.getObstacles()
	worldWidth = world.dimensions[0]
	worldHeight = world.dimensions[1]
	drawCross(world.debug, (0,0))
	drawCross(world.debug, (threshold,threshold))

	testLine = ((0,0), (worldWidth, worldHeight))
	pathnetwork.append(testLine)

	rawGrid = []
	xCoord = float(threshold)/2.0
	print "threshold", threshold
	print "xCoord: ", xCoord
	print "World Width: ", worldWidth, " World Height: ", worldHeight, " World Dimensions: ", world.dimensions
	while (xCoord < worldWidth) :
		yCoord = float(threshold)/2.0
		while(yCoord < worldHeight) :
			currPoint = (xCoord, yCoord)
			if (isGood(currPoint, world, float(threshold))) :
				rawGrid.append(currPoint)
			yCoord += cellsize
		xCoord += cellsize

	pathnodes = rawGrid
	# for point in pathnodes :
	# 	drawCross(world.debug, point)

	# pathnetwork = pathNetworkBuilder(world, threshold, pathnodes)
	pathnetwork = exhaustivePathNetworkBuilder(world, threshold, pathnodes)

	print "Length of PathNodes: ", len(pathnodes)
	print "Length of PathNetwork: ", len(pathnetwork)

	# for point in worldPoints:
	# 	print point
	# for obstacle in world.obstacles:
	#     print obstacle.pos

	return pathnodes, pathnetwork


