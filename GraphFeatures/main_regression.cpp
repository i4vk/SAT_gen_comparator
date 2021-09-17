#include <math.h>
#include <map>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <limits>
#include "tools.h"
#include <unistd.h>

using namespace std;

bool verbose;

//-----------------------------------------------------------------------------
int main(int argc, char *argv[]) {
//-----------------------------------------------------------------------------

  FILE *fplot=NULL;
  char * fin;
  double minx = numeric_limits<float>::min( );
  double maxx = numeric_limits<float>::max( );
  string filename;

  int opt;
  while ((opt = getopt(argc, argv, "f:?hp:m:M:")) != -1)
    switch (opt) {
    case 'f': 
	fin = optarg;
      break;
    case 'p':
      filename = optarg;
      if (filename.length() >=4 && filename.substr(filename.length() - 4) == ".plt") 
	filename = filename.substr(0, filename.length() - 4);
      if((fplot = fopen((filename+".plt").c_str(), "w"))==NULL){
	cerr << argv[0] << ": Unamble to open file " << filename << ".plt" << endl;
	exit(-1);
      }
      break;
    case 'm': minx = atof(optarg);
      break;
    case 'M': maxx = atof(optarg);
      break;
    case 'h':
    case '?':
    default : 
    printf("Usage: %s -f filein [-p fileplot] [-m minx] [-M maxx] \n",argv[0]);
    exit(0);
    break;
    }

/****************************************************************************/
  
  vector <pair <int,int> > v = readPoints(fin);

  vector <pair <double,double> > v1,v2;
  for (vector <pair <int,int> >::iterator it = v.begin(); it != v.end(); it++) 
    if (it->first >= minx && it->first <= maxx) {
      v1.push_back(pair<double,double>(log((double)it->first), log((double)it->second)));
      v2.push_back(pair<double,double>((double)it->first, log((double)it->second)));
    }
  
  pair <double,double> polreg = regresion(v1);
  pair <double,double> expreg = regresion(v2);
  cout << "dimension = " << -polreg.first << endl;
  cout << "decay = " << -expreg.first << endl;

  if (fplot != NULL) {
    fprintf(fplot,"set logscale xy\nset term postscript eps enhanced color\nset size 0.7,0.7\nset output \"%s.eps\"\n", filename.c_str());
    fprintf(fplot, "plot \"%s.dim\" lt 1 pt 7",
	    filename.c_str());
    fprintf(fplot, ",exp(%lf*log(x)+%lf) lt 1 ti \"dimension=%0.2f\"",
	    polreg.first, polreg.second ,-polreg.first); 
    fprintf(fplot, ",exp(%lf*x+%lf) lt 2 ti \"decay=%0.2f\"\n",
	    expreg.first, expreg.second, -expreg.first); 
    fprintf(fplot, "quit\n");
    fclose(fplot);
  }

}
