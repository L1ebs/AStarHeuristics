from __future__ import annotations
from dataclasses import dataclass
import tkinter
from tkinter import *
import numpy
import sys
import heapq
import math


#-------------------------------------------------------------------------------------------------------
# Vertex dataclass
@dataclass
class Vertex:
	x: int
	y: int
	gn: float = 0
	hn: float = 0
	fn: float = 0
	parent: Vertex = None

	def __lt__(self, other):
		return self.fn < other.fn

	def __eq__(self, other):
		if isinstance(other, Vertex):
			return ( (self.x == other.x) and (self.y == other.y) )

		return False


# Variables -----------------------

# Fringe (open list) and closed list
fringe = []
heapq.heapify(fringe)
closed_list = []

mode = 0 # For deciding whether to use A* or Theta* (A* is default mode)

start_vertex = None
start_vertex_io = [0, 0]
goal_vertex = None
goal_vertex_io = [0, 0]

grid = None
grid_dimensions = [0, 0]
rows = None
columns = None

#-------------------------------------------------------------------------------------------------------
# Reading the file

# Check if a file is already provided in the arguments
if ( len(sys.argv) == 3 ):

	file_ptr = open(sys.argv[1], 'r')
	lines_ptr = file_ptr.readlines()
	mode = int(sys.argv[2])

	# Read line by line, storing the data into our variables

	# 1: Read start_vertex
	numbers=[]
	for word in lines_ptr[0].split():
		if word.isdigit():
			numbers.append(int(word))
	start_vertex=Vertex(numbers[1]-1,numbers[0]-1)

	

	# 2: Read goal_vertex
	numbers=[]
	for word in lines_ptr[1].split():
		if word.isdigit():
			numbers.append(int(word))
	goal_vertex=Vertex(numbers[1]-1,numbers[0]-1)



	# 3: Read dimensions of the grid
	numbers = []
	for word in lines_ptr[2].split():
		if word.isdigit():
			numbers.append(int(word))
	rows = numbers[1]
	columns = numbers[0]

	# grid_dimensions[0] = int(lines_ptr[2][0])
	# grid_dimensions[1] = int(lines_ptr[2][2])

	# rows = grid_dimensions[0] + 1
	# columns = grid_dimensions[1] + 1


	# 4: Read the grid
	grid = numpy.zeros((rows, columns), dtype=int)

	for line in lines_ptr[3:]:
		numbers = []
		for word in line.split():
			if word.isdigit():
				numbers.append(int(word))
		grid[numbers[1]-1][numbers[0]-1]= numbers[2]





# In case the file is not provided in the arguments
elif ( len(sys.argv) == 1):
	file_name = input("Please provide the name of the input file: ")
	mode = int(input("Please select which algorithm to run (0 for A*, 1 for Theta*): "))
	file_ptr = open('{}'.format(file_name), 'r')
	lines_ptr = file_ptr.readlines()

	# Read line by line, storing the data into our variables

	# 1: Read start_vertex
	numbers=[]
	for word in lines_ptr[0].split():
		if word.isdigit():
			numbers.append(int(word))
	start_vertex=Vertex(numbers[1]-1,numbers[0]-1)

	

	# 2: Read goal_vertex
	numbers=[]
	for word in lines_ptr[1].split():
		if word.isdigit():
			numbers.append(int(word))
	goal_vertex=Vertex(numbers[1]-1,numbers[0]-1)



	# 3: Read dimensions of the grid
	numbers = []
	for word in lines_ptr[2].split():
		if word.isdigit():
			numbers.append(int(word))
	rows = numbers[1]
	columns = numbers[0]

	# grid_dimensions[0] = int(lines_ptr[2][0])
	# grid_dimensions[1] = int(lines_ptr[2][2])

	# rows = grid_dimensions[0] + 1
	# columns = grid_dimensions[1] + 1


	# 4: Read the grid
	grid = numpy.zeros((rows, columns), dtype=int)

	for line in lines_ptr[3:]:
		numbers = []
		for word in line.split():
			if word.isdigit():
				numbers.append(int(word))
		grid[numbers[1]-1][numbers[0]-1]= numbers[2]

