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
	
	lines.append(elements)
	for elt in elements:
		if isinstance(elt,int):
			max_loc = max(max_loc,elt)
grid = [['-' for x in range(max_loc+1)] for x in range(max_loc+1)]
map_input.close()
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
		grid[int(read_line[2])][int(read_line[1])] = read_line[3] 

	elif(read_line[0] == 'L'):
		grid[int(read_line[2])][int(read_line[1])] = 'L'

# out = open("map_output3.txt",'w')
# for line in grid:
# 	out.write(" ".join(line))
# 	out.write("\r\n")
# out.close()

large_grid = [['-' for x in range(3*(max_loc+1))] for x in range(3*(max_loc+1))]




for row in xrange((max_loc+1)):
	for col in xrange((max_loc+1)):
		if(grid[row][col] == 'W'):
			if(row < len(grid) - 1 and grid[row+1][col] == 'W'):
				start_row = row * 3 + 1
				end_row = (row+1) * 3 + 1
				new_col = col * 3 + 1
				while(start_row <= end_row):
					large_grid[start_row][new_col] = 'W'
					start_row += 1

			if(row > 0 and grid[row-1][col] == 'W'):
				start_row = row * 3 + 1
				end_row = (row-1) * 3 + 1
				new_col = col * 3 + 1
				while(start_row <= end_row):
					large_grid[start_row][new_col] = 'W'
					start_row -= 1

			if(col > 0 and grid[row][col-1] == 'W'):
				start_col = col * 3 + 1
				end_col = (col-1) * 3 + 1
				new_row = row * 3 + 1
				while(start_col >= end_col):
					large_grid[new_row][start_col] = 'W'
					start_col -= 1

			if(col < len(grid) - 1 and grid[row][col+1] == 'W'):
				start_col = col * 3 + 1
				end_col = (col+1) * 3 + 1
				new_row = row * 3 + 1
				while(start_col <= end_col):
					large_grid[new_row][start_col] = 'W'
					start_col += 1

			if(row < len(grid) - 1 and col < len(grid) - 1 and grid[row+1][col+1] == 'W' and grid[row+1][col] != 'W' and grid[row][col+1] != 'W'):
				start_row = row * 3 + 1
				end_row = (row+1) * 3 + 1
				start_col = col * 3 + 1
				end_col = (col+1) * 3 + 1
				while(start_row <= end_row and start_col <= end_col):
					large_grid[start_row][start_col] = 'W'
					start_row += 1
					start_col += 1

			if(row > 0 and col > 0 and grid[row-1][col-1] == 'W' and grid[row-1][col] != 'W' and grid[row][col-1] == '-'):
				start_row = row * 3 + 1
				end_row = (row-1) * 3 + 1
				start_col = col * 3 + 1
				end_col = (col-1) * 3 + 1
				while(start_row >= end_row and start_col >= end_col):
					large_grid[start_row][start_col] = 'W'
					start_row -= 1
					start_col -= 1			

			if(row > 0 and col < len(grid) - 1 and grid[row-1][col+1] == 'W' and grid[row-1][col] != 'W' and grid[row][col+1] != 'W'):
				start_row = row * 3 + 1
				end_row = (row-1) * 3 + 1
				start_col = col * 3 + 1
				end_col = (col+1) * 3 + 1
				while(start_row >= end_row and start_col <= end_col):
					large_grid[start_row][start_col] = 'W'
					start_row -= 1
					start_col += 1

			if(row < len(grid) - 1 and col > 0 and grid[row+1][col-1] == 'W' and grid[row+1][col] != 'W' and grid[row][col-1] != 'W'):
				start_row = row * 3 + 1
				end_row = (row+1) * 3 + 1
				start_col = col * 3 + 1
				end_col = (col-1) * 3 + 1
				while(start_row <= end_row and start_col >= end_col):
					large_grid[start_row][start_col] = 'W'
					start_row += 1
					start_col -= 1
			
		elif(grid[row][col] == 'R'):
			large_grid[3*(row) + 1][3*(col) + 1] = 'R'
		elif(grid[row][col] == 'G'):
			large_grid[3*(row) + 1][3*(col) + 1] = 'G'

		elif(grid[row][col] == 'L'):
			large_grid[3*row + 1][3*col + 1] = 'L'


out = open("large_map_output.txt",'w')
for line in large_grid:
	out.write(" ".join(line))
	out.write("\r\n")
out.close()
