# #####################################################################
# RETRAIN AN EXISTING MODEL WITH NEW DATA
# - Load an existing project and model
# - Copy the blueprint and retrain with a new dataset
#
# Assumes that you have DataRobot authentication set up with a YAML file
# Assumes that you are using a new dataset in which the target variable
#  has the same name.
# Assumes that you are using the default feature list 
# - This can be changed but requires more work
# ###########################################################################
library(datarobot)

# SET THE VARIABLES
# We need the identifiers for the existing project and model
project_id 	<- '5b19f64fdb03716d1a23be8b'
model_id 	<- '5b19f67d621c1e742150cacc'
newdata		<- 'test_data.csv'

# GET THE BLUEPRINT ID
project 	<- GetProject(project_id)
model		<- GetModel(project, model_id) 
blueprint	<- model$blueprintId
targ_col	<- model$projectTarget
metric		<- model$projectMetric

# CREATE A NEW PROJECT
newproj		<- SetupProject(dataSource=newdata, projectName="RETRAIN_TEST")
SetTarget(project=newproj, target=targ_col, mode='manual', metric=metric)
newproj_id	<- newproj$projectId

# NOW TRAIN THAT MODEL
totrain			<- list()
# THIS PART IS A BIT COUNTER-INTUITIVE 
# - YOU NEED THE PROJECT_ID FROM THE ORIGINAL PROJECT
totrain$projectId 	<- project_id
totrain$blueprintId 	<- blueprint
jobid			<- RequestNewModel(newproj_id, totrain)
model 			<- GetModelFromJobId(newproj, jobid)


#####################################################################
# SAME FUNCTIONALITY WRAPPED INSIDE A REUSABLE FUNCTION
# RETURN THE PROJECT AND MODEL ID FOR THE NEW PROJECT
##################################################################
retrainModel    <- function(project_id, model_id, newdata, newprojectname) {
   project         	<- GetProject(project_id)
   model           	<- GetModel(project, model_id)
   blueprint       	<- model$blueprintId
   targ_col        	<- model$projectTarget
   metric          	<- model$projectMetric
   newproj         	<- SetupProject(dataSource=newdata, projectName=newprojectname)
   SetTarget(project=newproj, target=targ_col, mode='manual', metric=metric)
   newproj_id      	<- newproj$projectId
   totrain           	<- list()
   totrain$projectId 	<- project_id
   totrain$blueprintId	<- blueprint
   jobid          	<- RequestNewModel(newproj_id, totrain)
   model 		<- GetModelFromJobId(newproj, jobid)
   results  		<- list()
   results$projectId	<- newproj_id
   results$modelId  	<- model$modelId
   return(results)
}


