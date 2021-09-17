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
#include <string.h>
#include <getopt.h>
#include <stdlib.h>
#include <vector>
#ifndef VECTOR
#include "graph_set.h"
#else
#include "graph_vector.h"
#endif
#include "tools.h"
#include "powerlaw.h"
#include "dimension.h"
#include "community.h"


#ifndef MAIN_H
#define MAIN_H

using namespace std;

std::string fin = "";

bool modeAll = true;
bool modeAlphaVar = false;
bool modeAlphaClause = false;
bool modeDimVIG = false;
bool modeDimCVIG = false;
bool modeModularityVIG = false;
bool modeModularityCVIG = false;

int minx = 0;
int maxx = 15;
int maxx2 = 6;
int maxclause = 400;
int maxxmin = 10;
double precision = 0.000001;
bool verbose = false;

bool all = false;
std::string var = "";
std::string alphavar = "";
std::string varint = "";
std::string varplot = "";
std::string clau = "";
std::string alphaclau = "";
std::string clauint = "";
std::string clauplot = "";
std::string dim = "";
std::string resdim = "";
std::string dimplot = "";
std::string dib = "";
std::string resdib = 	"";
std::string dibplot = "";
std::string mod = "";
std::string mob = "";
std::string fout = "";
std::string modules = "";

void printUsage(int argc, char *argv[]){
	cout << "Graph Features Computation for SAT instances. Version 2.2" << endl;
	cout << "Copyright (C) 2014  C. Ansótegui, M.L. Bonet, J. Giráldez-Cru, J. Levy" << endl;
	cout << "Contact: jgiraldez@iiia.csic.es" << endl;
	cout << endl;
	cout << "USAGE: " << argv[0] << " [modes] [options] [fileouts] <instance.cnf>" << endl;
	cout << endl;
	cout << "MODES:" << endl;
	cout << "     If one (or more) modes are activated," << endl;
	cout << "   only structures asociated to it (them)" << endl;
	cout << "   are computed (and only its/them" << endl;
	cout << "   associated output files are created)." << endl;
	cout << "  -1 : Scale-free structure for variable occurrences" << endl;
	cout << "  -2 : Scale-free structure for clause size" << endl;
	cout << "  -3 : Self-similar structure for VIG" << endl;
	cout << "  -4 : Self-similar structure for CVIG" << endl;
	cout << "  -5 : Community structure for VIG" << endl;
	cout << "  -6 : Community structure for CVIG" << endl;
	cout << endl;
	cout << "OPTIONS (default values in brackets):" << endl;
	cout << "  -x <int>     : Max f_min (10) for scale-free structure" << endl;
	cout << "  -c <int>     : Max clause size (400). Longer clauses are disregarded in VIG and CVIG" << endl;
	cout << "  -m <int>     : Min radius r in N(r) (0)" << endl;
	cout << "  -M <int>     : Max radius r in N(r) (15)" << endl;
	cout << "  -i <int>     : Max radius r in N(r) for computing the regression (6)" << endl;
	cout << "  -p <double>  : Precision of GFA (0.000001) for community structure" << endl;
	cout << "  -v           : Verbosity (no verbosity)" << endl;
	cout << "  -h           : Prints this help" << endl;
	cout << endl;
	cout << "FILEOUTS:" << endl;
	cout << "     If some mode is activated," << endl;
	cout << "   only its associated output" << endl;
	cout << "   files are generated." << endl;
	cout << "  -a : Generates all output files: <cnf>.<suffix>" << endl;
	cout << "    If this option is activated (false by default), any other fileout option is ignored." << endl;
	cout << "    List of suffixes:" << endl;
	cout << "      General: csv" << endl;
	cout << "      Scale-free: alphavar, alphavar.out, alphavar.int, alphavar.plt, alphaclau, alphaclau.out, alphaclau.int, alphaclau.plt" << endl;
	cout << "      Self-similarity: dim, dim.out, dim.plt, dib, dib.out, dib.plt," << endl;
	cout << "      Community: mod.out, mod.modules, mob.out," << endl;
	cout << "  -j <fileout> : General results in CSV format" << endl;
	cout << "    By default, they are printed in stdout." << endl;
	cout << "  -t <fileout> : Distribution of variables occurrences" << endl;
	cout << "  -l <fileout> : Scale-free structure results for variable occurrences" << endl;
	cout << "  -k <fileout> : Normalized distribution of variables occurrences" << endl;
	cout << "  -g <fileout> : Gnuplot file for variable occurrences" << endl;
	cout << "  -T <fileout> : Distribution of clauses sizes" << endl;
	cout << "  -L <fileout> : Scale-free structure results for clause sizes" << endl;
	cout << "  -K <fileout> : Normalized distribution of clause sizes" << endl;
	cout << "  -G <fileout> : Gnuplot file for clause sizes" << endl;
	cout << "  -d <fileout> : Function number of tiles vs radius: N(r) for VIG" << endl;
	cout << "  -o <fileout> : Self-similar structure results for VIG" << endl;
	cout << "  -b <fileout> : Gnuplot file for self-similar structure in VIG" << endl;
	cout << "  -D <fileout> : Function number of tiles vs radius: N(r) for CVIG" << endl;
	cout << "  -O <fileout> : Self-similar structure result for CVIG" << endl;
	cout << "  -B <fileout> : Gnuplot file for self-similar structure in CVIG" << endl;
	cout << "  -y <fileout> : Modularity results for VIG" << endl;
	cout << "  -q <fileout> : Modules of VIG" << endl;
	cout << "  -Y <fileout> : Modularity results for CVIG" << endl;
	exit(-1);
}

