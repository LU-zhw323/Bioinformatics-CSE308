import sys
import random
import numpy as np

#Weight for match, mismatch, cost of gaps
match = 1
mismatch = -4
gap_E = -0.5
gap_S = -11
impossible = float('-inf')


def parse_fasta(file):
    sequences = []
    with open(file, 'r') as f:
        seq = ''
        for line in f:
            if line.startswith('>'):
                if seq:
                    sequences.append(seq)
                    seq = ''
            else:
                seq += line.strip()
        if seq:
            sequences.append(seq)
    return sequences


#Function to see match or mismatch in two sequence:
def check_match(seq_1, seq_2, x_ind, y_ind):
	check_ind_x = x_ind - 1
	check_ind_y = y_ind - 1
	if seq_1[check_ind_x] == seq_2[check_ind_y]:
		return match
	else:
		return mismatch

#Function to fill the boundary of three grids
def fill_bound(M_grid, X_grid, Y_grid):
	#Fill M_grid
	d = 1
	for i in range(1, len(M_grid[0])):
		M_grid[0][i] = impossible
		Y_grid[0][i] = impossible
		X_grid[0][i] = gap_S + d*gap_E
		d += 1
	s = 1
	for i in range(1, len(M_grid)):
		M_grid[i][0] = impossible
		Y_grid[i][0] = gap_S + s*gap_E
		X_grid[i][0] = impossible
		s += 1
		
		

#Function to fill the grid
def fill_grid(M_grid, X_grid, Y_grid, seq_1, seq_2):
	for i in range(1, len(seq_2)+1):
		for j in range(1, len(seq_1)+1):
			#Fill the X_grid
			x_val = max(gap_S+gap_E+M_grid[i,j-1], gap_E+X_grid[i,j-1], gap_S+gap_E+Y_grid[i,j-1])
			X_grid[i,j] = x_val
			
			#Fill the Y_grid
			y_val = max(gap_S+gap_E+M_grid[i-1,j], gap_S+gap_E+X_grid[i-1,j], gap_E+Y_grid[i-1,j])
			Y_grid[i,j] = y_val
			
			#Fill the M_grid
			match_val = check_match(seq_1, seq_2,j, i)
			#m_val = match_val + max(M_grid[i-1,j-1], X_grid[i,j], Y_grid[i,j])
			m_val = max(match_val + M_grid[i-1,j-1], X_grid[i,j], Y_grid[i,j])
			M_grid[i,j] = m_val
			

#Funtion to determine the max cost
def determin_max(M_val, X_val, Y_val):
	max_val = max(M_val, X_val, Y_val)
	if max_val == M_val:
		return "M"
	elif max_val == X_val:
		return "X"
	else:
		return "Y"
	



