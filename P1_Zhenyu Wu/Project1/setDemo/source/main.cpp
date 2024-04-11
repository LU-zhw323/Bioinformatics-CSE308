////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////
//Example code for CSE 350/450, by Brian Y. Chen, 2010.
// --- Not to be used outside of CSE 350/450 without permission.
////////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////

#include "StdAfx.h"





//this demonstrates the set_t library that ou can use for universal hashing.
//it is very fast and effective.  I use this in my own code.
void set_demo()
{
	int i = 0;
	
	//instantiate a simple set (just a bag of nonredundant ints)
	printf("\ninstantiate a simple set (just a bag of nonredundant ints\n");
	set_t set1 = alloc_set(0);

	//we can store integers in it
	printf("\nwe can store integers in it\n");
	set1 = put_set(set1, 23);		printf("inserted: 23\n");
	set1 = put_set(set1, 24);		printf("inserted: 24\n");
	set1 = put_set(set1, 25);		printf("inserted: 25\n");
	set1 = put_set(set1, 26);		printf("inserted: 26\n");

	/////VERY IMPORTANT//////////////
	//*note that you must set set1 equal to the output of put_set, because the set is sometimes
	//*resized and reallocated.  For simplicity this is not done for you, so you must do this.
	//IF you do not, automatic reallocation will create serious errors!
	/////VERY IMPORTANT//////////////

	//now we can get the integers out as if it was an array:
	printf("\nnow we can get the integers out as an array\n");
	int myInt = set1[0];			printf("the 0th position in set1 is: %i\n", myInt);
	    myInt = set1[1];			printf("the 1th position in set1 is: %i\n", myInt);
	    myInt = set1[2];			printf("the 2th position in set1 is: %i\n", myInt);
	    myInt = set1[3];			printf("the 3th position in set1 is: %i\n", myInt);

	//you can also get teh size
	printf("\nWe can also tell how large a set is:\n");
	int mySize = size_set(set1);
	printf("size of the set: %i\n", mySize);

	///MOst importantly, we can tell if an integer is contained in the set in constant time:
	printf("\nWE can tell if an integer is contained in the set in constant time\n");
	printf("Lets see if the number 4 is in the set\n");
	if( contains_set(set1, 4) ){
		printf("Yup, 4 is contained in the set\n");
	}
	else{
		printf("nope, 4 is not contained in the set\n");
	}
	printf("Lets see if the number 23 is in the set\n");
	if( contains_set(set1, 23) ){
		printf("Yup, 23 is contained in the set\n");
	}
	else{
		printf("nope, 23 is not contained in the set\n");
	}
	printf("We can also see if first element in the set (%i), is in the set\n", set1[0]);
	if( contains_set(set1, set1[0]) ){
		printf("Yup, %i is contained in the set\n", set1[0]);
	}
	else{
		printf("nope, %i is not contained in the set\n", set1[0]);
	}
	
	///Finally, we can remove elements from the set:
	printf("\nWe can also remove something from a set.  Lets remove 23:\n");
	remove_set(set1, 23);
	printf("Lets see if the number 23 is in the set\n");
	if( contains_set(set1, 23) ){
		printf("Yup, 23 is contained in the set\n");
	}
	else{
		printf("nope, 23 is not contained in the set\n");
	}

	//de-allocate a simple set
	printf("\nThis is how we de-allocate a set\n");
	free_set(set1);
	
	//instantiate a set that points at objects.
	printf("\nYou can also instantiate a set that points at objects and other sets (e.g. pointers)\n");
	set_t mySet = alloc_set(SP_MAP);

	//make a bunch of PDB atoms that we will store.  pretend they are filled with data.
	printf("\nSo as an example, lets store sets inside a set.  You could nest sets arbitrarily deeply\n");
	printf("make a bunch of sets that we will store.  pretend they are filled with data.\n");
	printf("Lets make set 1 with integers 10, 11, 12, 13\n");
	set_t innerset1 = alloc_set(0);
		innerset1 = put_set(innerset1, 10);
		innerset1 = put_set(innerset1, 11);
		innerset1 = put_set(innerset1, 12);
		innerset1 = put_set(innerset1, 13);
	printf("Lets make set 2 with integers 20, 21, 22, 23\n");
	set_t innerset2 = alloc_set(0);
		innerset2 = put_set(innerset2, 20);
		innerset2 = put_set(innerset2, 21);
		innerset2 = put_set(innerset2, 22);
		innerset2 = put_set(innerset2, 23);
	printf("Lets make set 3 with integers 30, 31, 32, 33\n");
	set_t innerset3 = alloc_set(0);
		innerset3 = put_set(innerset3, 30);
		innerset3 = put_set(innerset3, 31);
		innerset3 = put_set(innerset3, 32);
		innerset3 = put_set(innerset3, 33);
	printf("Lets make set 4 with integers 40, 41, 42, 43\n");
	set_t innerset4 = alloc_set(0);
		innerset4 = put_set(innerset4, 40);
		innerset4 = put_set(innerset4, 41);
		innerset4 = put_set(innerset4, 42);
		innerset4 = put_set(innerset4, 43);

	//now we can put them with hashing indicies into the set: indices 100, 101, 102, 103
	printf("\nnow we can insert them into set with hashing indicies: 100, 101, 102, 103\n");
	mySet = associate_set(mySet, 100, innerset1);
	mySet = associate_set(mySet, 101, innerset2);
	mySet = associate_set(mySet, 102, innerset3);
	mySet = associate_set(mySet, 103, innerset4);

	/////VERY IMPORTANT//////////////
	//*note that you must set mySet equal to the output of associate_set, because the set is sometimes
	//*resized and reallocated.  For simplicity this is not done for you, so you must do this.
	//IF you do not, automatic reallocation will create serious errors!
	/////VERY IMPORTANT//////////////

	//now we can get these objects back out in expected constant time by the hashing index:
	printf("now we can get these objects back out in expected constant time by the hashing index:\n");
	printf("Lets pull the set out for index 100:\n");
	set_t tempInnerSet = (set_t) mapsto_set(mySet, 100);
	printf("Lets see what's inside the set indexed at 100:\n");
	for(i = 0; i<size_set(tempInnerSet); i++){
		printf("tempInnerSet[%i]: %i\n", i, tempInnerSet[i]);
	}

	//you can also get these objects out by their position in the matrix by using the index:
	printf("\nyou can also get these objects out by their position in the matrix by using the index: %i\n", 1);
	set_t thisSet = (set_t) mapsto_set(mySet, mySet[1]);
	printf("Lets see what's inside set at index %i\n", 1);
	for(i = 0; i<size_set(thisSet); i++){
		printf("%i\n", thisSet[i]);
	}


	///note that set_t is a pointer, so if you had an object pointer (Object *) 
	///stored in the set, then you would write:
	//Object thisSet = (Object *) mapsto_set(mySet, mySet[1]);

	///MEMORY MANAGEMENT:
	///now we can clear up the data in this set, then the data itself
	printf("\nnow we can clear up the data in this set, then the data itself\n");
	for(i = 0; i<size_set(mySet); i++){
		printf("Clearing up the set in position %i, with index %i\n", i, mySet[i]);
		//note that this is deleting the sets, but NOT TELLING the 
		//the set structure that they are deleted.  So do not go and use the
		//set structure after you delete its contents like this.
		set_t tempInnerSet = (set_t) mapsto_set(mySet, mySet[1]);
		free_set(tempInnerSet);
	}
	//after freeing the contents, free the set, to avoid hanging pointers.
	printf("after freeing the contents, free the set, to avoid hanging pointers.\n");
	free_set(mySet);

	printf("\nsets maintain nonredundant indices.  You can use this fact to generate nonredundant lists.\n");
	printf("If you insert the same integer into a simple set, then there will only be one in the set\n");

}




