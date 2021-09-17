/*
Graph Features Computation for SAT instances.
Version 2.2
Authors:
  - Carlos Ansótegui (DIEI - UdL)
  - María Luisa Bonet (LSI - UPC)
  - Jesús Giráldez-Cru (IIIA-CSIC)
  - Jordi Levy (IIIA-CSIC)

Contact: jgiraldez@iiia.csic.es

    Copyright (C) 2014  C. Ansótegui, M.L. Bonet, J. Giráldez-Cru, J. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <stdio.h>
#include <vector>
#ifndef VECTOR
#include "graph_set.h"
#else
#include "graph_vector.h"
#endif
#include <algorithm>

extern bool verbose;

int abs(int x){
	if(x<0)
		return -x;
	else
		return x;
}

vector<pair <int,int> > arityVar(char* filein){
	
	FILE *source;
	source = fopen(filein, "r");
	if(!source){
		cerr << "Unable to read CNF file " << filein << endl;
		exit(-1);
	}

	// Skip comments
	int aux=-1;
	while((aux=getc(source))=='c'){
		while (getc(source)!='\n')
			;
	}
	ungetc(aux,source);

	// File Head
	int totVars=0, totClauses=0;
	if( !fscanf(source, "p cnf %i %i", &totVars, &totClauses)) {
		cerr << "Invalid CNF file\n";
		exit(-1);
	}

	vector< pair <int,int> > v;
	vector<int> nOccurs(totVars,0);
	
	int var=-1;
	while(fscanf(source, "%d", &var)==1) {
		if(var==0){
			;
		}else{
			nOccurs[abs(var)-1]++;
		}
	}
	
	sort(nOccurs.begin(), nOccurs.end());
	
	int prev = nOccurs[0];
	int addition = 1;
	for (int i=1; i<nOccurs.size(); i++) {
		if (nOccurs[i] == prev)
			addition++;
		else {
			if(verbose)
				cerr << "     " << prev << " " << addition << endl;
			v.push_back(make_pair(prev,addition));
			prev = nOccurs[i];
			addition = 1;
		}
	}
	if(verbose)
		cerr << "     " << prev << " " << addition << endl;
	v.push_back(make_pair(prev,addition));
	
	return v;
}

vector<pair <int,int> > arityClause(char* filein){
	
	FILE *source;
	source = fopen(filein, "r");
	if(!source){
		cerr << "Unable to read CNF file " << filein << endl;
		exit(-1);
	}

	// Skip comments
	int aux=-1;
	while((aux=getc(source))=='c'){
		while (getc(source)!='\n')
			;
	}
	ungetc(aux,source);

	// File Head
	int totVars=0, totClauses=0;
	if( !fscanf(source, "p cnf %i %i", &totVars, &totClauses)) {
		cerr << "Invalid CNF file\n";
		exit(-1);
	}

	vector< pair <int,int> > v;
	vector<int> nOccurs(100,0);
	
	int var=-1;
	int clause=0;
	int size=0;
	while(fscanf(source, "%d", &var)==1) {
		if(var==0){
			if(size>=nOccurs.size())
				nOccurs.resize(size+1);
			nOccurs[size]++;
			size=0;
		}else{
			size++;
		}
	}
	
	for(int i=1; i<nOccurs.size(); i++){
		if(nOccurs[i]>0){
			if(verbose){
				cerr << "     " << i << " " << nOccurs[i] << endl;
			}
			v.push_back(make_pair(i,nOccurs[i]));
		}
	}
		
	return v;
}