else:
	
	print("Usage: python3 problem1.py [file] [mode]")
	print("[file] -> file to be read")
	print("[mode] -> algorithm to use (0 for A*, 1 for Theta*)")
	quit()

#-------------------------------------------------------------------------------------------------------
# GUI Helper Functions

def drawGrid(canvas, rows, columns, tile_width, initial_header):
	for i in range(rows):
		for j in range(columns):

			if (grid[i][j] == 0):
				canvas.create_rectangle(j * tile_width + initial_header, i * tile_width + initial_header, (j * tile_width) + tile_width + initial_header, (i * tile_width) + tile_width + initial_header)

			else:
				canvas.create_rectangle(j * tile_width + initial_header, i * tile_width + initial_header, (j * tile_width) + tile_width + initial_header, (i * tile_width) + tile_width + initial_header, fill='#C1BCBB')

def create_circle(canvas, x, y, r, color):
	x0 = x - r
	y0 = y - r
	x1 = x + r
	y1 = y + r
	return canvas.create_oval(x0, y0, x1, y1, fill='{}'.format(color))

def drawVertices(canvas, rows, columns, tile_width, initial_header):
	for i in range(rows + 1):
		for j in range(columns + 1):
			create_circle(canvas, j * tile_width + initial_header, i * tile_width + initial_header, 3, 'black')

def draw_line(canvas, vertex_s, vertex_x, tile_width, initial_header):

	canvas.create_line( (vertex_s.y * tile_width + initial_header), (vertex_s.x * tile_width + initial_header), (vertex_x.y * tile_width + initial_header), (vertex_x.x * tile_width + initial_header), fill='#1655FF', width='5')

def myAction():
	numbers = []
	for word in (entry.get()).split():
		if word.isdigit():
			numbers.append(int(word))

	numbers_x = (numbers[0] - 1)
	numbers_y = (numbers[1] - 1)

	for element in closed_list:

		if (element.x == numbers_x and element.y == numbers_y):

			output_label["text"] = "Vertex [{}, {}]: Fn = {}, Gn = {}, Hn = {}".format(element.x + 1, element.y + 1, element.fn, element.gn, element.hn)


	for element in fringe:

		if (element.x == numbers_x and element.y == numbers_y):

			output_label["text"] = "Vertex [{}, {}]: Fn = {}, Gn = {}, Hn = {}".format(element.x + 1, element.y + 1, element.fn, element.gn, element.hn)


#-------------------------------------------------------------------------------------------------------
# Helper functions for A* and Theta*

# Function to check if a given connection between two vertices is vaild (By seeing if they are blocked)
def check_vertices(s1, vertex_list, rows, columns, grid):

	# Two special connections between vertices: Edges or Diagonals

	for s2 in vertex_list:

		keep = False


		# Edges: they either share an x or y in common
		# (x, y1), (x, y2)
		if (s1.x == s2.x):

			# Take the smaller value of y
			if (s1.y < s2.y):

				# Check if it is within bounds
				if ( (s1.x >= 0 and s1.x <= rows-1) and (s1.y >= 0 and s1.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s1.x][s1.y] == 0):
						keep = True

				# Check if it is within bounds
				if ( (s1.x-1 >=0 and s1.x-1 <= rows-1) and (s1.y >= 0 and s1.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s1.x-1][s1.y] == 0):
						keep = True

			# (s2.y < s1.y)
			else:

				# Check if it is within bounds
				if ( (s2.x >= 0 and s2.x <= rows-1) and (s2.y >= 0 and s2.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s2.x][s2.y] == 0):
						keep = True

				# Check if it is within bounds
				if ( (s2.x-1 >=0 and s2.x-1 <= rows-1) and (s2.y >= 0 and s2.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s2.x-1][s2.y] == 0):
						keep = True


		# (x1, y), (x2, y)
		elif (s1.y == s2.y):

			# Take the smaller value of x
			if (s1.x < s2.x):

				# Check if it is within bounds
				if ( (s1.x >= 0 and s1.x <= rows-1) and (s1.y >= 0 and s1.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s1.x][s1.y] == 0):
						keep = True

				# Check if it is within bounds
				if ( (s1.x >=0 and s1.x <= rows-1) and (s1.y-1 >= 0 and s1.y-1 <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s1.x][s1.y-1] == 0):
						keep = True

			# (s2.y < s1.y)
			else:

				# Check if it is within bounds
				if ( (s2.x >= 0 and s2.x <= rows-1) and (s2.y >= 0 and s2.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s2.x][s2.y] == 0):
						keep = True

				# Check if it is within bounds
				if ( (s2.x >=0 and s2.x <= rows-1) and (s2.y-1 >= 0 and s2.y-1 <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s2.x][s2.y-1] == 0):
						keep = True


		# Diagonal: both their x and y are different
		# (x1, y1), (x2, y2)
		else:

			# Take the smaller vertex
			if (s1.x < s2.x and s1.y < s2.y):

				# Check if it is within bounds
				if ( (s1.x >= 0 and s1.x <= rows-1) and (s1.y >= 0 and s1.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s1.x][s1.y] == 0):
						keep = True


			elif (s1.x < s2.x and s1.y > s2.y):

				# Check if it is within bounds
				if ( (s1.x >= 0 and s1.x <= rows-1) and (s2.y >= 0 and s2.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s1.x][s2.y] == 0):
						keep = True


			elif (s1.x > s2.x and s1.y < s2.y):

				# Check if it is within bounds
				if ( (s2.x >= 0 and s2.x <= rows-1) and (s2.y >= 0 and s2.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s2.x][s1.y] == 0):
						keep = True

			else:

				# Check if it is within bounds
				if ( (s2.x >= 0 and s2.x <= rows-1) and (s2.y >= 0 and s2.y <= columns-1) ):

					# See if it is blocked / unblocked
					if (grid[s2.x][s2.y] == 0):
						keep = True



		if (keep == False):

			vertex_list.remove(s2)


	return vertex_list



