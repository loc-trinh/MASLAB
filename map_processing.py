def get_int(x):
	if x.isdigit():
		return int(x)
	return x

map_input = open("green_map.txt",'r')
max_loc = 0
lines = []
for line in map_input:
	line = line.strip()
	elements = line.split(",")
	elements = map(get_int,elements)
	print elements
	
	lines.append(elements)
	for elt in elements:
		if isinstance(elt,int):
			max_loc = max(max_loc,elt)
grid = [['-' for x in range(max_loc+1)] for x in range(max_loc+1)]
map_input.close()
print len(grid)
# Wall (W)
# Platform (P)
# Red Cube (R)
# Green Cube (G)
# Stack of Cubes (S)
# Home Base (H) (DOESN'T MATTER)
# Start Location (L)
for read_line in lines:
	if(read_line[0] == 'W'):
		for x in xrange(2,len(read_line),+2):
			grid[int(read_line[x])][int(read_line[x-1])] = 'W'

	elif(read_line[0] == 'P'):
		for x in xrange(2,len(read_line),+2):
			grid[int(read_line[x])][int(read_line[x-1])] = 'W'
	elif(read_line[0] == 'S'):
		grid[int(read_line[2])][int(read_line[1])] = read_line[3] #not caring about stacks right now...
	# elif(read_line[0] == 'H'):
	# 	for x in xrange(3,len(read_line),+2):
	# 		grid[int(read_line[x-1])-1][int(read_line[x])-1] = 'H'	
	# 		print read_line[x-1]
	# 		print read_line[x]
	#LOLNOPE

	elif(read_line[0] == 'L'):
		grid[int(read_line[2])][int(read_line[1])] = 'L'

#print grid

out = open("map_output3.txt",'w')
for line in grid:
	out.write(" ".join(line))
	out.write("\r\n")
out.close()

grid2 = [['-' for x in range(3*max_loc)] for x in range(3*max_loc)]


for read_line in lines:
	if(read_line[0] == 'W'):
		x_result = read_line[1] - read_line[3]
		y_result = read_line[2] - read_line[4]
		if(x_result == 0 and y_result == 1):
			new_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_y = read_line[4] * 3
			while(start_y >= end_y):
				grid2[start_y][new_x] = 'W'
				start_y -= 1
		elif(x_result == 0 and y_result == -1):
			new_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_y = read_line[4] * 3
			while(start_y <= end_y):
				grid2[start_y][new_x] = 'W'
				start_y += 1

		elif(x_result == 1 and y_result == 0):
			new_y = read_line[2] * 3
			start_x = read_line[1] * 3
			end_x = read_line[3] * 3
			while(start_x >= end_x):
				grid2[new_y][start_x] = "W"
				start_x -= 1

		elif(x_result == -1 and y_result == 0):
			new_y = read_line[2] * 3
			start_x = read_line[1] * 3
			end_x = read_line[3] * 3
			while(start_x <= end_x):
				grid2[new_y][start_x] = "W"
				start_x += 1			

		elif(x_result == 1 and y_result == 1):
			start_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_x = read_line[3] * 3
			end_y = read_line[4] * 3
			while start_x > end_x and start_y > end_y:
				grid2[start_y][start_x] = 'W'
				start_x -= 1
				start_y -= 1

		elif(x_result == 1 and y_result == -1):
			start_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_x = read_line[3] * 3
			end_y = read_line[4] * 3
			while start_x > end_x and start_y < end_y:
				grid2[start_y][start_x] = 'W'
				start_x -= 1
				start_y += 1

		elif(x_result == -1 and y_result == 1):
			start_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_x = read_line[3] * 3
			end_y = read_line[4] * 3
			while start_x < end_x and start_y < end_y:
				grid2[start_y][start_x] = 'W'
				start_x += 1
				start_y -= 1

		elif(x_result == -1 and y_result == -1):
			start_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_x = read_line[3] * 3
			end_y = read_line[4] * 3
			# print "Y HERE"
			# print read_line[2]
			# print read_line[4]
			while start_x < end_x and start_y < end_y:
				grid2[start_y][start_x] = 'W'
				start_x += 1
				start_y += 1
				print start_x
				print start_y

		# for x in xrange(2,len(read_line),+2):
		# 	grid[int(read_line[x-1])-1][int(read_line[x])-1] = 'W'

	elif(read_line[0] == 'P'):

		x_result = read_line[1] - read_line[3]
		y_result = read_line[2] - read_line[4]
		if(x_result == 0 and y_result == 1):
			new_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_y = read_line[4] * 3
			while(start_y >= end_y):
				grid2[start_y][new_x] = 'W'
				start_y -= 1
		elif(x_result == 0 and y_result == -1):
			new_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_y = read_line[4] * 3
			while(start_y <= end_y):
				grid2[start_y][new_x] = 'W'
				start_y += 1

		elif(x_result == 1 and y_result == 0):
			new_y = read_line[2] * 3
			start_x = read_line[1] * 3
			end_x = read_line[3] * 3
			while(start_x >= end_x):
				grid2[new_y][start_x] = 'W'
				start_x -= 1

		elif(x_result == -1 and y_result == 0):
			new_y = read_line[2] * 3
			start_x = read_line[1] * 3
			end_x = read_line[3] * 3
			while(start_x <= end_x):
				grid2[new_y][start_x] = 'W'
				start_x += 1			

		elif(x_result == 1 and y_result == 1):
			start_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_x = read_line[3] * 3
			end_y = read_line[4] * 3
			while start_x > end_x and start_y > end_y:
				grid2[start_y][start_x] = 'W'
				start_x -= 1
				start_y -= 1

		elif(x_result == 1 and y_result == -1):
			start_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_x = read_line[3] * 3
			end_y = read_line[4] * 3
			while start_x > end_x and start_y < end_y:
				grid2[start_y][start_x] = 'W'
				start_x -= 1
				start_y += 1

		elif(x_result == -1 and y_result == 1):
			start_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_x = read_line[3] * 3
			end_y = read_line[4] * 3
			while start_x < end_x and start_y < end_y:
				grid2[start_y][start_x] = 'W'
				start_x += 1
				start_y -= 1

		elif(x_result == -1 and y_result == -1):
			start_x = read_line[1] * 3
			start_y = read_line[2] * 3
			end_x = read_line[3] * 3
			end_y = read_line[4] * 3
			# print "Y HERE"
			# print read_line[2]
			# print read_line[4]
			while start_x < end_x and start_y < end_y:
				grid2[start_y][start_x] = 'W'
				start_x += 1
				start_y += 1
				print start_x
				print start_y
		
		# for x in xrange(2,len(read_line),+2):
		# 	grid2[int(read_line[x-1])-1][int(read_line[x])-1] = 'P'
		
	elif(read_line[0] == 'S'):
		grid2[3*(read_line[2])][3*(read_line[1])] = read_line[3] #not caring about stacks right now...
		
	# elif(read_line[0] == 'H'):
	# 	for x in xrange(3,len(read_line),+2):
	# 		grid[int(read_line[x-1])-1][int(read_line[x])-1] = 'H'	
	# 		print read_line[x-1]
	# 		print read_line[x]
	#LOLNOPE

	elif(read_line[0] == 'L'):
		grid2[3*(read_line[1])-1][3*(read_line[2])-1] = 'L'
		
