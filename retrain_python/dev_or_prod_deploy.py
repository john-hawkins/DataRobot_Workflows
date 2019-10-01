# Create a project, take a single blueprint and run a model based off it, then
# deploy that model. This is intended to illustrate what might happen in a
# production environment, after having experimented and chosen a blueprint in a
# dev or analytics environment.
#
# This scripts assumes a yaml config file exists: 'datarobot_config.yaml'
# containing the path to DataRobot, and your token:
# endpoint: https://app.datarobot.com/api/v2/
# token: not-my-real-token
#
# NOTE: need package datarobot>=2.17.0 for deployment creation

import datarobot as dr
import logging
import pandas as pd
import pickle

# optional script logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s: %(message)s',
    filename='deploy.log',
    filemode='w',
    level=logging.INFO)

dr.Client(config_path='datarobot_config.yaml')

################################################################################
# project creation

# config options can be parametrised outside this script
project_name = 'delays2013_prod'
data_path = 'logan-US-2013.csv'
target = 'was_delayed'
metric = 'AUC'
eval_set = 'validation'
deploy_description = 'Retrained model for flight delays'
logging.info('project name: %s', project_name)
logging.info('project data: %s', data_path)
logging.info('project target: %s', target)
logging.info('project metric: %s', metric)
logging.info('project evaluation set: %s', eval_set)

# read from a local file
df = pd.read_csv(data_path)

# make the same project, with the same settings as the original train script
project = dr.Project.create(df, project_name=project_name)
featurelist = project.create_featurelist('myfeatures', list(df.columns.values))

# run in manual model
logging.info('setting project target')
project.set_target(
    target=target,
    featurelist_id=featurelist.id,
    metric=metric,
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
logging.info('training blueprint: %s', new_bp.model_type)
job = project.train(new_bp, sample_pct=80, source_project_id=project.id)
model = dr.models.modeljob.wait_for_async_model_creation(project.id, job)

# optionally log model performance
logging.info('%s %s: %.3f', eval_set, metric, model.metrics[metric][eval_set])

# optionally set prediction threshold for binary classification
roc = model.get_roc_curve(eval_set)
threshold = roc.get_best_f1_threshold()
logging.info('setting prediction threshold to: %.3f', threshold)
model.set_prediction_threshold(threshold)
conf = roc.estimate_threshold(threshold)
logging.info('%s true positives: %.1f', eval_set, conf['true_positive_score'])
logging.info('%s true negatives: %.1f', eval_set, conf['true_negative_score'])
logging.info('%s false positives: %.1f', eval_set, conf['false_positive_score'])
logging.info('%s false negatives: %.1f', eval_set, conf['false_negative_score'])

# optionally output top features
impact = model.get_or_request_feature_impact()
impact.sort(key=lambda x: x['impactNormalized'], reverse=True)
for i in range(5):
    logging.info('feature impact %d: name="%s" impact=%.3f', i + 1,
                 impact[i]['featureName'], impact[i]['impactNormalized'])

################################################################################
# replace or create a deployment

# check if deployment already exists
deployments = [d for d in dr.Deployment.list() if d.label == project_name]

# replace an existing deployment if one exists, note the reason can be changed
if len(deployments) == 1:
    logging.info('replacing model in existing deployment')
    deployment = deployments[0]
    deployment.replace_model(
        model.id, dr.enums.MODEL_REPLACEMENT_REASON.SCHEDULED_REFRESH)
else:
    # get an available prediction server (the first one in this case)
    prediction_server = dr.PredictionServer.list()[0]
    # create a new deployment
    logging.info('creating new deployment')
    deployment = dr.Deployment.create_from_learning_model(
        model.id,
        label=project_name,
        description=deploy_description,
        default_prediction_server_id=prediction_server.id)

# get id for use by downstream applications
# ideally this would be stored somewhere
logging.info('deployment id: %s', deployment.id)