def check_corners(s, rows, columns):

	result = []

	# Corners: if the vertex we check happens to be a corner
	# (0, 0)
	if ( s.x == 0 and s.y == 0):

		current_vertex = Vertex(s.x + 1, s.y)
		result.append(current_vertex)
		current_vertex = Vertex(s.x, s.y + 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y + 1)
		result.append(current_vertex)

	# (0, col - 1)
	elif ( s.x == 0 and s.y == (columns - 1) ):

		current_vertex = Vertex(s.x, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y)
		result.append(current_vertex)


	# (row - 1, 0)
	elif ( s.x == (rows - 1) and s.y == 0 ):

		current_vertex = Vertex(s.x - 1, s.y)
		result.append(current_vertex)
		current_vertex = Vertex(s.x - 1, s.y + 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x, s.y + 1)
		result.append(current_vertex)

	# (row - 1, col - 1)
	elif (s.x == (rows - 1) and s.y == (columns - 1) ):

		current_vertex = Vertex(s.x - 1, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x - 1, s.y)
		result.append(current_vertex)
		current_vertex = Vertex(s.x, s.y - 1)
		result.append(current_vertex)

	return result


def check_edges(s, rows, columns):

	result = []

	# Edges: if the vertex we check happens to be in the edge
	# Top side
	if (s.x == 0 and (s.y > 0 and s.y < columns - 1) ):

		current_vertex = Vertex(s.x, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y + 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x, s.y + 1)
		result.append(current_vertex)

	# Bottom side
	elif (s.x == rows - 1 and (s.y > 0 and s.y < columns - 1) ):

		current_vertex = Vertex(s.x, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x - 1, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x - 1, s.y)
		result.append(current_vertex)
		current_vertex = Vertex(s.x - 1, s.y + 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x, s.y + 1)
		result.append(current_vertex)

	# Left side
	elif (s.y == 0 and (s.x > 0 and s.x < rows - 1) ):

		current_vertex = Vertex(s.x - 1, s.y)
		result.append(current_vertex)
		current_vertex = Vertex(s.x - 1, s.y + 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x, s.y + 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y + 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y)
		result.append(current_vertex)		

	# Right side
	elif (s.y == columns - 1 and (s.x > 0 and s.x < rows - 1) ):

		current_vertex = Vertex(s.x - 1, s.y)
		result.append(current_vertex)
		current_vertex = Vertex(s.x - 1, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y)
		result.append(current_vertex)

	return result


