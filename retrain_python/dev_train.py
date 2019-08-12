# Create a project, run autopilot, and select the best model.
#
# This scripts assumes a yaml config file exists: 'datarobot_config.yaml'
# containing the path to DataRobot, and your token:
# endpoint: https://app.datarobot.com/api/v2/
# token: not-my-real-token

import pandas as pd
import datarobot as dr
import pickle

dr.Client(config_path='datarobot_config.yaml')

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
# https://datarobot-public-api-client.readthedocs-hosted.com/en/v2.17.0/autodoc/api_reference.html#advanced-options-api

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

