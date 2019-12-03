Auto Build & Deploy Model
-------------------------

This project contains a standalone python application that will execute 
a DataRobot autopilot and return the project and model id. In addition
it can automatically deploy the recommended model, replacing an existing
deployment where one exists.

You will be able to use this script as a starting point to customise your
own autopilot run and model selection criteria.

## Requirements

This script requires that you have a valid DataRobot account.

It uses Python 3.

It requires that you have the DataRobot python package installed.

It requires that you have a YAML configuration file setup to authenticate 
against your DataRobot server.

## Instructions

See the [RUN.sh](RUN.sh) script for a usage example.