out2 = open("map_output2.txt",'w')
for line in grid2:
	out2.write(" ".join(line))
	out2.write("\r\n")
out2.close()

grid3 = [['-' for x in range(3*(max_loc+1))] for x in range(3*(max_loc+1))]




for row in xrange((max_loc+1)):
	for col in xrange((max_loc+1)):
		if(grid[row][col] == 'W'):
			print "here"
			if(row < len(grid) - 1 and grid[row+1][col] == 'W'):
				print "case 1"
				start_row = row * 3 + 1
				end_row = (row+1) * 3 + 1
				new_col = col * 3 + 1
				while(start_row <= end_row):
					print "maybe here?"
					grid3[start_row][new_col] = 'W'
					start_row += 1

			if(row > 0 and grid[row-1][col] == 'W'):
				print "case 2"
				start_row = row * 3 + 1
				end_row = (row-1) * 3 + 1
				new_col = col * 3 + 1
				while(start_row <= end_row):
					grid3[start_row][new_col] = 'W'
					start_row -= 1

			if(col > 0 and grid[row][col-1] == 'W'):
				start_col = col * 3 + 1
				end_col = (col-1) * 3 + 1
				new_row = row * 3 + 1
				while(start_col >= end_col):
					grid3[new_row][start_col] = 'W'
					start_col -= 1

			if(col < len(grid) - 1 and grid[row][col+1] == 'W'):
				start_col = col * 3 + 1
				end_col = (col+1) * 3 + 1
				new_row = row * 3 + 1
				while(start_col <= end_col):
					grid3[new_row][start_col] = 'W'
					start_col += 1

			if(row < len(grid) - 1 and col < len(grid) - 1 and grid[row+1][col+1] == 'W' and grid[row+1][col] != 'W' and grid[row][col+1] != 'W'):
				start_row = row * 3 + 1
				end_row = (row+1) * 3 + 1
				start_col = col * 3 + 1
				end_col = (col+1) * 3 + 1
				while(start_row <= end_row and start_col <= end_col):
					grid3[start_row][start_col] = 'W'
					start_row += 1
					start_col += 1

			if(row > 0 and col > 0 and grid[row-1][col-1] == 'W' and grid[row-1][col] != 'W' and grid[row][col-1] == '-'):
				start_row = row * 3 + 1
				end_row = (row-1) * 3 + 1
				start_col = col * 3 + 1
				end_col = (col-1) * 3 + 1
				while(start_row >= end_row and start_col >= end_col):
					grid3[start_row][start_col] = 'W'
					start_row -= 1
					start_col -= 1			

			if(row > 0 and col < len(grid) - 1 and grid[row-1][col+1] == 'W' and grid[row-1][col] != 'W' and grid[row][col+1] != 'W'):
				start_row = row * 3 + 1
				end_row = (row-1) * 3 + 1
				start_col = col * 3 + 1
				end_col = (col+1) * 3 + 1
				while(start_row >= end_row and start_col <= end_col):
					grid3[start_row][start_col] = 'W'
					start_row -= 1
					start_col += 1
			if(row < len(grid) - 1 and col > 0 and grid[row+1][col-1] == 'W' and grid[row+1][col] != 'W' and grid[row][col-1] != 'W'):
				start_row = row * 3 + 1
				end_row = (row+1) * 3 + 1
				start_col = col * 3 + 1
				end_col = (col-1) * 3 + 1
				while(start_row <= end_row and start_col >= end_col):
					grid3[start_row][start_col] = 'W'
					start_row += 1
					start_col -= 1

		# x_result = read_line[1] - read_line[3]
		# y_result = read_line[2] - read_line[4]
		# if(x_result == 0 and y_result == 1):
		# 	new_x = read_line[1] * 3 + 1
		# 	start_y = read_line[2] * 3 + 1
		# 	end_y = read_line[4] * 3 + 1
		# 	while(start_y >= end_y):
		# 		grid3[start_y][new_x] = 'W'
		# 		start_y -= 1
		# elif(x_result == 0 and y_result == -1):
		# 	new_x = read_line[1] * 3 + 1
		# 	start_y = read_line[2] * 3 + 1
		# 	end_y = read_line[4] * 3 + 1
		# 	while(start_y <= end_y):
		# 		grid3[start_y][new_x] = 'W'
		# 		start_y += 1

		# elif(x_result == 1 and y_result == 0):
		# 	new_y = read_line[2] * 3 + 1
		# 	start_x = read_line[1] * 3 + 1
		# 	end_x = read_line[3] * 3 + 1
		# 	while(start_x >= end_x):
		# 		grid3[new_y][start_x] = "W"
		# 		start_x -= 1

		# elif(x_result == -1 and y_result == 0):
		# 	new_y = read_line[2] * 3 + 1
		# 	start_x = read_line[1] * 3 + 1
		# 	end_x = read_line[3] * 3 + 1
		# 	while(start_x <= end_x):
		# 		grid3[new_y][start_x] = "W"
		# 		start_x += 1			

		# elif(x_result == 1 and y_result == 1):
		# 	start_x = read_line[1] * 3 + 1
		# 	start_y = read_line[2] * 3 + 1
		# 	end_x = read_line[3] * 3 + 1
		# 	end_y = read_line[4] * 3 + 1
		# 	while start_x > end_x and start_y > end_y:
		# 		grid3[start_y][start_x] = 'W'
		# 		start_x -= 1
		# 		start_y -= 1

		# elif(x_result == 1 and y_result == -1):
		# 	start_x = read_line[1] * 3 + 1
		# 	start_y = read_line[2] * 3 + 1
		# 	end_x = read_line[3] * 3 + 1
		# 	end_y = read_line[4] * 3 + 1
		# 	while start_x > end_x and start_y < end_y:
		# 		grid3[start_y][start_x] = 'W'
		# 		start_x -= 1
		# 		start_y += 1

		# elif(x_result == -1 and y_result == 1):
		# 	start_x = read_line[1] * 3 + 1
		# 	start_y = read_line[2] * 3 + 1
		# 	end_x = read_line[3] * 3 + 1
		# 	end_y = read_line[4] * 3 + 1
		# 	while start_x < end_x and start_y < end_y:
		# 		grid3[start_y][start_x] = 'W'
		# 		start_x += 1
		# 		start_y -= 1

		# elif(x_result == -1 and y_result == -1):
		# 	start_x = read_line[1] * 3 + 1
		# 	start_y = read_line[2] * 3 + 1
		# 	end_x = read_line[3] * 3 + 1
		# 	end_y = read_line[4] * 3 + 1
		# 	# print "Y HERE"
		# 	# print read_line[2]
		# 	# print read_line[4]
		# 	while start_x < end_x and start_y < end_y:
		# 		grid3[start_y][start_x] = 'W'
		# 		start_x += 1
		# 		start_y += 1
		# 		print start_x
		# 		print start_y

		# # for x in xrange(2,len(read_line),+2):
		# 	grid[int(read_line[x-1])-1][int(read_line[x])-1] = 'W'

			
		elif(grid[row][col] == 'R'):
			grid3[3*(row) + 1][3*(col) + 1] = 'R'
		elif(grid[row][col] == 'G'):
			grid3[3*(row) + 1][3*(col) + 1] = 'G'
			
		# elif(read_line[0] == 'H'):
		# 	for x in xrange(3,len(read_line),+2):
		# 		grid[int(read_line[x-1])-1][int(read_line[x])-1] = 'H'	
		# 		print read_line[x-1]
		# 		print read_line[x]
		#LOLNOPE

		elif(grid[row][col] == 'L'):
			grid3[3*row + 1][3*col + 1] = 'L'


out4 = open("map_output4.txt",'w')
for line in grid3:
	out4.write(" ".join(line))
	out4.write("\r\n")
out4.close()
