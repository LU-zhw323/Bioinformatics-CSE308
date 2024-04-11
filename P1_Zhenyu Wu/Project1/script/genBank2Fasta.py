import sys
import getopt
import string
import os
import re
import glob
import random
from random import shuffle
from string import upper

###########################################################################
### Credit
###########################################################################
def credit():
	print "genBank2Fasta script, by Brian Chen, Lehigh University, 2011."




###########################################################################
### Usage
###########################################################################
def usage():
	credit();
	print("========================================================="   );
	print(""                                                          );
	print("python genBank2Fasta.py"        );
	print("   Running with no input returns this usage info."  );
	print(""                                                          );
	print("python genBank2Fasta.py -genome [genBankFile] [fastaOutput]"       );
	print("   Transforms [genBankFile], in genBank format, into a single"  );
	print("   FASTA entry and outputs to a new file called [fastaOutput]"  );
	print("");
	print("python genBank2Fasta.py -reads [genBankFile] [readLength] [xCoverage] [minOverlap] [maxOverlap] [fastaOutput] [answerKey]" );
	print("   Takes Genome in [genBankFile] and breaks it into reads of length"  );
	print("   [readLength], with coverage at least [xCoverage] (integer) throughout, and"  );
	print("   outputs a fasta format to [fastaOutput].  Reads will overlap between [minOverlap] and"  );
	print("   [maxOverlap] (integer) nucleotides. [answerKey] outputs the reads in the correct");
	print("   order, as well as the whole genome");
	print("");
	print("python genBank2Fasta.py -randomizeFasta [outputFasta] [answerKey] [inputRead(s)]" );
	print("   Takes reads in the (possibly multiple) files [inputReads(s), which can be"  );
	print("   defined using wildcards.  Jumbles the reads up and outputs the reads into"  );
	print("   [outputFasta] without labeled headers.  Headers labeled in inputReads are"  );
	print("   preserved in [answerKey], which is jumbled the same way as [outputFasta].");
	print("   Does not change read lengths.");
	print("");
	print("python genBank2Fasta.py -denseReads [genBankFile] [outputFasta] [readLength] [minReadsPerNucleotide] [maxReadsPerNucleotide] [answerKey]" );
	print("   Takes Genome in [genBankFile] generates reads starting at every or nearly every"  );
	print("   nucleotide.  This is to simulate high throughput sequencing outputs that have "  );
	print("   50-100x coverage or more."  );
	print("   Answer Key indicates the starting index of every read."  );
	print("");
	print("========================================================="   );


###########################################################################
###########################################################################
### output genome as fasta
### print("python genBank2Fasta.py -genome [genBankFile] [fastaOutput]"       );
###########################################################################
###########################################################################
def getGenome( genBankFile, fastaOutput ):

	###open the input file
	gbFile = open(genBankFile, 'rt');
	line = gbFile.readline()

	###open the output file
	fOutput = open(fastaOutput, 'w');
	fOutput.write("> " + fastaOutput +"\n");

	###skip out to the ORIGIN line	
	while line:
		if ( not (line.startswith("ORIGIN") ) ):
			line = gbFile.readline();
			continue;
		else:
			break;

	###skip the ORIGIN line also
	line = gbFile.readline();

	###now parse out the sequences.
	while line:
		if ( line.startswith("//") ):
			break;		

		wordList = line.split();
		outputLine = ''.join(wordList[1::]) + "\n";
		fOutput.write(upper(outputLine));

		line = gbFile.readline();

	##close files
	gbFile.close();
	fOutput.close();




