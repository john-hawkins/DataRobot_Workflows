"""
@author: Eu Jin Lok

Setup datadrift on deployment and feedback accuracy for tracking. This script will initialise a data drift tracker 
and feedback actuals to datarobot. Full documentation: 
https://datarobot-public-api-client.readthedocs-hosted.com/en/v2.18.0/entities/deployment.html#create-a-deployment


NOTE: 
- Items to bring to new environment 
    - requirement.txt                
    - config.yaml  
    - <this script>.py
- Python environment was used but not commited to repo. Initiate python environment on the terminal:
    python3 -m venv API_Workflow_EndtoEnd/new_env
    source API_Workflow_EndtoEnd/new_env/bin/activate
- Intall required libraries:
    pip install -r API_Workflow_EndtoEnd/requirements.txt 
- .yaml file not commited. Use your own API token and other credentials 
"""

######################################
# %% Import libraries and set the config path 
import sys, os
import pandas as pd
import datarobot as dr
from datarobot import Project, Deployment
from datarobot.enums import SERVICE_STAT_METRIC, ACCURACY_METRIC
import pickle
import requests
import json
import time 
print(sys.version)
dr.Client(config_path=os.getcwd()+'/API_Workflow_EndtoEnd/config.yaml')

with open('API_Workflow_EndtoEnd/Deployment_Creds.json') as f:
    param = json.load(f)

DATAROBOT_KEY = param['DATAROBOT_KEY']
API_KEY = param['API_KEY']
USERNAME = param['USERNAME']
DEPLOYMENT_ID = '5dbe5e49397e660046399f92'
MAX_PREDICTION_FILE_SIZE_BYTES = 52428800  # 50 MB


# Activate data drift 
deployment = dr.Deployment.get(deployment_id=DEPLOYMENT_ID)
deployment.update_drift_tracking_settings(target_drift_enabled=True, feature_drift_enabled=True)

# now check that it has been set
settings = deployment.get_drift_tracking_settings()
settings

# Get service stats 
# need to make sure there's some predictions submited in the last 7 days or it will error
service_stats = deployment.get_service_stats()
service_stats

# Total number of predictions stat
service_stats[SERVICE_STAT_METRIC.TOTAL_PREDICTIONS]

# Set datadrift 
deployment.update_drift_tracking_settings(target_drift_enabled=True, feature_drift_enabled=True)


# STEP 5: Assign an association ID to the deployment and set up drift tracking
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization':  f'Token {API_KEY}'
}

association_id_column_name = 'event_id'
BASE_URL = 'https://app.datarobot.com/api/v2'

def set_association_id(deployment_id, association_id, allow_missing_values=False):
    """Assigns the association ID for a deployment"""
    url = f'{BASE_URL}/modelDeployments/{deployment_id}/associationIdSettings/'
    
    data = {'allowMissingValues': allow_missing_values, 'columnName': association_id}
    
    resp = requests.patch(url, json=data, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

set_association_id(deployment.id, association_id_column_name, allow_missing_values=False)

# Now feedback actuals 


# Now lets check how much the accuracy has drifted
accuracy = deployment.get_accuracy()
accuracy[ACCURACY_METRIC.RMSE]

'''
from datetime import datetime

from datarobot.helpers.partitioning_methods import construct_duration_string
from datarobot.models import Deployment

service_stats = deployment.get_service_stats(
    start_time=datetime(2019, 8, 1, hour=15),
    end_time=datetime(2019, 8, 8, hour=15)
)
service_stats[SERVICE_STAT_METRIC.TOTAL_PREDICTIONS]
'''

# We can't get any metrics because we haven't submitted any predictions 

# Lets generate a simulated dataset for submission 

# lets create a seperate script that will generate a new file everyday