//////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////
//                                                                                                  //                      
//  ###   ###    ###    ######  ##   ##      ###   ###  #######  ######  ##   ##   #####   #####    //                                                                                
//  #### ####   ## ##     ##    ###  ##      #### ####  ##         ##    ##   ##  ##   ##  ##  ##   //                                                                                                            
//  ## ### ##  ##   ##    ##    #### ##      ## ### ##  ######     ##    #######  ##   ##  ##   ##  //                                                                                                              
//  ##  #  ##  #######    ##    ## ####      ##  #  ##  ##         ##    ##   ##  ##   ##  ##   ##  //                                                                  
//  ##     ##  ##   ##    ##    ##  ###      ##     ##  ##         ##    ##   ##  ##   ##  ##  ##   //                                                            
//  ##     ##  ##   ##  ######  ##   ##      ##     ##  #######    ##    ##   ##   #####   #####    //                                                                         
//                                                                                                  //                      
//////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////////////////////////////
int main(int argc, char* argv[])
{
	
	if(argc == 1){
		printf("#####################################################################################\n");
		printf("###COURSE CODE DEVELOPED FOR CSE308/408 at LEHIGH UNIVERSITY, by BRIAN CHEN, 2011.###\n");
		printf("###    NOT TO BE USED OUTSIDE OF CSE 308/408 FOR ANY REASON WITHOUT PERMISSION    ###\n");
		printf("#####################################################################################\n");
		printf("to see the set demo, type example -set\n");
		exit(1);
	}

	if(argc == 2){
		if( strcmp(argv[1], "-set")==0 ){
			//this demonstrates the set_t library that ou can use for universal hashing.
			//it is very fast and effective.  I use this in my own code.
			set_demo();
			exit(1);
		}

		printf("incorrect input.  exitting\n");
		exit(1);
	}

	else{
		printf("incorrect input.  exitting\n");
		exit(1);
	}

	return 1;

}
