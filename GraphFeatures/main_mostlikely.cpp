#include <stdio.h>
#include <getopt.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <vector>
#include <algorithm>
#include <iostream> 
#include <assert.h>
#include "tools.h"
#include <unistd.h>

using namespace std;

bool verbose;
bool var = true;

void printUsage(char* arg){
	printf("Usage: %s -f filein [-m maxmin] [-o fileout] [-p fileplot] [-i fileint] [-c (for plotting clauses)]\n", arg);
	exit(-1);
}


//-----------------------------------------------------------------------------
int main(int argc, char *argv[]) {
//-----------------------------------------------------------------------------

  int opt;
  char *fin;
  char *fout = NULL;
  char *fint = NULL;
  char *fplot = NULL;
  int maxxmin = 10;

  while ((opt = getopt(argc, argv, "f:o:m:?hp:ci:")) != -1)
    switch (opt) {
    case 'm':
      maxxmin = atoi(optarg);
      break;
    case 'f': 
      fin = optarg;
      break;
    case 'c':
	  var = false;
	  break;
    case 'o':
	fout = optarg; 
      break;
    case 'p': 
		fplot =optarg;     
      break;
	case 'i':
	  fint = optarg;
	  break;
    case 'h':
    case 'v':
    case '?':
    default : 
		printUsage(argv[0]);
    }
  

/****************************************************************************/

  vector <pair <int,int> > v = readPoints(fin);

  double alpha = mostlikely(v, maxxmin, fout, fint, fplot, var);
  cout << "alpha = " << alpha << endl;

}

