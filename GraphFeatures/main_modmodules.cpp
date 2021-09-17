#include <stdio.h>
#include <getopt.h>
#include <stdlib.h>
#include <vector>
#include <stack>
#include <algorithm>
#include <unistd.h>
#include "graph_vector.h"
#include "tools.h"
#include "community.h"

char *filein = NULL;
char *fileout = NULL;

int maxclause = 400;
bool verbose = false;
int maxx=0;

char *modules = NULL;

void printUsage(char* arg){
	printf("Usage: %s [-v] [-o <fileout>] [-m maxclause] -M <modules> filein\n", arg);
	exit(-1);
}

int main(int argc, char *argv[]){

	int opt;
	
	while ((opt = getopt(argc, argv, "?ho:m:M:v")) != -1){
		switch (opt){
			case 'o':
				fileout = optarg;
				break;
			case 'm':
				maxclause = atoi(optarg);
				break;
			case 'M':
				modules = optarg;
				break;
			case 'v':
				verbose = true;
				break;
			default:
				printUsage(argv[0]);
		}
	}
	
	if(optind<argc)
		filein = argv[optind];
	
	if(filein == NULL || modules == NULL){
		printUsage(argv[0]);
	}
	
	
	// Reading graph
	if(verbose)
		cerr << "Reading formula...";
	
	Graph *g = readVIG(filein,maxclause);
	
	if(verbose)
		cerr << "DONE!" << endl;
	
	// Reading modules
	vector<int> n2c;
	FILE *source;
	source = fopen(modules, "r");
	if(!source){
		cerr << "Unable to read CNF file " << modules << endl;
		exit(-1);
	}
	
	int var=-1;
	while(fscanf(source, "%i", &var)==1) {
		n2c.push_back(var);
	}
	
	Community c(g, n2c);
	double mod = c.modularity();
	cout << "modularity = " << mod << endl;
	
	if(fileout != NULL){
		FILE* out = fopen(fileout, "w");
		fprintf(out, "modularity = %f\n", mod);
		fclose(out);
	}
	
	
}