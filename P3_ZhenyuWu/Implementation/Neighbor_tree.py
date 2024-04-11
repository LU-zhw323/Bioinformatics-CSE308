import numpy as np

def Neighbor(dm, seq_list):
	def leg_weight(dm, seq_list):
	    res = {}
	    N = len(dm)-2
	    for i in range (0, len(dm)):
	        weight = 0
	        for j in range(0, len(dm[i])):
	            if i == j:
	                continue
	            weight += dm[i][j]
	        weight = weight/N
	        res[seq_list[i]] = weight
	    return res


	def find_Min(dm, leg, seq):
	    Min = float('inf')
	    ind_1 = 0
	    ind_2 = 0
	    for i in range(0, len(dm)):
	        for j in range(0, len(dm[i])):
	            if i == j:
	                continue
	            node_1 = seq[i]
	            node_2 = seq[j]
	            val = dm[i][j] - leg[node_1] - leg[node_2]
	            if val < Min:
	                Min = val
	                ind_1 = i
	                ind_2 = j
	    return (Min, ind_1, ind_2)


	def update_seq(neighbor, seq_list, tree, ancestor_counter):
	    ind_1 = neighbor[1]
	    ind_2 = neighbor[2]
	    node_1 = tree[ind_1+1]
	    node_2 = tree[ind_2+1]
	    new_clu = (ancestor_counter, node_1, node_2)
	    seq_list.pop(ind_1)
	    seq_list.pop(ind_2-1)
	    tree.pop(ind_1+1)
	    tree.pop(ind_2+1-1)
	    seq_list.append(ancestor_counter)
	    tree.append(new_clu)

	def record_height(seq,neighbor,dm, leg, ancestor_counter, map):
	    ind_1 = neighbor[1]
	    ind_2 = neighbor[2]
	    distance = dm[ind_1][ind_2]
	    leg_1 = leg[seq[ind_1]]
	    leg_2 = leg[seq[ind_2]]
	    val1 = distance/2 + (leg_1-leg_2)/2
	    val2 = distance/2 + (leg_2-leg_1)/2
	    str_1 = str(ancestor_counter) +" to " + str(seq[ind_1])
	    str_2 = str(ancestor_counter) + " to " + str(seq[ind_2])
	    map[str_1] = val1
	    map[str_2] = val2


	def update_dm(neighbor, dm):
	    ind_1 = neighbor[1]
	    ind_2 = neighbor[2]
	    new_dis = []
	    for i in range(0, len(dm)):
	        if i == ind_1 or i == ind_2:
	            continue
	        dis_1 = dm[ind_1][i]
	        dis_2 = dm[ind_2][i]
	        dis = dm[ind_1][ind_2]
	        val = (dis_1+dis_2-dis)/2
	        new_dis.append(val)
	    new_dis.append(0)     
	    dm = np.delete(dm, ind_1, axis=0)
	    dm = np.delete(dm, ind_2-1, axis=0)
	    dm = np.delete(dm, ind_1, axis=1)
	    dm = np.delete(dm, ind_2-1, axis=1)
	    updated_dm = np.zeros((len(new_dis), len(new_dis)), dtype=float)
	    updated_dm [:len(dm), :len(dm)] = dm
	    updated_dm[-1,:] = new_dis
	    updated_dm[:,-1] = new_dis
	    return updated_dm





	
	#ÔÚseqÀï¸úÐÂseq list
	tree = seq_list[:]
	tree.insert(0,"U")
	ancestor_counter = 1
	node_dm = dm.copy()
	height_map = {}



	while True:
	    if len(dm) == 2:
	    		ancestor_counter -= 1
	    		break
	    U_weight = leg_weight(dm, seq_list)
	    #print(U_weight)
	    pair = find_Min(dm,U_weight, seq_list)
	    #print(pair)
	    record_height(seq_list,pair,dm, U_weight, ancestor_counter, height_map)
	    #print(height_map)
	    update_seq(pair, seq_list, tree, ancestor_counter)
	    #print(seq_list)
	    #print(tree)
	    ancestor_counter += 1
	    dm = update_dm(pair, dm)
	root = ancestor_counter
	root_ind = seq_list.index(root)
	last_node = [x for x in seq_list if x != root][0]
	last_ind = seq_list.index(last_node)
	str_fin = str(root) + ' to ' + str(last_node)
	height_map[str_fin] = dm[root_ind][last_ind]
	
	last_tree = ()
	root_tree = ()
	for i in tree:
		if root == i[0]:
			root_tree = i
		elif last_node == i[0]:
			last_tree = i
	root_tree += (last_tree, )
	return(root_tree, height_map)