def check_inner(s, rows, columns):

	result = []

	# Inner Square: if the vertex we check happens to be in the inner square of our grid

	if ( (s.x > 0 and s.x < rows - 1) and (s.y > 0 and s.y < columns - 1) ):

		current_vertex = Vertex(s.x - 1, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x - 1, s.y)
		result.append(current_vertex)
		current_vertex = Vertex(s.x - 1, s.y + 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x, s.y + 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y - 1)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y)
		result.append(current_vertex)
		current_vertex = Vertex(s.x + 1, s.y + 1)
		result.append(current_vertex)

	return result


def find_neighbors(s, rows, columns, grid):

	result = []

	# 3 Sets of cases: Corners, Edges, Everything else (inner square)

	# Check corners
	result = check_corners(s, rows, columns)

	if (result):
		result = check_vertices(s, result, rows, columns, grid)
		return result

	# Check edges
	result = check_edges(s, rows, columns)

	if (result):
		result = check_vertices(s, result, rows, columns, grid)
		return result

	# Check the inner square
	result = check_inner(s, rows, columns)
	result = check_vertices(s, result, rows, columns, grid)

	return result

#-------------------------------------------------------------------------------------------------------
# Update Vertex

def trace_path(canvas, s, tile_width, initial_header):

	if (s.parent == s):
		return

	else:
		draw_line(canvas, s, s.parent, tile_width, initial_header)
		trace_path(canvas, s.parent, tile_width, initial_header)


def get_distance(s, parent):

	distance = math.sqrt( math.pow(s.x - parent.x, 2) + math.pow(s.y - parent.y, 2) )
	return distance


def c(s, parent):

	return get_distance(s, parent)


def g(s):

	if (s.parent == s):
		return 0

	else:
		s.gn = get_distance(s, s.parent)
		return (s.gn + g(s.parent) )


def h(s, goal_vertex):
	
	result = (math.sqrt(2)) * (min( (abs(s.x - goal_vertex.x)) , abs(s.y - goal_vertex.y) )) + max( (abs(s.x - goal_vertex.x)) , (abs(s.y - goal_vertex.y)) ) - min( (abs(s.x - goal_vertex.x)), (abs(s.y - goal_vertex.y)))
	return result


def fringe_remove(fringe, item):

	temp = []

	while (fringe):

		temp.append(heapq.heappop(fringe))

	temp.remove(item)
	heapq.heapify(temp)
	fringe = temp

def update_vertex(s, x, goal_vertex):

	if ( g(s) + c(s, x) < x.gn ):

		x.gn = g(s) + c(s, x)
		x.hn = h(x, goal_vertex)
		x.fn = (x.gn + x.hn)
		x.parent = s

		if (x in fringe):

			fringe_remove(fringe, x)

		heapq.heappush(fringe, x)

def update_theta_vertex(s, x, goal_vertex):
	if LoS(s.parent, x):
		if(g(s.parent)+c(s.parent,x)<x.gn):
			x.gn = g(s.parent)+c(s.parent,x)
			x.hn = h(x,goal_vertex)
			x.fn = x.gn + x.hn
			x.parent = s.parent #<---------
			if x in fringe:
				fringe_remove(fringe,x)
			heapq.heappush(fringe,x)
	else:
		if ( g(s) + c(s, x) < x.gn ):

			x.gn = g(s) + c(s, x)
			x.hn = h(x, goal_vertex)
			x.fn = (x.gn + x.hn)
			x.parent = s

			if (x in fringe):

				fringe_remove(fringe, x)

			heapq.heappush(fringe, x)
            
        

#-------------------------------------------------------------------------------------------------------
# A* Algorithm

def a_star(start_vertex, goal_vertex, grid, rows, columns):

	# Initial setup
	start_vertex.gn = 0
	start_vertex.parent = start_vertex

	heapq.heappush(fringe, start_vertex)

	while (fringe):

		s = heapq.heappop(fringe)


		# Check if goal matches current vertex
		if (s == goal_vertex):
			return s

		closed_list.append(s)

		neighbors = find_neighbors(s, rows, columns, grid)
		
		for x in neighbors:

			if (x not in closed_list):

				if (x not in fringe):

					x.gn = float("inf")
					x.parent = None

				update_vertex(s, x, goal_vertex)


	return None

