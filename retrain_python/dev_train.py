# Create a project, run autopilot, and export the blueprint for the best model.
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

# run autopilot with more accurate models
project.set_target(
    target='was_delayed',
    featurelist_id=featurelist.id,
    metric='AUC',
    advanced_options=dr.AdvancedOptions(accuracy_optimized_mb=True),
    mode=dr.AUTOPILOT_MODE.FULL_AUTO,
    worker_count=-1)
project.wait_for_autopilot()

# run a custom model - e.g. Fasttext word embeddings
blueprints = project.get_blueprints()
fasttext = [bp for bp in blueprints if any('Fasttext' in p for p in bp.processes)]
for f in fasttext:
    job = project.train(f, sample_pct=64, source_project_id=project.id, scoring_type=dr.enums.SCORING_TYPE.cross_validation)
    model = dr.models.modeljob.wait_for_async_model_creation(project.id, job)

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
# additional metrics that may be useful for storing and comparing to prod deploy

# get additional information for the best model
best_model.metrics

# get best prediction threshold for the f1 score, and print metrics
roc = model.get_roc_curve('crossValidation')
threshold = roc.get_best_f1_threshold()
roc.estimate_threshold(threshold)

# examine feature impact
model.get_or_request_feature_impact()
