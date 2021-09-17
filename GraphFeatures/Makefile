CPP = g++ -DNDEBUG -ansi -O3
LDLIBS += -lm
CFLAGS += -Wall -Wno-deprecated -DNDEBUG

all : features_v features_s modmodules regression mostlikely

clean :
	rm -f *.o features_v features_s modmodules regression mostlikely *~

features_v : main.cpp graph_vector.h tools.h powerlaw.h community.h dimension.h
		$(CPP) -o $@ $^ -DVECTOR
		
features_s : main.cpp graph_set.h tools.h powerlaw.h community.h dimension.h
				$(CPP) -o $@ $^ -DSET
				
modmodules : main_modmodules.cpp graph_vector.h community.h tools.h
		$(CPP) -o $@ $^
		
regression : main_regression.cpp tools.h
		$(CPP) -o $@ $^

mostlikely : main_mostlikely.cpp tools.h
		$(CPP) -o $@ $^
		
%: %.cpp 
	$(CPP) -o $@ $^

%.o: %.cpp %.h
	$(CPP) -o $@ -c $<

%.cpp: %.lex
	lex -+ -o $@ $<
