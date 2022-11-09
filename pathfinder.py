import cv2 as cv
import numpy as np
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import pyautogui
from time import sleep
import ctypes

# Set the time.sleep function's resolution to 1ms
ctypes.windll.winmm.timeBeginPeriod(1)

def image_to_bitmap(image):
	bitmap = np.all(image>np.array([200,200,200]), axis=2)
	bitmap = bitmap.astype(int)
	return bitmap

def bitmap_to_image(bitmap):
	bitmap = bitmap[:,:,np.newaxis]
	image = bitmap*[255, 255, 255]
	image = image.astype("uint8")
	return image

class Pathfinding:
	def __init__(self, start, end, image):
		self.start = start
		self.end = end
		self.bitmap = image_to_bitmap(image)

	def find_path(self):
		grid = Grid(matrix=self.bitmap)
		start = grid.node(self.start[0], self.start[1])
		end = grid.node(self.end[0], self.end[1])

		finder = AStarFinder(diagonal_movement=False)
		self.path, runs = finder.find_path(start,end,grid)
		self.path = np.array(self.path)
		self.path = np.flip(self.path, axis=1) # Change from (x,y) to (y,x) for OpenCV

	def read_directions(self):
		done_reading_directions = False
		i, final_i = 0, self.path.shape[0]
		current_node = self.path[0]
		next_node = self.path[1]
		list_of_directions = []
		while not done_reading_directions:
			current_direction = next_node-current_node
			next_direction = current_direction
			distance = 0
			while np.all(next_direction == current_direction):
				distance += 1
				i += 1
				if i+1 == final_i:
					done_reading_directions = True
					break
				current_node = self.path[i]
				next_node = self.path[i+1]
				next_direction = next_node-current_node

			list_of_directions.append((current_direction, distance))
		self.directions = list_of_directions

	def pathy_image(self):
		pathy_bitmap = self.bitmap
		for coord in self.path:
			pathy_bitmap[coord[0], coord[1]]=0
		return pathy_bitmap

	def main(self):
		self.find_path()
		self.read_directions()

image = cv.imread('images//map_loopylane.jpg')
loopylane = Pathfinding((218,356), (566,262), image)
loopylane.main()

# pyautogui stuff
rotation = 3.48 # Seconds it takes to do a 360 rotation by holding right arrow key.
pps = 10.6 # Number of pixels moved when up arrow key is held for one second.

sleep(2)

class Player:
	def __init__(self):
		self.direction = np.array([-1,0])
		self.angle = self.direction_to_angle(self.direction)
		self.full_rotation = 3 # Seconds it takes to do a 360 rotation by holding right arrow key.
		self.pps = 16 # Number of pixels moved when up arrow key is held for one second.

	def press_key(self,key,duration):
		pyautogui.keyDown(key)
		sleep(duration)
		pyautogui.keyUp(key)

	def rotate(self,degrees):
		if degrees < 0:
			key = "right"
		if degrees >= 0:
			key = "left"
		duration = (abs(degrees)/360)*self.full_rotation
		self.angle += degrees
		self.angle = self.angle%360
		print("my angle is: "+str(self.angle))
		self.press_key(key, duration)

	def direction_to_angle(self, direction):
		# Takes vector direction and converts it to angle in degrees.
		if np.all(direction == np.array([0, 1])):
			angle = 0
		if np.all(direction == np.array([-1, 0])):
			angle = 90
		if np.all(direction == np.array([0, -1])):
			angle = 180
		if np.all(direction == np.array([1, 0])):
			angle = 270
		return angle

	def change_direction(self, new_direction):
		new_angle = self.direction_to_angle(new_direction)
		# Find which direction to turn in (smaller angle is preferred)
		# positive_angle = new_angle - self.angle
		# negative_angle = 360 - abs(positive_angle)
		# if abs(positive_angle) < negative_angle:
		# 	degrees = positive_angle
		# else:
		# 	degrees = negative_angle
		# self.direction = new_direction
		degrees = new_angle - self.angle
		self.rotate(degrees)

	def move_forward(self,pixels):
		duration = pixels/self.pps
		self.press_key("up", duration)
		
	def follow_directions(self):
		directions = loopylane.directions
		print(self.direction)
		for instruction in directions:
			direction = instruction[0]
			distance = instruction[1]
			print("changing direction to "+str(direction))
			self.change_direction(direction)
			print("move pixels: "+str(distance))
			self.move_forward(distance)

hopeful = Player()
hopeful.follow_directions()

# print(loopylane.directions)

# pathy = loopylane.pathy_image()
# pathy = bitmap_to_image(pathy)
# cv.imshow("pathy",pathy)
# cv.waitKey()