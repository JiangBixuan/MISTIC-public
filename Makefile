#.PHONY: X_clean 1_create_environment 2_dl_raw_data 3_dl_training_sets 4_prepare_data requirements

#################################################################################
# GLOBALS                                                                       #
#################################################################################


PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = MISTIC-public
PYTHON_INTERPRETER = python


ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Set up python interpreter environment
create_environment:
ifeq (True,$(HAS_CONDA))
	@echo ">>> Detected conda, creating conda environment."
	conda env create --name $(PROJECT_NAME) --file=.MISTIC-public.yml
	conda activate MISTIC-public

endif
	@echo ">>> New conda env created. Activate with:\nconda activate $(PROJECT_NAME)"

dl_data_clinvar_and_training_sets:
ifeq (default,$(PROFILE))
	rsync -auP ssh.lbgi.fr:/gstock/biolo_datasets/variation/benchmark/Databases/clinvar/clinvar_20180930_annot.vcf.gz data/raw/deleterious
	rsync -auP ssh.lbgi.fr:/gstock/biolo_datasets/variation/benchmark/MISTIC/TRAINING_SETS/* data/raw/training_sets

endif

dl_data_gnomad:
ifeq (default,$(PROFILE))
	rsync -auP ssh.lbgi.fr:/gstock/biolo_datasets/variation/gnomAD/latest/vcf/exomes/gnomad.exomes.r2.1.1.sites.vcf.bgz data/raw/population
endif

dl_mistic_pickle_models:
ifeq (default,$(PROFILE))
	rsync -auP ssh.lbgi.fr:/gstock/biolo_datasets/variation/benchmark/MISTIC/WEBSITE_DATA/MODELS/* models
endif

dl_mistic_test:
ifeq (default,$(PROFILE))
	rsync -auP ssh.lbgi.fr:/gstock/biolo_datasets/variation/benchmark/MISTIC/WEBSITE_DATA/pandas_path_mistic_test.csv.gz data/processed
endif

## Prepare RAW data by applying filters
prepare_data: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset.py

train:
	$(PYTHON_INTERPRETER) MISTIC.py --train_and_test -i data/examples/pandas_mini_training.csv.gz -e data/examples/pandas_mini_eval.csv.gz



## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete




#################################################################################
# PROJECT RULES                                                                 #
#################################################################################



#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
