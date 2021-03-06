# Retraining a single model for deployment in a separate environment

This folder is intended to demonstrate an example workflow where there are
different DataRobot environments intended for development and production. This
will often be the case in large enterprises.

Note that the scripts themselves are intended to be used as examples, in
reality you would apply your own business logic to customise these to your own
use cases.

## Workflow

The structure of the workflow looks like:

1. In a development environment
    * Create a project by importing your dataset
    * Run autopilot to create models
    * Choose the best model based on your business criteria
    * Export the blueprint of the best model, so that it can be retrained and
      deployed in prod
2. In the production environment
    * Create a project by importing the same dataset as in dev
    * Run manual mode
    * Train a single model based on the blueprint from dev
    * Deploy this model either as a new deployment, or updating an existing
      deployment if it exists

## Running

Update `drconfig.yaml` with your credentials and the location of DataRobot
installation.

Create a project in dev, train and select best model using:

```{bash}
python dev_train.py
```

This script creates a `bp.pkl` artifact that represents the best model.

Deploy this best model in your dev or your prod environment using:

```{bash}
python dev_or_prod_deploy.py
```

This script assumes that `drconfig.yaml` and `bp.pkl` exist in the current working directory.

## Assumptions:

* This script assumes data is available in the same location for both
  development and production environments, in reality the location of the model
  training data may have to be parametrised across different environments
* The assumption is that a DataRobot config file with credentials can be made
  available when deploying in production, along with a model artifact, and the
  production script itself
