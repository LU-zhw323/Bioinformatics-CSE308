

<SOURCE CODE>
1. UPGMA_tree.py:       codes for UPGMA tree
2. Neighbor_tree.py:    codes for Neighbor-joining tree
3. tree.py:             codes generate the tree, just need to run this one

<HOW TO RUN>(in current directory)
1. Parse ClustalW stdout:
	./clustalw2 test.fasta -type=protein > clustalw.output
2. Parse Distance Matrix:
	python clustal2Matrix.py clustalw.output matrix
3. Run the code:
	python tree.py

<DETAIL about tree.py>
1. Press 1 for UPGAM tree, 2 for Neighbor-joining tree
2. It will read "matrix" file, the output of clustal2Matrix.py
3. It will print out the result
4. It will output result into "outfile_p3" in current directory as well
5. Components of output: tree(tuple format), tree topology, length of edges