#Function to do back tracking
def back_track(M_grid, X_grid, Y_grid, start_p, seq_1, seq_2):
	end_p = ("M", (0,0))
	res = ["", ""]
	while True:
		i = start_p[1][0]
		j = start_p[1][1]
		current_grid = start_p[0]
		next_step = ()
		#Currently in M-grid
		if current_grid == "M":
			match_val = check_match(seq_1, seq_2, j-1, i-1)
			M_val = M_grid[i-1,j-1] + match_val
			X_val = X_grid[i,j] + 0
			Y_val = Y_grid[i,j] + 0
			max_val = determin_max(M_val,X_val,Y_val)
			if max_val == "M":
				next_step = ("M", (i-1,j-1))
				if next_step == end_p:
					break
				if res[0] == "" and res[1] == "":
					res[0] += seq_1[j-1]
					res[1] += seq_2[i-1]
				res[0] += seq_1[j-1-1]
				res[1] += seq_2[i-1-1]
			elif max_val == "X":
				next_step = ("X", (i,j))
				if res[0] == "" and res[1] == "":
					res[0] += seq_1[j-1]
					res[1] += "_"
				else:
					list1 = list(res[1])
					list1[len(list1)-1] = "_"
					res[1] = ''.join(list1)
			elif max_val == "Y":
				next_step = ("Y", (i,j))
				if res[0] == "" and res[1] == "":
					res[0] += "_"
					res[1] += seq_2[i-1]
				else:
					list1 = list(res[0])
					list1[len(list1)-1] = "_"
					res[0] = ''.join(list1)
		
		#CUrrently in X-grid
		elif current_grid == "X":
			M_val = M_grid[i,j-1] + gap_S + gap_E
			X_val = X_grid[i,j-1] + gap_E
			Y_val = Y_grid[i,j-1] + gap_S + gap_E
			max_val = determin_max(M_val, X_val, Y_val)
			if max_val == "M":
				next_step = ("M", (i, j-1))
				res[0] += seq_1[j-1-1]
				res[1] += seq_2[i-1]
			elif max_val == "X":
				next_step = ("X", (i, j-1))
				res[0] += seq_1[j-1-1]
				res[1] += "_"
			elif max_val == "Y":
				next_step = ("Y", (i, j-1))
				res[0] += "_"
				res[1] += seq_2[i-1]
	
				
		#Currently in Y_grid
		elif current_grid == "Y":
			M_val = M_grid[i-1,j] + gap_S + gap_E
			X_val = X_grid[i-1,j] + gap_S + gap_E
			Y_val = Y_grid[i-1,j] + gap_E
			max_val = determin_max(M_val,X_val,Y_val)
			if max_val == "M":
				next_step = ("M", (i-1,j))
				res[0] += seq_1[j-1]
				res[1] += seq_2[i-1-1]
			elif max_val == "X":
				next_step = ("X", (i-1,j))
				res[0] += seq_1[j-1]
				res[0] += "_"
			elif max_val == "Y":
				next_step = ("Y", (i-1,j))
				res[0] += "_"
				res[1] += seq_2[i-1-1]
		start_p = next_step
	res[0] = res[0][::-1]
	res[1] = res[1][::-1]
	return res
			
			




filename = sys.argv[1]	
#file = open(filename)
#raw_reads = file.readlines()
#file.close()

seq = parse_fasta(filename)
name_list = []
with open(filename, 'r') as f:
	for line in f:
	    if line.startswith('>'):
	        name_list.append(line.replace("\n",''))
#Each time it will take 2 sequnces to do alignment
output = []
i = 0
j = i + 1
while len(seq) >= 2:
	#Take out the paired sequence
	seq_1 = seq.pop(0)
	seq_2 = seq.pop(0)
	#Find their length
	len_1 = len(seq_1)
	len_2 = len(seq_2)
	#Initialize grids
	M_grid = np.zeros((len_2+1, len_1+1),dtype=float)
	X_grid = np.zeros((len_2+1, len_1+1),dtype=float)
	Y_grid = np.zeros((len_2+1, len_1+1),dtype=float)
	#Fill the boundary of grids
	fill_bound(M_grid, X_grid, Y_grid)
	fill_grid(M_grid, X_grid, Y_grid, seq_1, seq_2)
	#print(M_grid)
	#print("____________")
	#print(X_grid)
	#print("_____________")
	#print(Y_grid)
	start_p = ("M", (len_2, len_1))
	res = back_track(M_grid, X_grid, Y_grid, start_p,seq_1, seq_2)
	#print(res[0])
	#print(res[1])
	output.append(name_list[i])
	output.append(res[0])
	output.append(name_list[i+1])
	output.append(res[1])
	i += 2
	print(res[0])
	print(res[1])
sequences = output

print("Alignment file is created: aligned_sequences.aln")
formatted_sequences = []
max_name_length = max([len(seq) for seq in sequences if seq.startswith('>')]) + 1
for i in range(0, len(sequences), 2):
    name = sequences[i].strip()
    sequence = sequences[i+1].strip()
    formatted_sequence = f"{name:{max_name_length}} {sequence}"
    formatted_sequences.append(formatted_sequence)

with open("aligned_sequences.aln", "w") as f:
    f.write('\n'.join(formatted_sequences))
    f.write("\n")

	 	 