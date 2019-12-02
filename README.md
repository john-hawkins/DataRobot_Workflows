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

[retrain_python](retrain_python/README.md)

## API_Workflow_EndtoEnd 

Example in Python for a step by step process to Build, deploy and get predictions from DataRobot via API. Most of the code here leverages retrain_python but updated with the latest changes from DataRobot. This code is particularly relevant for systems where the DataRobot Prediction environment is isolated and the DRX file cannot be transfered to it. The prediction environment is a DataRobot Standalone Instance.

1. [Model Training.py]()
   
   Builds the model and save the winning BluePrint. Runs it on Autopilot but selects a model that isn't a Blender. 

2. [Model Deployment.py]()

   Retrains the winning model BluePrint built in the Development area. We have to obtain the model artificats from step 1 above, to the prediction environment where prediction outputs will flow downstream. The outputs (model and predictions) should be exactly the same here and in DEV. But yet to verify this.... 

3. [Get Predictions.py]()

   Now that we have replicated the model in the prediction environment, we can now get predictions by submitting a new dataset. This is a test to ensure that the predictions does indeed return and in an expected format.

4. [4.Model_Monitoring_Management.py]()

    We can get predictions via the REST API route as well, so this script allows you to run this script on the command line anywhere as long as you're on the web and have DataRobot Credentials. An example of how to run: 
    ```
    python API_Workflow_EndtoEnd/4.Model_Monitoring_Management.py "retrain_python/logan-US-2014.csv"
    ```

## Add Actuals to a DataRobot Deployment

After a DataRobot deployment is used to make predictions against records, you can monitor performance by feeding back actual outcomes once they become known.

[add_actuals.py](add_actuals.py)



## Automated Model Build & Deploy 

A python command line application that will take a training data set location and a target column and run a
DataRobot Autopilot. Optional parameter to auto-deploy.

[auto_build_deploy](auto_build_deploy/README.md)

