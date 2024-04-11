#################################################################################
#	Simple gnu Makefile for VC++ users, by Brian Chen
#
#	X =  is a field being set
#	$(X) is a defined field
#
#	notes:
#		-new following line must be delimited with <TAB> and not spaces.
#################################################################################


#################################################################################
# Names and flags													#
#################################################################################

CC = gcc
CXX = g++
CPPFLAGS = -g -Wall -pedantic -pedantic-errors -Wno-deprecated 
CFLAGS = -g

#directory containing source
SOURCEDIR = source/

#directory for object files
OBJECTDIR = object/

#directory for executables and input files
DEBUGDIR = debug/

#name of executable
EXENAME = example

#Standard Affix files, for VC++ projects
STDAFX = $(SOURCEDIR)StdAfx.cpp

#executable path
EXEPATH = $(DEBUGDIR)$(EXENAME)


#################################################################################
# Define SUPPORT_OBJS to be any .o files that must be linked in with the	#
# final compiler.								#
#################################################################################

C_OBJS = \
$(OBJECTDIR)set.o \
$(OBJECTDIR)prime.o

SUPPORT_OBJS = \
$(OBJECTDIR)StdAfx.o \
$(OBJECTDIR)main.o \

#################################################################################
# Define final output here with lowest level dependancies (should be automatic)	#
#################################################################################

$(EXEPATH): $(SUPPORT_OBJS) $(C_OBJS)
	$(CXX) $(CFLAGS) -o $(EXEPATH) $(SUPPORT_OBJS) $(C_OBJS) -lm

#################################################################################
# Dependencies of .o files							#
#################################################################################

$(SUPPORT_OBJS): $(OBJECTDIR)%.o: $(SOURCEDIR)%.cpp $(STDAFX)
	$(CXX) -c $(CPPFLAGS) $< -o $@

$(C_OBJS): $(OBJECTDIR)%.o: $(SOURCEDIR)%.c $(STDAFX)
	$(CC) -c $(CFLAGS) $< -o $@

#################################################################################
# Cleaning option for deleting old object files					#
#################################################################################

clean:
	rm -f $(OBJECTDIR)*.o $(EXEPATH)
