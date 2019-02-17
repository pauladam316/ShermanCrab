import pyscreenshot as ImageGrab
import time
import numpy
import pyautogui

grid_width, grid_height = 30, 16
x_offset, y_offset, square_halfsize = 436,190,10

#values of the squares. 0-8 are self explanatory. 9 is flagged, 10 is uncovered
values = numpy.zeros((grid_width,grid_height))

def screenCoordsToGridPos(position):
	return[(position[0]-x_offset)/(square_halfsize*2),(position[1]-y_offset)/(square_halfsize*2)]

def gridPosToScreenCoords(position):
	return[position[0]*square_halfsize*2+x_offset, position[1]*square_halfsize*2+y_offset]

def clickLeft(position):
	pyautogui.click(x=position[0], y=position[1], button='left')

def clickRight(position):
	pyautogui.click(x=position[0], y=position[1], button='right')

def updateValues():
	width, height = rgb_im.size
	y = 20
	x_index = 0
	y_index = 0
	while y_index < grid_height:
		x = 48
		x_index = 0
		while x_index < grid_width:
			if (values[x_index][y_index] == 9):
				continue
			r, g, b = rgb_im.getpixel((x,y))
			if (r == 189 and g == 189 and b == 189):
				r, g, b = rgb_im.getpixel((x-11,y))
				if (r == 169 and g == 169 and b == 169):
					values[x_index][y_index] = 0
				elif (r == 255 and g == 255 and b == 255):
					values[x_index][y_index] = 10
			elif (r == 94 and g == 94 and b == 222):
				values[x_index][y_index] = 1
			elif (r == 0 and g == 123 and b == 0):
				values[x_index][y_index] = 2
			elif (r == 255 and g == 0 and b == 0):
				values[x_index][y_index] = 3
			elif (r == 0 and g == 0 and b == 123):
				values[x_index][y_index] = 4
			elif (r == 123 and g == 0 and b == 0):
				values[x_index][y_index] = 5
			elif (r == 0 and g == 123 and b == 123):
				values[x_index][y_index] = 6
			elif (r == 0 and g == 0 and b == 0):
				values[x_index][y_index] = 7
			elif (r == 123 and g == 123 and b == 123):
				values[x_index][y_index] = 8
			x_index += 1
			x += 20
		y_index += 1
		y += 20

def findAllAdjacent(position):
	count = 0
	for y in range(position[1]-1, position[1]+2):
		if (y < 0 or y >= grid_height): continue
		for x in range(position[0]-1, position[0]+2):
			print("run")
			print(position[0])
			print(position[1])
			print(values[position[0],position[1]])
			if (x == y): continue
			if (x < 0 or x >= grid_width): continue
			if (values[x,y] == 9 or values[x,y] == 10): count += 1
	return count

def flagLocation(position):
	if (position[0] < 0 or position[0] >= grid_width or position[1] < 0 or position[1] >= grid_height): print ("out of range flag placement")
	if values[position[0],position[1]] == 10:
		values[position[0],position[1]] = 9
		clickRight(gridPosToScreenCoords(position))

def flagAllAdjacent(position):
	for y in range(position[1]-1, position[1]+2):
		if (y < 0 or y >= grid_height): continue
		for x in range(position[0]-1, position[0]+2):
			if (x < 0 or x >= grid_width): continue
			flagLocation([x,y])

def flagConfirmed(position):
	if (values[position[0],position[1]] != 0 and values[position[0],position[1]] != 9 and values[position[0],position[1]] != 10):
		if (findAllAdjacent(position) == values[position[0],position[1]]):
			print ("found")
			print(values[position[0],position[1]])
			flagAllAdjacent(position)

def performForAll(operation):
	for y in range(0,grid_height):
		for x in range(0,grid_width):
			operation([x,y])


while (1):
	# part of the screen
	time.sleep(5)
	im=ImageGrab.grab(bbox=(400,180,1200,530),childprocess=False)
	im.save('screenshot.png')
	rgb_im = im.convert('RGB')
	updateValues()
	print(values)
	performForAll(flagConfirmed)

