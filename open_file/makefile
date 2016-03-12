CXX=g++
CXXFLAGS=-O2
LIBS=-lmagic
SRC=open_file.cpp
PROG=open_file
OSX_INCLUDE_DIR=/usr/local/include
OSX_LIB_DIR=/usr/local/lib
OBJ=$(SRC:.cpp=.o)

$(PROG): $(OBJ)
	$(CXX) -L $(OSX_LIB_DIR) -o $@ $^ $(DEBUGFLAGS) $(CXXFLAGS) $(LIBS)

$(OBJ): $(SRC)
	$(CXX) -I $(OSX_INCLUDE_DIR) -c -D CONFIG=$(CONFIG) $(DEBUGFLAGS) $(CXXFLAGS) $^

clean:
	rm -f $(OBJ) $(PROG)

