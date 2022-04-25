import os
import sys
import random

#----------------------------------------------------------------------------------------------

dir_path = '/common/home/tma105/cs440/Project 1/Test_Cases'


# Get the number of files requested from the user
num_files = int(input("Please provide the number of files to be generated: "))


# Generate that many test files
for file in range(num_files):

	current_name = "test{}.txt".format( (file + 1) )

	complete_name = os.path.join(dir_path, current_name)

	#-----------------------------------------------------
	# Now write on each file the corresponding data
	file_ptr = open(complete_name, 'w')


	# Generate random values
	
	# Dimensions
	rows = random.randint(3, 30)
	columns = random.randint(3, 30)

	# Start vertex
	start_x = random.randint(1, rows)
	start_y = random.randint(1, columns)

	# Goal vertex
	goal_x = random.randint(1, rows)
	goal_y = random.randint(1, columns)

	
	# Write Start vertex
	file_ptr.write("{} {}\n".format(start_x, start_y))

	# Write Goal vertex
	file_ptr.write("{} {}\n".format(goal_x, goal_y))

	# Write Dimensions
	file_ptr.write("{} {}\n".format(rows, columns))



	# Now, assign a value for every cell (blocked / unblocked)
	for i in range(rows):
		for j in range(columns):

			# 10% Probability to be blocked, 90% to be unblocked
			draw = random.randint(1, 100)

			if (draw <= 10):
				file_ptr.write("{} {} 1\n".format(i+1, j+1))

			else:
				file_ptr.write("{} {} 0\n".format(i+1, j+1))

	file_ptr.close()