void parseArgs(int argc, char *argv[]){
	int opt;
	while((opt=getopt(argc, argv, "123456x:c:m:M:i:p:v?haj:t:l:k:g:T:L:K:G:d:o:b:D:O:B:y:q:Y:")) != -1)
		switch(opt){
			case '1':
				modeAlphaVar = true;
				modeAll = false;
				break;
			case '2':
				modeAlphaClause = true;
				modeAll = false;
				break;
			case '3':
				modeDimVIG = true;
				modeAll = false;
				break;
			case '4':
				modeDimCVIG = true;
				modeAll = false;
				break;
			case '5':
				modeModularityVIG = true;
				modeAll = false;
				break;
			case '6':
				modeModularityCVIG = true;
				modeAll = false;
				break;
			case 'm':
				minx = atoi(optarg);
				break;
			case 'M':
				maxx = atoi(optarg);
				break;
			case 'i':
				maxx2 = atoi(optarg);
				break;
			case 'c':
				maxclause = atoi(optarg);
				break;
			case 'x':
				maxxmin = atoi(optarg);
				break;
			case 'p':
				precision = atof(optarg);
				break;
			case 'v':
				verbose = true;
				break;
			case 'a':
				all = true;
				break;
			case 'j':
				fout = optarg;
				break;
			case 't':
				var = optarg;
				break;
			case 'l':
				alphavar = optarg;
				break;
			case 'k':
				varint = optarg;
				break;
			case 'g':
				varplot = optarg;
				break;
			case 'T':
				clau = optarg;
				break;
			case 'L':
				alphaclau = optarg;
				break;
			case 'K':
				clauint = optarg;
				break;
			case 'G':
				clauplot = optarg;
				break;
			case 'd':
				dim = optarg;
				break;
			case 'o':
				resdim = optarg;
				break;
			case 'b':
				dimplot = optarg;
				break;
			case 'D':
				dib = optarg;
				break;
			case 'O':
				resdib = optarg;
				break;
			case 'B':
				dibplot = optarg;
				break;
			case 'y':
				mod = optarg;
				break;
			case 'z':
				mob = optarg;
				break;
			case 'q':
					modules = optarg;
					break;
			case 'h':
			case '?':
			default:
				printUsage(argc, argv);
		}
		
	if(optind < argc){
		fin = argv[optind];
		if(all){
				// var = new char[strlen(fin)+9];
				var.copy(fin, fin.length(), 0);
				var = var + ".alphavar";
				// strcpy(var, fin);
				// strcat(var, ".alphavar");
				// alphavar = new char[strlen(fin)+13];
				alphavar.copy(fin, fin.length(), 0);
				alphavar = alphavar + ".alphavar.out";
				// strcpy(alphavar, fin);
				// strcat(alphavar, ".alphavar.out");
				// varint = new char[strlen(fin)+13];
				varint.copy(fin, fin.length(), 0);
				varint = varint + ".alphavar.int"
				// strcpy(varint, fin);
				// strcat(varint, ".alphavar.int");
				// varplot = new char[strlen(fin)+13];
				varplot.copy(fin, fin.length(), 0);
				varplot = varplot + "alphavar.plt"
				// strcpy(varplot, fin);
				// strcat(varplot, ".alphavar.plt");

				cout << "llego 2" << endl;
			
				// clau = new char[strlen(fin)+9];
				// strcpy(clau, fin);
				// strcat(clau, ".alphaclau");
				clau.copy(fin, fin.length(), 0);
				clau = clau + ".alphaclau";
				// alphaclau = new char[strlen(fin)+13];
				// strcpy(alphaclau, fin);
				// strcat(alphaclau, ".alphaclau.out");
				alphaclau.copy(fin, fin.length(), 0);
				alphaclau = alphaclau + ".alphaclau.out";
				// clauint = new char[strlen(fin)+13];
				// strcpy(clauint, fin);
				// strcat(clauint, ".alphaclau.int");
				clauint.copy(fin, fin.length(), 0);
				clauint = clauint + ".alphaclau.int";
				// clauplot = new char[strlen(fin)+13];
				// strcpy(clauplot, fin);
				// strcat(clauplot, ".alphaclau.plt");
				clauplot.copy(fin, fin.length(), 0);
				clauplot = clauplot + ".alphaclau.plt";
			
				// dim = new char[strlen(fin)+5];
				// strcpy(dim, fin);
				// strcat(dim, ".dim");
				dim.copy(fin, fin.length(), 0);
				dim = dim + ".dim";
				// cout << strlen(fin)+9 << endl;
				// cout << resdim << endl;
				// cout << "telescopio" << endl;
				// resdim = new char[strlen(fin)+9];
				// cout << "papaya" << endl;
				// strcpy(resdim, fin);
				// strcat(resdim, ".dim.out");
				resdim.copy(fin, fin.length(), 0);
				resdim = resdim + ".dim.out";
				// dimplot = new char[strlen(fin)+9];
				// strcpy(dimplot, fin);
				// strcat(dimplot, ".dim.plt");
				dimplot.copy(fin, fin.length(), 0);
				dimplot = dimplot + ".dim.plt";
			
				// dib = new char[strlen(fin)+5];
				// strcpy(dib, fin);
				// strcat(dib, ".dib");
				dib.copy(fin, fin.length(), 0);
				dib = dib + ".dib";
				// resdib = new char[strlen(fin)+9];
				// strcpy(resdib, fin);
				// strcat(resdib, ".dib.out");
				std::str.copy(resdib, fin);
				resdib = resdib + ".dib.out";
				// dibplot = new char[strlen(fin)+9];
				// strcpy(dibplot, fin);
				// strcat(dibplot, ".dib.plt");
				std::str.copy(dibplot, fin);
				dibplot = dibplot + ".dib.plot";
			
				// mod = new char[strlen(fin)+9];
				// strcpy(mod, fin);
				// strcat(mod, ".mod.out");
				std::str.copy(mod, fin);
				mod = mod + ".mod.out";
				// mob = new char[strlen(fin)+9];
				// strcpy(mob, fin);
				// strcat(mob, ".mob.out");
				std::str.copy(mob, fin);
				mob = mob + ".mob.out";
				// modules = new char[strlen(fin)+13];
				// strcpy(modules, fin);
				// strcat(modules, ".mod.modules");
				std::str.copy(modules, fin);
				modules = modules + ".mod.modules";
			
				// fout = new char[strlen(fin)+5];
				// strcpy(fout, fin);
				// strcat(fout, ".csv");
				std::str.copy(fout, fin);
				fout = fout + ".csv";
		}
	}
	if(fin == ""){
		printUsage(argc, argv);
	}

}

