LDFLAGS += 
OBJECTS := main.o
CXXFLAGS ?= -Wall -Wextra
CXXFLAGS += 
CXX ?= g++

HEADERS := 
EXECUTABLE := main

debug : CXXFLAGS += -Og -g -pg
release : CXXFLAGS += -O3 -fno-exceptions
debug : LDFLAGS +=
release : LDFLAGS += -O
debug : BUILD_TYPE := debug
release : BUILD_TYPE := release

debug: $(EXECUTABLE)
release: $(EXECUTABLE)

$(EXECUTABLE): $(OBJECTS) $(HEADERS) $(BOARD_LIB)
	$(CXX) $(OBJECTS) $(LDFLAGS) $(BOARD_LIB) -o $@

%.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $< -c

.PHONY: clean $(BOARD_LIB)

clean:
	$(RM) $(EXECUTABLE) $(OBJECTS)