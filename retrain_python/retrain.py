# Example workflow script to:
# Create a project and run autopilot
# Take the best blueprint and retrain that approach on a new project
# Create a deployment using this newly created model
#
# This scripts assumes a yaml config file has been created at:
# '~/.config/datarobot/drconfig.yaml'
#
# containing the path to DataRobot, and your token:
# endpoint: https://app.datarobot.com/api/v2/
# token: not-my-real-token
#
# NOTE: need package datarobot>=2.17.0 for deployment creation

import pandas as pd
import datarobot as dr
import pickle

################################################################################
# project creation

# from a local file
data_path = 'logan-US-2013.csv'
df = pd.read_csv(data_path)
df.head()

# create a project from a dataset, this can also be a filepath directly or a url
project = dr.Project.create(df, project_name='delays2013')

################################################################################
# options

# see available metrics (optional)
project.get_metrics('was_delayed')['available_metrics']

# custom feature lists (optional)
featurelist = project.create_featurelist('myfeatures', list(df.columns.values))

# for other advanced options see the docs, e.g.
# https://datarobot-public-api-client.readthedocs-hosted.com/en/v2.16.0/autodoc/api_reference.html#advanced-options-api

# run autopilot
project.set_target(
    target='was_delayed',
    featurelist_id=featurelist.id,
    metric='AUC',
    mode=dr.AUTOPILOT_MODE.FULL_AUTO,
    worker_count=-1)
project.wait_for_autopilot()

################################################################################
# model selection

# get leaderboard
lb = project.get_models()
# filter to models we will consider, in this case everything with a CV score
valid_models = [m for m in lb if m.metrics[project.metric]['crossValidation']]
# top model from CV, that maximises AUC
best_model = max(
    valid_models, key=lambda m: m.metrics[project.metric]['crossValidation'])

# get top blueprint id
best_bp = best_model.blueprint_id

# extract top blueprint object
bp = [bp for bp in project.get_blueprints() if bp.id == best_bp][0]

# serialize this and store somewhere
pickle.dump(bp, open('bp.pkl', 'wb'))

################################################################################
# run top blueprint in a new project
# note: if this is done in a new environment, you'd want a new config pointing
# to the install location

# make the same project, with the same settings
project = dr.Project.create(df, project_name='delays2013_prod_similar')
featurelist = project.create_featurelist('myfeatures', list(df.columns.values))
# run in manual model
project.set_target(
    target='was_delayed',
    featurelist_id=featurelist.id,
    metric='AUC',
    mode=dr.AUTOPILOT_MODE.MANUAL,
    worker_count=1)
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
# create a deployment

# get an available prediction server
prediction_server = dr.PredictionServer.list()[0]

# create a deployment
deployment = dr.Deployment.create_from_learning_model(
    model.id,
    label='delays2013',
    description='Retrained model for flight delays',
    default_prediction_server_id=prediction_server.id)

# get id to for use by downstream applications
deployment.id
