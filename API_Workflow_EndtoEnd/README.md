# Steps to reproduce result

In order to reproduce the results, there are key setups that needs to be done before running the script in the order. 
 
## Install required 
- Download and install Python 3 
- Clone or fork this repository
- fill in the .yaml file. Use your own API token and other credentials 
- Initiate terminal from this repository at the parent level and: 
    - Install python environment here

    ```python3 -m venv API_Workflow_EndtoEnd/new_env```
    - Activate the environment once installed
    
    ```source API_Workflow_EndtoEnd/new_env/bin/activate```
- Intall required libraries:
    
    ```pip install -r API_Workflow_EndtoEnd/requirements.txt```
- Activate python

    ```python```

## Run scripts  
Do not run the script outright. Open up each of the scripts and step through executing the code. This is to ensure the user understand what is happening. The order are: 
1. [Model Training.py]()
2. [Model Deployment.py]()
3. [Get Predictions.py]()
4. [4.Model_Monitoring_Management.py]

### 1. Model Training 
This will load a csv file and run the Autopilot in DataRobot. The only custom selection here is using 'AUC' as the optimisation metric. Upon finishing, a pickle file of the model for serialisation, and a .json file is created to store information about our model so we can choose the correct model for deployment in a seperate independent process (ie. Starting a new session but wanting to retrieve the previously ran model, or going into a different environment and trying to replicate the same outputs)

### 2. Model Deployment 
Simlar process is repeated like in step 1 except, we DO NOT use autopilot. Instead, we run a manual selection of the Model Blueprint that we did in step 1 above. We're doing this because we want to replicate the same outcome as in Step 1. And because we kept the pickle model, we will read it and obtain the correct BluePrints to run. After running the model, we deploy it. 

Upon deployment, a .json file is created to store information about our model so we can choose the correct model for scoring in the next process. 

### 3. Get Predictions 
Here we select a new data that we would like to get predictions for, and we submit the file to DataRobot. Note that this is similar to doing a batch prediction via the GUI (ie. is not via API). The model deployed will also appear in the Deployment tab

### 4. Model Monitoring Management 
Here we use the DataRobot standard REST API where we send a payload (the data) and we get the results back, which is a list of predictions. You need the use your DataRobot credentials which you will need to update in the script, and you need to run this script from the command line. Here's a example of how you would run it: 
```
python API_Workflow_EndtoEnd/4.Model_Monitoring_Management.py "retrain_python/logan-US-2014.csv"
```
For more information visit the official [DataRobot API documentation](https://datarobot-public-api-client.readthedocs-hosted.com/en/v2.18/)

## TODO
Make a single script that executes end to end seperately (as opposed to a step by step process)
Refactor the script 
Create a seperate custom model and load to DataRobot (Customer Inference Model)
