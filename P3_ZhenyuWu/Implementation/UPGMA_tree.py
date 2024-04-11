
import numpy as np
import string

def UPGMA(dm, seq_list):
    val = 0
    height = 1
    attribute = 2

    def UPGMA_initialize(seq_list):
        res = []
        for seq in seq_list:
            res.append((seq, 0, "node"))
        return res

    def find_min(dm):
        res = ()
        Min_num = float('inf')
        for i in range(0, len(dm)):
            for j in range(0, len(dm[i])):
                if i == j:
                    continue
                if dm[i][j] < Min_num:
                    Min_num = dm[i][j]
                    res = (i,j,Min_num)
        return res

    def update_cluster(cluster, close_pair, tree, ancestor_counter, length):
        ind_1 = close_pair[0]
        ind_2 = close_pair[1]
        distance = close_pair[2]
        node_1 = cluster[ind_1]
        node_2 = cluster[ind_2]
        tree_node_1 = tree[ind_1]
        tree_node_2 = tree[ind_2]
        #update tree
        new_clu = (ancestor_counter, tree_node_1, tree_node_2)
        tree.pop(ind_1)
        tree.pop(ind_2-1)
        tree.append(new_clu)

        #update cluster
        new_attribute = ""
        if node_1[attribute] == 'node' and node_2[attribute] == 'node':
            new_attribute = "l1_cluster"
        if node_1[attribute] == 'l1_cluster' or node_2[attribute] == 'l1_cluster':
            new_attribute = 'l2_cluster'
        new_clu = (ancestor_counter, distance/2, new_attribute)
        cluster.pop(ind_1)
        cluster.pop(ind_2-1)
        cluster.append(new_clu)
            
    def extract_strings(tree):
        strings = []
        if isinstance(tree, str):
            strings.append(tree)
            return strings
       
        for element in tree:
            if isinstance(element, str):
                strings.append(element)
            elif isinstance(element, tuple):
                strings += extract_strings(element)
        return strings


        
    def update_dm(cluster, dm, close_pair,tree, node_dm, seq_list):
        ind_1 = close_pair[0]
        ind_2 = close_pair[1]
        #Delete row and column
        dm = np.delete(dm, ind_1, axis=0)
        dm = np.delete(dm, ind_2-1, axis=0)
        dm = np.delete(dm, ind_1, axis=1)
        dm = np.delete(dm, ind_2-1, axis=1)
        new_clu = cluster[-1]
        target = tree[-1]
        #for i in tree:
            #if i[0] == new_clu[val]:
                #target = i
                #break
        target_node_list = extract_strings(target)
        target_ind_list = []
        for i in target_node_list:
            target_ind_list.append(seq_list.index(i))
        #Start calculate the dm
        dm_list = []
        for i in tree:
            if i == target:
                dm_list.append(0)
                continue
            current_node = i
            current_node_list = extract_strings(current_node)
            current_ind_list = []
            for k in current_node_list:
                    current_ind_list.append(seq_list.index(k))
            res = []
            for target_ind in target_ind_list:
                    for current_ind in current_ind_list:
                        res.append(node_dm[target_ind,current_ind])
            dm_list.append(np.mean(res))
        #Reshape the matrix
        updated_dm = np.zeros((len(dm_list), len(dm_list)), dtype=float)
        updated_dm [:len(dm), :len(dm)] = dm
        updated_dm[-1,:] = dm_list
        updated_dm[:,-1] = dm_list
        return updated_dm

    def record_height(cluster, height_map):
        for i in cluster:
            if i[0] not in height_map.keys():
                height_map[i[0]] = i[height]
        
                

            



    
		
    node_dm = dm.copy()
    #seq_list = result = [string.ascii_uppercase[i] for i in range(len(raw_list))]
    upgma_tree = seq_list[:]
    cluster_list = UPGMA_initialize(seq_list)
    ancestor_counter = 1
    #print(cluster_list)
    height_map = {}
    record_height(cluster_list,height_map)


    while True:
        if len(cluster_list) <= 1:
            break
        close_pair = find_min(dm)
        #print(close_pair)
        update_cluster(cluster_list, close_pair, upgma_tree, ancestor_counter, height_map)
        ancestor_counter += 1
        #print(cluster_list)
        #print(upgma_tree)
        dm = update_dm(cluster_list, dm, close_pair,upgma_tree, node_dm, seq_list)
        #print(dm)

        record_height(cluster_list,height_map)
        #print(height_map)
    #print(cluster_list)
    #print(upgma_tree[0])

    return (upgma_tree[0], height_map)