#!/usr/bin/python

import os
import sys
import yaml
import contextlib
import datarobot as dr

#################################################################################
def main():
    if len(sys.argv) < 3:
        print("*** ERROR: MISSING ARGUMENTS *** ")
        print_usage(sys.argv)
        exit(1)
    else:
        file_loc = (sys.argv[1])
        target = (sys.argv[2])
        project_name = (sys.argv[3])
        out_file = (sys.argv[4])

        if len(sys.argv) > 5: 
            deploy = (sys.argv[5])

        deploy_id=""

        project_id, model_id = run_project(file_loc, target, project_name)

        if deploy=="True":
            deploy_id = deploy_model(project_id, model_id, project_name)

        # FINALLY WRITE TO DISK
        dict_file = {'project_id' : project_id, 'model_id' :model_id, 'deployment_id' : deploy_id}
        with open(out_file, 'w') as file:
            documents = yaml.dump(dict_file, file, default_flow_style=False)

#################################################################################
def print_usage(args):
    print("USAGE ")
    print(args[0], "<PATH TO TRAINING DATA> <TARGET COLUMN NAME> <PROJECT NAME> <RESULTS YAML FILE> (<DEPLOY> DEFAULT=False)")
    print()
    print("Run the DataRobot Autopilot")
    print()

#################################################################################
# RUN THE DATAROBOT PROJECT
#################################################################################
def run_project(file_loc, target, project_name):
            project = dr.Project.create(file_loc, project_name=project_name, max_wait=2000, read_timeout=2000) 
            project.set_target(target = target, mode = dr.AUTOPILOT_MODE.FULL_AUTO, worker_count = -1)
            project.wait_for_autopilot()
            ##################################################################################
            # HERE WE ARE TAKING THE DATAROBOT RECOMMENDED MODEL -- BEST CV SCORE NON-BLENDER
            best_model = dr.ModelRecommendation.get(project.id).get_model()
            return (project.id, best_model.id)


#################################################################################
# DEPLOY THE MODEL 
# NOTE: This script assumes each project_name will have only a single associated
#       deployment. It will replace an existing deployment if one is found.
#################################################################################
def deploy_model(project_id, model_id, project_name):
            deployments = [d for d in dr.Deployment.list() if d.label == project_name]

            # REPLACE IF FOUND
            if len(deployments) == 1:
                deployment = deployments[0]
                deployment.replace_model(model_id, dr.enums.MODEL_REPLACEMENT_REASON.SCHEDULED_REFRESH)
            else:
                # CREATE NEW DEPLOYMENT 
                prediction_server = dr.PredictionServer.list()[0]
                deployment = dr.Deployment.create_from_learning_model(
                    model_id,
                    label=project_name,
                    default_prediction_server_id=prediction_server.id
                )
            return deployment.id 


#################################################################################
if __name__ == "__main__": main()


