import sys
import random

#Function to parse the input
def parse(raw_reads):
	res = []
	for i in range (0, len(raw_reads)):
		if(i % 2 != 0):
			res.append(raw_reads[i])
	for i in range(0 , len(res)):
		res[i] = res[i].replace("\n",'')
	return res
	
def max_length(l):
	max_l = -1
	for i in l:
		if len(i) > max_l:
			max_l = len(i)
	return max_l

def check_length(tb):
	sum = 0
	for i in tb:
		for j in tb[i]:
			sum += tb[i][j]
	print(sum)

def clear_same_contig(tb):
	output = []
	for i in tb:
		if i not in output:
			if not any(i in s for s in output):
				output.append(i)
	res = []
	for i in output:
		if i not in res:
			if not any(i in s and i != s for s in output):
				res.append(i)
	#for i in reversed(output):
		#if i not in res:
			#if not any(i in s for s in res):
				#res.append(i)
	return res
	
def clll(Tb):
	res = []
	tb = []
	for i in Tb:
		if i not in tb:
			tb.append(i)
	for i in tb:
		if i not in res:
			temp = [s for s in tb if s != i]
			sm = True
			for j in temp:
				if all(z in j for z in i):
					sm = False
			if sm:
				res.append(i)
		#print(len(res))
			
	return res

def clear_same_contig_mod(tb):
	output = []
	no_dup = list(set(tb))
	for i in no_dup:
		if i not in output:
			if not any(i in s and i != s for s in no_dup):
				output.append(i)
	
	return output				

#Function to join the path and cycle
def join_path_cycle(path, cycle):
	buck = {}
	for i in cycle:
		for j in range(0,len(path)):
			if i[0] in path[j]:
				buck[j] = path[j]
	key_l = list(buck.keys())
	val_l = clll(list(buck.values()))
	clean_buck = {}
	waste_buck = []
	for val in val_l:
		for key in key_l:
			target = buck[key]
			if target not in list(clean_buck.values()):
				if target == val:
					clean_buck[key] = val
				else:
					waste_buck.append(key)
			else:
				waste_buck.append(key)
	#print(clean_buck)
	for i in cycle:
		for j in clean_buck:
			p = clean_buck[j]
			if i[0] in p:
				sub1 = p[:p.index(i[0])]
				sub2 = p[p.index(i[0])+1:]
				res = sub1+i+sub2
				path[j] = res
				break
	for i in waste_buck:
		path.pop(i)
	
	
	


#Function to find overlap between two stings with given length
def overlap(str1, str2, length):
	res = []
	section_str1 = []
	section_str2 = []
	if(length > len(str1) or length > len(str2)):
			print("Exceed length of input array")
			return []
	#Cut the str1 into multiple sction of equal length
	for i in range(0 , len(str1)):
		piece = str1[i:len(str1)]
		if(len(piece) < length):
			break
		else:
			section_str1.append(str1[i:i+length])
		
	#Cut the str2 into multiple section of equal lenght
	for i in range(0 , len(str2)):
		piece = str2[i:len(str2)]
		if(len(piece) < length):
			break
		else:
			section_str2.append(str2[i:i+length])
	#Compare both
	if len(section_str1) > len(section_str2):
		for i in section_str1:
			for j in section_str2:
				if(i == j):
					if i not in res:
						res.append(i)
	else:
		for i in section_str2:
			for j in section_str1:
				if(i == j):
					if i not in res:
						res.append(i)
	
	return res

#Function to bind the overlaping contigs
def bind(str1, str2):
	counter = 1
	res =[]
	while True:
		if counter > len(str1) or counter > len(str2):
			break
		if str1[:counter] == str2[-counter:]:
			res.append(str1[:counter])
		elif str1[-counter:] == str2[:counter]:
			res.append(str1[-counter:])
		counter += 1
	filte = [i for i in res if len(i) >= 15]
	#print(filte)
	#filte = res
	Res = ''
	max_len = -1
	for i in filte:
		if len(i) > max_len:
			max_len = len(i)
			Res = i
	#print(Res)	
	return Res
	
	

#Funtion to hash the prefix or suffix into an integer
def hash_in(str_in):
	res = 0
	for i in range(0, len(str_in)):
	    temp = pow(4,i)
	    if(str_in[i] == 'A'):
	        temp = temp * 0
	    elif str_in[i] == 'C':
	        temp = temp * 1
	    elif str_in[i] == 'G':
	        temp = temp * 2
	    elif str_in[i] == 'T':
	        temp = temp * 3
	    res += temp
	return res
		
		