int main(int argc, char *argv[]){

	clock_t t_ini, t_fin;
	double secsGraphs, secsAlphaVar, secsAlphaClau, secsDim, secsDib, secsMod, secsModBip, secsTotal;

	parseArgs(argc, argv);
	
	t_ini = clock();
	
	if(verbose){
		cerr << "***************************************" << endl;
		cerr << "Graph Features Computation for SAT instances. Version 2.2" << endl;
		cerr << "Copyright (C) 2014  C. Ansótegui, M.L. Bonet, J. Giráldez-Cru, J. Levy" << endl;
		cerr << "Contact: jgiraldez@iiia.csic.es" << endl;
		cerr << "***************************************" << endl;
		cerr << "Formula: " << fin << endl;
		cerr << "Reading formula and building graphs...";
	}
	
	bool anyModeVIG = modeDimVIG || modeModularityVIG;
	bool anyModeCVIG = modeDimCVIG || modeModularityCVIG;
	
	Graph* vig = NULL;
	Graph* cvig = NULL;
	
	if(modeAll || (anyModeVIG && anyModeCVIG)){
		t_ini = clock();
		pair<Graph*,Graph*> p = readFormula(fin, maxclause);
		t_fin = clock();
		secsGraphs = (double)(t_fin - t_ini) / CLOCKS_PER_SEC;
	
		vig = p.first;
		cvig = p.second;
	}else if(anyModeVIG){
		t_ini = clock();
		vig = readVIG(fin, maxclause);
		t_fin = clock();
		secsGraphs = (double)(t_fin - t_ini) / CLOCKS_PER_SEC;
	}else if(anyModeCVIG){ //anyModeCVIG
		t_ini = clock();
		cvig = readCVIG(fin, maxclause);
		t_fin = clock();
		secsGraphs = (double)(t_fin - t_ini) / CLOCKS_PER_SEC;
	}

	if(verbose)
		cerr << " DONE!" << endl << "------------" << endl;
		
	double alphavarexp=-1;
	double alphaclauexp=-1;

	vector<int> needed;
	vector <pair <double,double> > v1;
	vector <pair <double,double> > v2;
	pair <double,double> polreg = make_pair(-1,-1);
	pair <double,double> expreg = make_pair(-1,-1);
	pair <double,double> polregB = make_pair(-1,-1);
	pair <double,double> expregB = make_pair(-1,-1);

	Community c(vig);
	Community c_bip(cvig);
	double modularity=-1;
	double modularity_bip=-1;
	
	//****************************************************************
	if(modeAll || modeAlphaVar){
		if(verbose)
			cerr << "Computing SCALE-FREE Structure (Variables)" << endl;

		t_ini = clock();
		vector<pair <int,int> > a = arityVar(fin);
		alphavarexp = mostlikely(a, maxxmin, alphavar, varint, varplot, true);
		t_fin = clock();
		secsAlphaVar = (double)(t_fin - t_ini) / CLOCKS_PER_SEC;
	
		if(var != ""){
			FILE* f1 = fopen(var.c_str(), "w");
			for(int i=0; i<a.size(); i++)
				fprintf(f1, "%d %d\n", a[i].first, a[i].second);
			fclose(f1);
		}
	
		if(verbose)
			cerr << "------------" << endl;
	}
	//****************************************************************
	if(modeAll || modeAlphaClause){
		if(verbose)
			cerr << "Computing SCALE-FREE Structure (Clauses)" << endl;

		t_ini = clock();
		vector<pair <int,int> > b = arityClause(fin);
		alphaclauexp = mostlikely(b, maxxmin, alphaclau, clauint, clauplot, false);
		t_fin = clock();
		secsAlphaClau = (double)(t_fin - t_ini) / CLOCKS_PER_SEC;
		
		if(clau != ""){
			FILE* f1 = fopen(clau.c_str(), "w");
			for(int i=0; i<b.size(); i++)
				fprintf(f1, "%d %d\n", b[i].first, b[i].second);
			fclose(f1);
		}
		
		if(verbose)
			cerr << "------------" << endl;	
	}
	//****************************************************************		
	if(modeAll || modeDimVIG){
		if(verbose)
			cerr << "Computing SELF-SIMILAR Structure (VIG)" << endl;

		v1.clear(); v2.clear();
		
		t_ini = clock();	
		needed = computeNeeded(vig);
		
		for(int i=1; i<needed.size(); i++){
			if(i>=minx && i<=maxx2){
				v1.push_back(pair<double,double>(log(i), log(needed[i])));
				v2.push_back(pair<double,double>((double)i, log(needed[i])));	
			}
		}
		
		polreg = regresion(v1);
		expreg = regresion(v2);
		
		t_fin = clock();
		secsDim = (double)(t_fin - t_ini) / CLOCKS_PER_SEC;
	
		if(dim != ""){
			FILE *f2 = fopen(dim.c_str(), "w");
			for(int i=1; i<needed.size(); i++){
				fprintf(f2, "%d %d\n", i, needed[i]);
			}
			fclose(f2);
		}
	
		if(resdim != ""){
			FILE* f3 = fopen(resdim.c_str(), "w");
			fprintf(f3, "dimension = %f\n", -polreg.first);
			fprintf(f3, "decay = %f\n", -expreg.first);
			fclose(f3);
		}
		
	    if (dimplot != "") {
			if(dim != ""){
				FILE *fplot = fopen(dimplot.c_str(), "w");
				string eps(dimplot);
				eps = eps.substr(0,strlen(dimplot)-4);
				eps.append(".eps");
				fprintf(fplot,"set logscale xy\nset term postscript eps enhanced color\nset size 0.7,0.7\nset output \"%s\"\n", eps.c_str());
				fprintf(fplot, "plot \"%s\" lt 1 pt 7", dim);
				fprintf(fplot, ",exp(%lf*log(x)+%lf) lt 1 ti \"dimension=%0.2f\"",polreg.first, polreg.second ,-polreg.first); 
				fprintf(fplot, ",exp(%lf*x+%lf) lt 2 ti \"decay=%0.2f\"\n",expreg.first, expreg.second, -expreg.first); 
				fprintf(fplot, "quit\n");
				fclose(fplot);
			}else{
				cerr << "[WARNING]: Both dimension files for N(r) function and plot should be defined." << endl;
			}
	    }
		
		if(verbose){
			cerr << "dimension = " << -polreg.first << endl;
			cerr << "decay = " << -expreg.first << endl;
			cerr << "------------" << endl;
		}

	}
	//****************************************************************
	if(modeAll || modeDimCVIG){
		if(verbose)
			cerr << "Computing SELF-SIMILAR Structure (CVIG)" << endl;

		v1.clear(); v2.clear();
		
		t_ini = clock();		
		needed = computeNeeded(cvig);
	
		for(int i=1; i<needed.size(); i++){
			if(i>=minx && i<=maxx2){
				v1.push_back(pair<double,double>(log(i), log(needed[i])));
				v2.push_back(pair<double,double>((double)i, log(needed[i])));	
			}
		}
		
		polregB = regresion(v1);
		expregB = regresion(v2);
		
		t_fin = clock();
		secsDib = (double)(t_fin - t_ini) / CLOCKS_PER_SEC;	
		
		FILE* f4;
		if(dib != ""){
			f4 = fopen(dib.c_str(), "w");
			for(int i=1; i<needed.size(); i++){
				fprintf(f4, "%d %d\n", i, needed[i]);
			}
			fclose(f4);
		}

		if(verbose){
			cerr << "dimension bipartite = " << -polregB.first << endl;
			cerr << "decay bipartite = " << -expregB.first << endl;
			cerr << "------------" << endl;
		}
	
		if(resdib != ""){
			FILE* f5 = fopen(resdib.c_str(), "w");
			fprintf(f5, "dimension_bip = %f\n", -polregB.first);
			fprintf(f5, "decay_bip = %f\n", -expregB.first);
			fclose(f5);
		}
		
	    if (dibplot != "") {
			if(dib != ""){
				FILE *fplot = fopen(dibplot.c_str(), "w");
				string eps(dibplot);
				eps = eps.substr(0,strlen(dibplot)-4);
				eps.append(".eps");
				fprintf(fplot,"set logscale xy\nset term postscript eps enhanced color\nset size 0.7,0.7\nset output \"%s\"\n", eps.c_str());
				fprintf(fplot, "plot \"%s\" lt 1 pt 7", dib);
				fprintf(fplot, ",exp(%lf*log(x)+%lf) lt 1 ti \"dimension=%0.2f\"",polregB.first, polregB.second ,-polregB.first); 
				fprintf(fplot, ",exp(%lf*x+%lf) lt 2 ti \"decay=%0.2f\"\n",expregB.first, expregB.second, -expregB.first); 
				fprintf(fplot, "quit\n");
				fclose(fplot);
			}else{
				cerr << "[WARNING]: Both dimension files for N(r) function and plot should be defined." << endl;
			}
	    }
	}
	//****************************************************************
	if(modeAll || modeModularityVIG){
		if(verbose)
			cerr << "Computing COMMUNITY Structure (VIG)" << endl;
	
		t_ini = clock();
		modularity = c.compute_modularity_GFA(precision);
		c.compute_communities();
		t_fin = clock();
		secsMod = (double)(t_fin - t_ini) / CLOCKS_PER_SEC;

		if(verbose){
			cerr << "modularity = " << modularity << endl;
			cerr << "communities = " << (int)c.ncomm << endl;
			cerr << "largest size = " << (double)c.Comm[c.Comm_order[0].first].size()/vig->size() << endl;
			cerr << "iterations = " << c.iterations << endl;
			cerr << "------------" << endl;
		}
	
		if(mod != ""){
			FILE* f6 = fopen(mod.c_str(), "w");
			fprintf(f6, "modularity = %f\n", modularity);
			fprintf(f6, "communities = %d\n", (int) c.ncomm);
			fprintf(f6, "largest size = %f\n", (double)c.Comm[c.Comm_order[0].first].size()/vig->size());
			fprintf(f6, "iterations = %d\n", c.iterations);
			fclose(f6);
		}
	
		if(modules != ""){
			c.print_modules(modules);
		}
	}
	//****************************************************************	
	if(modeAll || modeModularityCVIG){
		if(verbose)
			cerr << "Computing COMMUNITY Structure (CVIG)" << endl;
	
		t_ini = clock();	
		modularity_bip = c_bip.compute_modularity_GFA(precision);
		c_bip.compute_communities();
		t_fin = clock();
	
		if(verbose){
			cerr << "modularity = " << modularity_bip << endl;
			cerr << "communities = " << (int)c_bip.ncomm << endl;
			cerr << "largest size = " << (double)c_bip.Comm[c_bip.Comm_order[0].first].size()/cvig->size() << endl;
			cerr << "iterations = " << c_bip.iterations << endl;
			cerr << "------------" << endl;
		}
	
		if(mob != ""){
			FILE* f6 = fopen(mob.c_str(), "w");
			fprintf(f6, "modularity = %f\n", modularity_bip);
			fprintf(f6, "communities = %d\n", (int) c_bip.ncomm);
			fprintf(f6, "largest size = %f\n", (double)c_bip.Comm[c_bip.Comm_order[0].first].size()/cvig->size());
			fprintf(f6, "iterations = %d\n", c_bip.iterations);
			fclose(f6);
		}
	
	
		secsModBip = (double)(t_fin - t_ini) / CLOCKS_PER_SEC;
	}
	//****************************************************************
	
	secsTotal = secsGraphs + secsAlphaVar + secsAlphaClau + secsDim + secsDib + secsMod + secsModBip;
	
	if(verbose){
		cerr << "Runtime = " << secsTotal << " secs" << endl;
		cerr << "***************************************" << endl;
	}

	if(fout != ""){
		FILE* f7 = fopen(fout.c_str(), "w");
		fprintf(f7, "#instances,time-buildGraphs,alphaVarExp,time-AlphaVar,alphaClauExp,time-AlphaClau,dim,time-dim,dim-bip,time-dimBip,mod,#comm-vig,time-mod,mod-bip,#comm-cvig,time-mod-bip,time-total\n");
		fprintf(f7, "%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%d,%f,%f,%d,%f,%f\n", fin, secsGraphs, alphavarexp, secsAlphaVar, alphaclauexp, secsAlphaClau, -polreg.first, secsDim, -polregB.first, secsDib, modularity, (int)c.ncomm,secsMod, modularity_bip, (int)c_bip.ncomm, secsModBip, secsTotal);
		fclose(f7);
	}else{	
		cout << "#instances,time-buildGraphs,alphaVarExp,time-AlphaVar,alphaClauExp,time-AlphaClau,dim,time-dim,dim-bip,time-dimBip,mod,#comm-vig,time-mod,mod-bip,#comm-cvigtime-mod-bip,time-total" << endl;
		cout << fin << "," << secsGraphs << "," << alphavarexp << "," << secsAlphaVar << "," << alphaclauexp << "," << secsAlphaClau << "," << -polreg.first << "," << secsDim << "," << -polregB.first << "," << secsDib << "," << modularity << "," << (int)c.ncomm << "," << secsMod << "," << modularity_bip << "," << (int)c_bip.ncomm << "," << secsModBip << ","  << secsTotal << endl;
	}
	
	//****************************************************************	

}

#endif