#--------------------------------------------------------------------------------------------------------------------
def theta_star(start_vertex, goal_vertex, grid, rows, columns):
	# Initial setup
	start_vertex.gn = 0
	start_vertex.parent = start_vertex

	heapq.heappush(fringe, start_vertex)

	while (fringe):

		s = heapq.heappop(fringe)


		# Check if goal matches current vertex
		if (s == goal_vertex):
			return s

		closed_list.append(s)

		neighbors = find_neighbors(s, rows, columns, grid)
		
		for x in neighbors:

			if (x not in closed_list):

				if (x not in fringe):

					x.gn = float("inf")
					x.parent = None

				update_theta_vertex(s, x, goal_vertex)


	return None



def LoS(parent, child):
	x0=parent.x
	y0=parent.y
	x1=child.x
	y1=child.y
	f=0
	diffy=y1-y0
	diffx=x1-x0
	if diffy < 0:
		diffy = -diffy
		sy=-1
	else:
		sy=1
	if diffx < 0:
		diffx=-diffx
		sx=-1
	else:
		sx=1
	if diffx>=diffy:
		while x0!=x1:
			f+=diffy
			if f>=diffx:
				if grid[int(x0+((sx-1)/2))][int(y0+((sy-1)/2))]==1:
					return 0
				y0+=sy
				f-=diffx
			if f!=0 and grid[int(x0+((sx-1)/2))][int(y0+((sy-1)/2))]==1:
				return 0
			if diffy==0 and grid[int(x0 + ((sx-1)/2))][y0] == 0 and grid[int(x0+((sx-1)/2))][y0-1]:
				return 0
			x0+=sx
	else:
		while y0!=y1:
			f+=diffx
			if f>=diffy:
				if grid[int(x0+((sx-1)/2))][int(y0+((sy-1)/2))]==1:
					return 0
				x0+=sx
				f-=diffy
			if f!=0 and grid[int(x0+((sx-1)/2))][int(y0+((sy-1)/2))]==1:
				return 0
			if diffx==0 and grid[x0][int(y0+((sy-1)/2))] == 1 and grid[x0-1][int(y0+((sy-1)/2))]==1:
				return 0
			y0+=sy
	return 1

#-------------------------------------------------------------------------------------------------------
# Create tkinter window to visualize everything
root = tkinter.Tk()


canvas = tkinter.Canvas(root, width=2000, height=2000, borderwidth=5, background='white')


# Draw the grid on our canvas
tile_width = 30
initial_header = 75
drawGrid(canvas, rows, columns, tile_width, initial_header)
drawVertices(canvas, rows, columns, tile_width, initial_header)

# Draw start and goal
create_circle(canvas, (start_vertex.y * tile_width + initial_header), (start_vertex.x * tile_width + initial_header), 7, '#F03510')
create_circle(canvas, (goal_vertex.y * tile_width + initial_header), (goal_vertex.x * tile_width + initial_header), 7, '#5EF010')

# Draw the reference numbers for the grid
count = 1
for i in range(rows + 1):
	num_label = Label(root, text="{}".format(count), bg='white')
	num_label.place(x = tile_width, y = ((i * tile_width) + initial_header - 5) )
	count = count + 1

count = 1
for i in range(columns + 1):
	num_label = Label(root, text="{}".format(count), bg='white')
	num_label.place(x = ((i * tile_width) + initial_header - 5), y = tile_width )
	count = count + 1


# Handle user input
label = Label(root, text="Please, provide the coordinates of the vertex to get (y x):", bg='white')
label.place(x=70 , y = ((rows * tile_width) + initial_header + 50) )

entry = Entry(root, width=5, bg='#C4C4C4')
entry.place(x=450 , y = ((rows * tile_width) + initial_header + 50) )

button = Button(root, text="Find", command=myAction)
button.place(x=500 , y = ((rows * tile_width) + initial_header + 50) )

output_label = Label(root, text="", bg='white')
output_label.place(x=70 , y = ((rows * tile_width) + initial_header + 100) )


final_result = None
if (mode == 0):
	final_result = a_star(start_vertex, goal_vertex, grid, rows, columns)

else:
	final_result = theta_star(start_vertex, goal_vertex, grid, rows, columns)


trace_path(canvas, final_result, tile_width, initial_header)




canvas.pack()

root.mainloop()