#Function to hash the integer back to the prefix or suffix
def hash_back(int_in):
	Res = ""
	for i in range(14, -1, -1):
	    temp = int(int_in/pow(4,i))
	    if temp == 0:
	        Res += "A"
	    elif temp == 1:
	        Res += 'C'
	    elif temp == 2:
	        Res += 'G'
	    elif temp == 3:
	        Res += 'T'
	    int_in -= temp*pow(4,i)
	return Res[::-1]

	
#Function to put prefix and suffix into a hash table
def hash_table(pre, suf):
	res = {}
	for i in range(0, len(pre)):
		if pre[i] in res:
			if suf[i] in res[pre[i]]:
				res[pre[i]][suf[i]] += 1
			else:
				res[pre[i]].update({suf[i]:1})
		else:
			res[pre[i]] = {suf[i]:1}
	return res	

#Function to find the outdegree or indegree of the node
def find_Degree(arr):
	res = {}
	for node in arr:
		if node in res:
			res[node] += 1
		else:
			res[node] = 1
	return res


#Function to read the path from a node with larger outdegree
def read_path(p, key, out_degree, in_degree):
    # Find the starting node of the path
    start_node = key

    contigs = []
    current_node = start_node
    contigs.append(current_node)
    counter = 1
    while True:
        next_node = None
        if not p.get(current_node):
        	break
        for i in p[current_node]:
            if p[current_node][i] > 0:
                next_node = i
                break
        if next_node is None:
        		#contigs.append(current_node)
        		break
        #if current_node in out_degree:
            #if out_degree[current_node] > 0:
            	#out_degree[current_node] -= 1
        # Add the current node and the next node to the list of contigs
        #contigs.append(current_node)
        #contigs.append(next_node)

        # Mark the edge as visited and update the degrees
        p[current_node][next_node] -= 1
        if p[current_node][next_node] == 0:
            p[current_node].pop(next_node)
        current_node = next_node
        contigs.append(current_node)
        if current_node in in_degree:
        		if in_degree[current_node] > 0:
        			in_degree[current_node] -= 1
        counter +=1
    #print("YES",contigs)
    return contigs


#Function to clean the hash table
def clean_hash(hash_tb):
	non_dup = list(set(hash_tb))
	return non_dup
   
#Function to read the hash table
def read_hash(hash_tb,out_de,in_de):
	path = []
	cycle = []
	for key in hash_tb:
		while True:
			out_degree = sum(hash_tb[key].values())		
			#if key in out_de:
				#out_degree = out_de[key]
			in_degree = 0
			if key in in_de:
				in_degree = in_de[key]
			if out_degree > in_degree:
				path.append(read_path(hash_tb,key, out_de, in_de))
			if out_degree <= in_degree:
				break
	# x = clean_hash(hash_tb)
	
	for key in hash_tb:
		if len(hash_tb[key]) == 0:
			continue
		cycle.append(read_path(hash_tb,key, out_de, in_de))
	return {"path":path, "cycle":cycle}

def assemble_in_res(pivot, tb):
	#use_count = []
	for i in range(0, len(tb)):
		if pivot in tb[i] or tb[i] in pivot:
			if pivot in tb[i]:
				pivot = tb[i]
			#if i not in use_count:
				#use_count.append(i)
			tb[i] = ''
			continue
		share_region = bind(pivot, tb[i])
		if share_region != '':
			if share_region == pivot[:len(share_region)]:
				pivot = tb[i][0:(len(tb[i])-len(share_region))] + pivot
			elif share_region == pivot[(-len(share_region)):]:
				pivot = pivot[0:(len(pivot)-len(share_region))] + tb[i]
			#if i not in use_count:
				#use_count.append(i)
			#return pivot
			tb[i] = ''		
	#print(pivot)
	return pivot

def assemble_in_tb_mod(pivot, tb,res):
	region = {}
	max_index = 0
	max_length = 0
	for i in range(0, len(tb)):
		if pivot in tb[i] or tb[i] in pivot:
			if pivot in tb[i]:
				pivot = tb[i]
			#if i not in use_count:
				#use_count.append(i)
			tb[i] = ''
			continue
		share_region = bind(pivot, tb[i])
		if share_region != '':
			if len(share_region) > max_length:
				max_length = len(share_region)
				max_index = i
			region[i] = share_region
	if len(region) != 0:
		overlap_r = region[max_index]
		if overlap_r == pivot[:len(overlap_r)]:
			pivot = tb[max_index][0:(len(tb[max_index])-len(overlap_r))] + pivot
		elif overlap_r == pivot[(-len(overlap_r)):]:
			pivot = pivot[0:(len(pivot)-len(overlap_r))] + tb[max_index]
		tb[max_index] = ''	
	#print(pivot)
	pivot = assemble_in_res(pivot,res)
	return pivot

