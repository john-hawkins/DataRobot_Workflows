#!/bin/bash

# ###########################################################
# EXAMPLE RUN OF THE AUTO BUILD & DEPLOY APPLICATION
# THE RETURNED VALUES ARE CAPTURED IN THE VARIABLE 'results'
#

results=($(python auto_build_deploy.py "../data/test_data.csv" "outcome" "AutoBuildTest" True))

echo ${results[0]}
echo ${results[1]}
echo ${results[2]}