###########################################################################
###########################################################################
### Parse the genBank file and output reads.
### print("python genBank2Fasta.py -reads [genBankFile] [readLength] [xCoverage] [minOverlap] [maxOverlap] [fastaOutput] [answerKey]" );
###########################################################################
###########################################################################
def getReads( genBankFile, readLength, xCoverage, minOlap, maxOlap, fastaOutput, answerKey ):
	###open the input file
	gbFile = open(genBankFile, 'rt');
	line = gbFile.readline()

	###open the output file
	fOutput = open(fastaOutput, 'w');
	
	###open the answerKey file
	key = open(answerKey, 'w');

	##parse the readLength and xCoverage
	rLength = int(readLength);
	xCover  = int(xCoverage);
	minO = int(minOlap);
	maxO = int(maxOlap);

	if (rLength < (maxO-1)):
		printf("ERROR: read length is less than maxoverlap-1\n");
		return;

	###skip out to the ORIGIN line	
	while line:
		if ( not (line.startswith("ORIGIN") ) ):
			line = gbFile.readline();
			continue;
		else:
			break;

	###skip the ORIGIN line also
	line = gbFile.readline();
	
	###wholeGenomePointer
	genome = '';

	###now parse out the genome into a single long string.
	while line:
		if ( line.startswith("//") ):
			break;		

		wordList = line.split();
		genomeLine = ''.join(wordList[1::]);
		genome = genome + genomeLine;

		line = gbFile.readline();

	##make the genome uppercase
	genome = upper(genome);

	##get the number of bases
	genomeLength = len(genome);

	readsList = [];
	keyList = [];

	currentRead = 0;
	###now generate the reads
	for i in range(xCover):
		nextStartingPosition = 0 + random.randint(minO, maxO);
		while( nextStartingPosition + rLength < genomeLength ):
			readsList.insert( len(readsList), str(currentRead) +" "+ genome[nextStartingPosition:nextStartingPosition+rLength] );
			keyList.insert( len(keyList), str(currentRead) +" "+ genome[nextStartingPosition:nextStartingPosition+rLength] );
			nextStartingPosition = nextStartingPosition + rLength - random.randint(minO, maxO);
			currentRead = currentRead+1;
	
	###problem: this currently outputs the reads in sequential order.  too easy.
	shuffle(readsList);

	###now output the reads
	for i in range( len(readsList) ):
		fOutput.write("> " + fastaOutput + "\n");
		fOutput.write( readsList[i].split()[1] + "\n" );

	###now output the answerKey
	key.write("########################################################\n");
	key.write("## READS IN SHUFFLED ORDER #############################\n");
	key.write("########################################################\n");

	for i in range( len(readsList) ):
		key.write("> " + fastaOutput + " Read: " + readsList[i].split()[0] + "\n");
		key.write( readsList[i].split()[1] + "\n" );
		
	key.write("########################################################\n");
	key.write("## READS IN UNSHUFFLED ORDER ###########################\n");
	key.write("########################################################\n");

	for i in range( len(keyList) ):
		key.write("> " + fastaOutput + " Read: " + keyList[i].split()[0] + "\n");
		key.write( keyList[i].split()[1] + "\n" );

	key.write("########################################################\n");
	key.write("## FULL ORIGINAL GENOME SEQUENCE #######################\n");
	key.write("########################################################\n");

	key.write("> Full Original Genome\n");
	genomeMarker = 0;
	while( genomeMarker < len(genome) ):
		if( genomeMarker+80 < len(genome) ):
			key.write( genome[genomeMarker:genomeMarker+80] + "\n");
			genomeMarker = genomeMarker+80;
		else:
			key.write( genome[genomeMarker::] + "\n");
			break;

	##close files
	key.close();
	gbFile.close();
	fOutput.close();
	



###########################################################################
########################################################################### 
### File gobble
###########################################################################
###########################################################################
def gobble(fileName):                                                     
        #print("Gobbling: "+ fileName);
        
        inputFile = open(fileName, 'rt'); 
        inputLine = inputFile.readline();
        
        outputList = "".split();  #### list declaration
        
        while inputLine: 
                outputList.append(inputLine);
                inputLine = inputFile.readline();
        
        inputFile.close(); 
        
#       for l in outputList:
#               print l;
        
        return outputList;
        

###########################################################################
###########################################################################
### Parse the genBank file and output reads.
### print("python genBank2Fasta.py -randomizeFasta [outputFasta] [answerKey] [inputRead(s)]" );
###########################################################################
###########################################################################
def randomizeFastas( outputFasta, answerKey, fastaList ):
	readList = [];
	
	for fileName in fastaList:
		fFileLineList = gobble(fileName);
		tempList = [];

		tempList.append(fFileLineList[0]);
		for line in fFileLineList[1::]:
			if( line.startswith(">")):
				readList.append(tempList);
				tempList = [];
				tempList.append(line);
				continue;
			else:
				tempList.append(line);

		readList.append(tempList);
		
	shuffle(readList);

	###open the output file
	fOutput = open(outputFasta, 'w');
	###open the answerKey file
	key = open(answerKey, 'w');
	
	for lineSet in readList:
		fOutput.write("> \n");
		key.write(lineSet[0]);

		for line in lineSet[1::]:
			fOutput.write(line);
			key.write(line);
			
	##close files
	key.close();
	fOutput.close();





