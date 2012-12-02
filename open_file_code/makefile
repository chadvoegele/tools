CXX=g++
CC=g++
DEBUG=-g
CXXFLAGS=-O2 $(DEBUG)
LIBS=-lmagic
SRC=open_file.cpp
PROG=open_file
OBJ=$(SRC:.cpp=.o)

$(PROG): $(OBJ)
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LIBS)

clean:
	rm -f $(OBJ) $(PROG)

