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

## TODO
Test the get predictions by running it on a different computer

Make a single script that executes end to end 

Test run the REST API route for getting predictions. The MMM will record activity