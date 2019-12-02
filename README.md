# DataRobot_Workflows

Examples of how to build custom workflows in DataRobot

Use the DataRobot API and set up alternative data partitioning schemes before training models

 
## Cross Validation and Holdout

Example in R of how to set up specific CV folds and Holdout percentage when running a project

[CV_and_Holdout.R](CV_and_Holdout.R)
 

## Retrain a Model

Example in R of how to get the Blueprint ID from an existing project, and then re-train that model
using a new dataset.

[Retrain_a_model.R](Retrain_a_model.R)


## retrain_python

Example in Python of retraining a blueprint on a new project, potentially in a separate prod environment.

[retrain_python/retrain.py](retrain_python/retrain.py)


## Add Actuals to a DataRobot Deployment

After a DataRobot deployment is used to make predictions against records, you can monitor performance by feeding back actual outcomes once they become known.

[add_actuals.py](add_actuals.py)


## Automated Model Build & Deploy 

A python command line application that will take a training data set location and a target column and run a
DataRobot Autopilot. Optional parameter to auto-deploy.

[auto_build_deploy/README.md](auto_build_deploy/README.md)


