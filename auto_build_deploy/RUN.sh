#!/bin/bash

# ###########################################################
# AUTO BUILD & DEPLOY APPLICATION
#
# The DataRobot project, model and deployment comnfiguration 
# details will be written to the file results_config.yaml (4th param)

python auto_build_deploy.py ../data/test_data.csv outcome AutoBuildTest results_config.yaml True

cat results_config.yaml
 
