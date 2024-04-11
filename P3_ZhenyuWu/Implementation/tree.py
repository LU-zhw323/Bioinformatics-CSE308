# -*- coding: utf-8 -*-
import numpy as np
import UPGMA_tree
import Neighbor_tree
# A Binary Tree Node
class Node:
    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
 
class Trunk:
    def __init__(self, prev=None, str=None):
        self.prev = prev
        self.str = str
 
def showTrunks(p,outfile):
    if p is None:
        return
    showTrunks(p.prev,outfile)
    print(p.str, end='')
    print(p.str, end='',file = outfile)
 
 
def printTree(root, prev, isLeft, outfile):
    if root is None:
        return
 
    prev_str = '    '
    trunk = Trunk(prev, prev_str)
    printTree(root.right, trunk, True,outfile)
 
    if prev is None:
        trunk.str = '____'
    elif isLeft:
        trunk.str = '+---'
        prev_str = '   |'
    else:
        trunk.str = '+---'
        prev.str = prev_str
 
    showTrunks(trunk, outfile)
    print(str(root.data))
    print(str(root.data),file = outfile)
    if prev:
        prev.str = prev_str
    trunk.str = '   |'
    printTree(root.left, trunk, False, outfile)

def buildTree(data):
    if isinstance(data, int) or isinstance(data,str):
        return Node(data)
    else:
        value = data[0]
        if len(data) < 2:
            return None
        left_data = data[1]
        right_data = data[2]
        left = buildTree(left_data)
        right = buildTree(right_data)
        return Node(value, left, right)
        
        
def parse_matrix():
	size = 0
	raw_seq = []
	raw_matrix = []
	with open('matrix', 'r') as file:
		counter = 1
		for line in file:
			temp = line.replace('\n','')
			if counter == 1:
				size = int(temp)
			else:
				seq = temp[:10]
				raw_seq.append(seq.replace(' ',''))
				row = (temp[10:] + '0.0').split(' ')
				row = [x for x in row if x != '']
				raw_matrix.append(row)
			counter += 1
	mylist = raw_matrix
	# Get the dimensions of the original list of lists
	num_rows = len(mylist)
	num_cols = max([len(row) for row in mylist])

	# Create a numpy array of zeros with the same dimensions as the original list of lists
	myarray = np.zeros((num_rows, num_cols))

	# Copy the values from the original list of lists to the numpy array
	for i in range(num_rows):
	    for j in range(len(mylist[i])):
	        myarray[i, j] = abs(float(mylist[i][j]))

	# Fill the remaining elements with 0.0
	myarray[myarray == 0] = 0.0
	
	for i in range(0, size):
		myarray[i,:] = myarray[:,i]
	
	return(raw_seq, myarray)



			
def print_leaf(node, parent,length,outfile):
    if isinstance(node, tuple):
        for child in node[1:]:
            print_leaf(child, node[0],length,outfile)
    else:
        print(parent, "to", node,": ", length[parent]-length[node])
        print(parent, "to", node,": ", length[parent]-length[node],file = outfile)
			
def	print_parent(node,length,outfile):
	if isinstance(node[1], tuple) and isinstance(node[2],tuple):
		print(node[0], 'to', node[1][0],": ", length[node[0]]- length[node[1][0]])
		print(node[0], 'to', node[1][0],": ", length[node[0]]- length[node[1][0]],file=outfile)
		print(node[0], 'to', node[2][0],": ", length[node[0]]- length[node[2][0]])
		print(node[0], 'to', node[2][0],": ", length[node[0]]- length[node[2][0]],file = outfile)
		print_parent(node[1],length,outfile)
		print_parent(node[2],length,outfile)
	elif isinstance(node[1], tuple):
		print(node[0], 'to', node[1][0],": ", length[node[0]]- length[node[1][0]])
		print(node[0], 'to', node[1][0],": ", length[node[0]]- length[node[1][0]],file = outfile)
		print_parent(node[1],length,outfile)
	elif isinstance(node[2], tuple):
		print(node[0], 'to', node[2][0],": ", length[node[0]]- length[node[2][0]])
		print(node[0], 'to', node[2][0],": ", length[node[0]]- length[node[2][0]],file = outfile)
		print_parent(node[2],length,outfile)
			
			
def print_length(tree, length,outfile):
	print_parent(tree,length,outfile)
	print_leaf(tree,None, length,outfile)
			
			
			
			
			
			
	
in_file = parse_matrix()
dm = in_file[1]
raw_list = in_file[0]
decision = -1
while True:
	print("<[1]: UPGMA TREE>")
	print("<[2]: NEIGHBOR JOINING TREE>")
	user_in = input("<SELECT A TREE, PRESS 1 or 2>")
	if user_in == str(1):
		decision = 1
		break
	elif user_in == str(2):
		decision = 2
		break
	else:
		print("<ONLY ACCEPT 1 or 2>")
		continue
		
filename = 'outfile_p3'
outfile = open(filename, 'w')

if decision == 1:
	res = UPGMA_tree.UPGMA(dm, raw_list)
	tree_data = res[0]
	length = res[1]
	root = buildTree(tree_data)
	print(" ",file=outfile)
	print(" ")
	print("<UPGMA TREE>")
	print("<UPGMA TREE>", file=outfile)
	print(tree_data)
	print(tree_data, file = outfile)
	print(" ")
	print(" ",file=outfile)
	print("<TREE TOPOLOGY>")
	print("<TREE TOPOLOGY>", file=outfile)
	printTree(root, None, False, outfile)
	print(" ")
	print(" ",file=outfile)
	print("<LENGTH OF EDGE>")
	print("<LENGTH OF EDGE>", file=outfile)
	print_length(tree_data, length,outfile)
	print(" ")
	print("<FILE:outfile_p3 CREATED>")
	print(" ")
	outfile.close()

else:
	res = Neighbor_tree.Neighbor(dm, raw_list)
	tree_data = res[0]
	length = res[1]
	print(" ")
	print(" ",file = outfile)
	print("<NEIGHBOR JOINING TREE>")
	print("<NEIGHBOR JOINING TREE>", file = outfile)
	print(tree_data)
	print(tree_data, file = outfile)
	print(" ")
	print(" ",file = outfile)
	print("<TREE TOPOLOGY>")
	print("<TREE TOPOLOGY>", file = outfile)
	small = None
	ind = 0
	for i in range(1, len(tree_data)):
		if isinstance(tree_data[i], str):
			small = tree_data[i]
			ind = 0
	if small == None:
		Min = len(tree_data[1])
		small = tree_data[1]
		for i in range(1, len(tree_data)):
			if len(tree_data[i]) < Min:
				Min = len(tree_data[i])
				small = tree_data[i]
				ind = i
	tree_data = tuple(i for i in tree_data if i != small)
	root = buildTree(tree_data)
	printTree(root, None, False, outfile)
	print("|")
	print("|", file = outfile)
	print("|")
	print("|", file = outfile)
	print("|")
	print("|", file = outfile)
	if isinstance(small, str):
		print("+---", small)
		print("+---", small, file = outfile)
	else:
		addition = buildTree(small)
		printTree(addition, None, False, outfile)
	print(" ")
	print(" ",file = outfile)
	print("<LENGTH OF EDGE>")
	print("<LENGTH OF EDGE>", file=outfile)
	for i in length:
		print(i, ":", length[i])
		print(i, ":", length[i], file=outfile)
	print(" ")
	print("<FILE:outfile_p3 CREATED>")
	print(" ")
	outfile.close()