def assemble_in_tb(pivot, tb,res):
	#use_count = []
	for i in range(0, len(tb)):
		if pivot in tb[i] or tb[i] in pivot:
			if pivot in tb[i]:
				pivot = tb[i]
			#if i not in use_count:
				#use_count.append(i)
			tb[i] = ''
			continue
		share_region = bind(pivot, tb[i])
		if share_region != '':
			if share_region == pivot[:len(share_region)]:
				pivot = tb[i][0:(len(tb[i])-len(share_region))] + pivot
			elif share_region == pivot[(-len(share_region)):]:
				pivot = pivot[0:(len(pivot)-len(share_region))] + tb[i]
			#if i not in use_count:
				#use_count.append(i)
			#return pivot
			tb[i] = ''
	#print(pivot)
	return pivot
	
def glue(hash_tb):
	res = []
	while len(hash_tb) != 0:
		pivot = hash_tb[0]
		old_pivot = ''
		use_count = []
		while True:
			old_pivot = pivot
			#another function is assemble_in_tb_mod
			output = assemble_in_tb(pivot,hash_tb,res)
			hash_tb = [x for x in hash_tb if x != '']
			res = [x for x in res if x != ""]
			pivot = output
			#print(pivot)
			#for i in output[1]:
				#use_count.append(i)
			if old_pivot == pivot:
				break
			if pivot == '':
				break
		if pivot != '':
			res.append(pivot)
		#for i in use_count:
			#hash_tb[i] = ""
		#hash_tb = [x for x in hash_tb if x != ""]
		#for i in use_count:
			#hash_tb[i] = ''
		#hash_tb = [x for x in hash_tb if x != '']
		#res = clear_same_contig(res)
	return res
				

filename = sys.argv[1]	
file = open(filename)
raw_reads = file.readlines()
file.close()

#Read fasta file into a list of Reads
reads = parse(raw_reads)

#Break Reads into two lists: prefix and suffix
prefix = []
suffix = []
half = int(len(reads[0])/2)
for element in reads:
	prefix.append(element[0:half])
	suffix.append(element[half:len(element)])
 

#Hash the prefix and suffix into hash number
hashed_prefix = []
hashed_suffix = []
for i in prefix:
	hashed_prefix.append(hash_in(i))
for i in suffix:
	hashed_suffix.append(hash_in(i))
#find the outdegree of the node
out_degree = find_Degree(hashed_prefix)

#find the indegree of the node
in_degree = find_Degree(hashed_suffix)

#Implement hash table
hash_tb = hash_table(hashed_prefix, hashed_suffix)

print('<READING FROM HASH TB>')
contigs = read_hash(hash_tb,out_degree, in_degree)
path = contigs['path']
cycle = contigs['cycle']
print("<DONE>")
#print(len(path))
#print(len(reads))
#print(max_length(path))
print("<BINDING PATH & CYCLE>")
#join the path and cycle
#path = clll(path)
join_path_cycle(path,cycle)
print("<DONE>")
print("<DECODING NODE>")
#hash back the encoded contigs
real_path = []
for arr in path:
	temp = ""
	for node in arr:
		temp += hash_back(node)
	real_path.append(temp)
print("<DONE>")
#print(real_path)
#print(real_path)
print("<CLEANING DUPLICATED CONTIGS>")
##################################################################################################

#cleared_path = clear_same_contig(real_path)
cleared_path = clear_same_contig(real_path)
#cleared_path_mod = clear_same_contig_mod(real_path)
print("<DONE>")
#print(len(real_path))
print("<BINDING OVERLAPING CONTIGS>")
RRR = glue(cleared_path)
print("<DONE>")
#print(RRR)
#print(len(RRR[0]))
#print(len(clear_same_contig(RRR)))

print("<EXPORTING FILE>")
o_file = f"Output_{random.randint(1, 100000)}.fasta"
file = open(o_file, "w")

for i in range(len(RRR)):
    file.write(">" + "contig"+ str(i+1) + '|' + 'size' + str(len(RRR[i])) + "\n" + RRR[i] + "\n")


file.close()
print("<DONE>")
print("PlEASE CHECK CURRENT FOLDER")
