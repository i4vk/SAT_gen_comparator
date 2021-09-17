SOLVERS_DIR = solvers
BIN_DIR = $(SOLVERS_DIR)/bin
MAPLESAT_DIR = $(SOLVERS_DIR)/MapleSAT/simp
GLUCOSE_DIR = $(SOLVERS_DIR)/glucose-syrup-4.1/simp
CADICAL_DIR = $(SOLVERS_DIR)/cadical-master
LINGELING_DIR = $(SOLVERS_DIR)/lingeling-bcj-78ebb86-180517
MAPLE_LCM_CHRONO = $(SOLVERS_DIR)/MapleLCMDiscChronoBT-DL-v3
GRAPH_FEATURES_DIR = GraphFeatures


all: cadical glucose maplesat lingeling maple-lcm-chrono graph-features

dir_target:
	mkdir -p $(BIN_DIR)

permission:
	cd $(CADICAL_DIR) && chmod a+x configure && chmod a+x scripts/make-build-header.sh
	cd $(MAPLE_LCM_CHRONO) && chmod a+x starexec_build
	cd $(LINGELING_DIR) && chmod a+x configure.sh && chmod a+x mkconfig.sh

cadical: dir_target permission
	cd $(CADICAL_DIR) && ./configure && $(MAKE)
	cp $(CADICAL_DIR)/build/cadical $(BIN_DIR)/cadical

glucose: dir_target
	cd $(GLUCOSE_DIR) && $(MAKE) rs
	cp $(GLUCOSE_DIR)/glucose_static $(BIN_DIR)/glucose

maplesat: dir_target
	cd $(MAPLESAT_DIR) && export MROOT=../ && $(MAKE) rs
	cp  $(MAPLESAT_DIR)/maplesat_static $(BIN_DIR)/maplesat

lingeling: dir_target permission
	cd $(LINGELING_DIR) && ./configure.sh && $(MAKE)
	cp  $(LINGELING_DIR)/lingeling $(BIN_DIR)/lingeling

maple-lcm-chrono: dir_target permission
	cd $(MAPLE_LCM_CHRONO) && ./starexec_build
	cp $(MAPLE_LCM_CHRONO)/bin/MapleLCMDistChrBt-DL-v3 $(BIN_DIR)/MapleLCMDistChrBt-DL-v3
	chmod a+x $(BIN_DIR)/MapleLCMDistChrBt-DL-v3

graph-features:
	cd $(GRAPH_FEATURES_DIR) && $(MAKE)

clean: permission
	rm -rf $(BIN_DIR)
	cd $(CADICAL_DIR) && ./configure && $(MAKE) clean
	cd $(GLUCOSE_DIR) && $(MAKE) clean
	cd $(MAPLESAT_DIR) && export MROOT=../ && $(MAKE) clean
	cd $(LINGELING_DIR) && ./configure.sh && $(MAKE) clean
	cd $(MAPLE_LCM_CHRONO)/sources/simp && $(MAKE) clean
	cd $(GRAPH_FEATURES_DIR) && $(MAKE) clean