###########################################################################
###########################################################################
### DenseReads
###########################################################################
###########################################################################
##print("python genBank2Fasta.py -denseReads [genBankFile] [outputFasta] [readLength] [minReadsPerNucleotide] [maxReadsPerNucleotide] [answerKey]" );
def denseReadsFasta( genBankFile, fastaOutput, readLength, minReadsPerNuc, maxReadsPerNuc, answerKey ):
	###open the input file
	gbFile = open(genBankFile, 'rt');
	line = gbFile.readline()

	###open the output file
	fOutput = open(fastaOutput, 'w');
	
	###open the answerKey file
	key = open(answerKey, 'w');

	##parse the min max reads per nucleotide
	rLength = int(readLength);
	minR = int(minReadsPerNuc);
	maxR = int(maxReadsPerNuc);

	###skip out to the ORIGIN line	
	while line:
		if ( not (line.startswith("ORIGIN") ) ):
			line = gbFile.readline();
			continue;
		else:
			break;

	###skip the ORIGIN line also
	line = gbFile.readline();
	
	###wholeGenomePointer
	genome = '';

	###now parse out the genome into a single long string.
	while line:
		if ( line.startswith("//") ):
			break;		

		wordList = line.split();
		genomeLine = ''.join(wordList[1::]);
		genome = genome + genomeLine;

		line = gbFile.readline();

	##make the genome uppercase
	genome = upper(genome);

	##get the number of bases
	genomeLength = len(genome);

	readsList = [];
	keyList = [];

	currentRead = 0;
	###now generate the reads
	for i in range(genomeLength-rLength):
		for j in range(random.randint(minR, maxR) ):
			readsList.insert( len(readsList), str(i) +" "+ genome[i:i+rLength] );
			keyList.insert( len(keyList), str(i) +" "+ genome[i:i+rLength] );
			##print( genome[i:i+rLength] + "\n" );
			j = j+1;
		i = i+1;
	
	###problem: this currently outputs the reads in sequential order.  too easy.
	shuffle(readsList);

	###now output the reads
	for i in range( len(readsList) ):
		fOutput.write("> " + fastaOutput + "\n");
		fOutput.write( readsList[i].split()[1] + "\n" );

	###now output the answerKey
	key.write("########################################################\n");
	key.write("## READS IN SHUFFLED ORDER #############################\n");
	key.write("########################################################\n");

	for i in range( len(readsList) ):
		key.write("> " + fastaOutput + " Read starting at Nucleotide " + readsList[i].split()[0] + "\n");
		key.write( readsList[i].split()[1] + "\n" );
		
	key.write("########################################################\n");
	key.write("## READS IN UNSHUFFLED ORDER ###########################\n");
	key.write("########################################################\n");

	for i in range( len(keyList) ):
		key.write("> " + fastaOutput + " Read starting at Nucleotide: " + keyList[i].split()[0] + "\n");
		key.write( keyList[i].split()[1] + "\n" );

	key.write("########################################################\n");
	key.write("## FULL ORIGINAL GENOME SEQUENCE #######################\n");
	key.write("########################################################\n");

	key.write("> Full Original Genome\n");
	genomeMarker = 0;
	while( genomeMarker < len(genome) ):
		if( genomeMarker+80 < len(genome) ):
			key.write( genome[genomeMarker:genomeMarker+80] + "\n");
			genomeMarker = genomeMarker+80;
		else:
			key.write( genome[genomeMarker::] + "\n");
			break;

	##close files
	key.close();
	gbFile.close();
	fOutput.close();
	




###########################################################################
###########################################################################
### Main Method
###########################################################################
###########################################################################
def main():

#	testDebug();
	random.seed();
	
	################################################ Usage Statement
	if len(sys.argv) == 1:
		usage()
		raise SystemExit, 5

	################################################ Help Statement
	else:
		if(len(sys.argv) == 4 and sys.argv[1] == "-genome"):
			getGenome( sys.argv[2], sys.argv[3] );
			raise SystemExit, 5
		
		##print("python genBank2Fasta.py -reads [genBankFile] [readLength] [xCoverage] [minOverlap [maxOverlap] [fastaOutput] [answerKey]" );
		if(len(sys.argv) == 9 and sys.argv[1] == "-reads"):
			getReads( sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8]  );
			raise SystemExit, 5

		##print("python genBank2Fasta.py -randomizeFasta [outputFasta] [answerKey] [inputRead(s)]" );
		if(sys.argv[1] == "-randomizeFasta" and len(sys.argv) > 5):
			randomizeFastas( sys.argv[2], sys.argv[3], sys.argv[4::] );
			raise SystemExit, 5

		##print("python genBank2Fasta.py -denseReads [genBankFile] [outputFasta] [readLength] [minReadsPerNucleotide] [maxReadsPerNucleotide] [answerKey]" );
		if( sys.argv[1] == "-denseReads" and len(sys.argv) == 8 ):
			denseReadsFasta( sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7] );
			raise SystemExit, 5

		###if none of the usage scenarios happen, exit.
		usage();
		raise SystemExit, 5
	################################################ 

if __name__ == "__main__":
	main()
	














