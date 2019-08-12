# Create a project, take a single blueprint and run a model based off it,
# then deploy that model.
#
# This scripts assumes a yaml config file exists: 'datarobot_config.yaml'
# containing the path to DataRobot, and your token:
# endpoint: https://app.datarobot.com/api/v2/
# token: not-my-real-token
#
# NOTE: need package datarobot>=2.17.0 for deployment creation

import pandas as pd
import datarobot as dr
import pickle

dr.Client(config_path='datarobot_config.yaml')

################################################################################
# project creation

# from a local file
data_path = 'logan-US-2013.csv'
df = pd.read_csv(data_path)

# make the same project, with the same settings as the original train script
project = dr.Project.create(df, project_name='delays2013_prod')
featurelist = project.create_featurelist('myfeatures', list(df.columns.values))
# run in manual model
project.set_target(
    target='was_delayed',
    featurelist_id=featurelist.id,
    metric='AUC',
    mode=dr.AUTOPILOT_MODE.MANUAL,
    worker_count=1)

################################################################################
# retrain best model

# read original blueprint
old_bp = pickle.load(open('bp.pkl', 'rb'))

## Different options for retraining a blueprint
#
# get a blueprint that is of the same type, but could have different feature engineering
# new_bp = [bp for bp in project.get_blueprints() if old_bp.model_type == bp.model_type][0]
#
# get a blueprint of the same type and with the same feature engineering
# new_bp = [bp for bp in project.get_blueprints() if old_bp.processes == bp.processes][0]
#
# retrain exactly the same model, requires project settings and dataset to be exactly the same
new_bp = old_bp
#
## End

# train new blueprint on 80%
job = project.train(new_bp, sample_pct=80, source_project_id=project.id)
model = dr.models.modeljob.wait_for_async_model_creation(project.id, job)

# optionally set prediction threshold for binary classification
roc = model.get_roc_curve('crossValidation')
threshold = roc.get_best_f1_threshold()
model.set_prediction_threshold(threshold)

################################################################################
# replace or create a deployment

# check if deployment already exists
deployments = [d for d in dr.Deployment.list() if d.label == 'delays2013']

# replace an existing deployment if one exists, note the reason can be changed
if len(deployments) == 1:
    deployment = deployments[0]
    deployment.replace_model(model.id, dr.enums.MODEL_REPLACEMENT_REASON.SCHEDULED_REFRESH)
else:
    # get an available prediction server (the first one in this case)
    prediction_server = dr.PredictionServer.list()[0]
    # create a new deployment
    deployment = dr.Deployment.create_from_learning_model(
        model.id,
        label='delays2013',
        description='Retrained model for flight delays',
        default_prediction_server_id=prediction_server.id)

# get id for use by downstream applications
# ideally this would be stored somewhere
print(deployment.id)
