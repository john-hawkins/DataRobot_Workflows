# #####################################################################
# Create a DataRobot Project and force cross validation and holdout
#
# Assumes that you have DataRobot authentication set up with a YAML file
#
# ###########################################################################
library(datarobot)

#
# SET THE VARIABLES FOR THE WORKFLOW

projName		<- "Test_Workflow_Project"
target			<- "outcome"
maxWorkers		<- 4
cvFolds			<- 5
holdoutPercentage	<- 20

df 		<- read.csv('test_data.csv')

project  	<- SetupProject( dataSource=df, projectName=projName )

#
# SET-UP THE PARTITIONS

partition 	<- CreateRandomPartition("CV", holdoutPct = holdoutPercentage, reps = cvFolds)

SetTarget(project=project, target=target, partition = partition, mode = 'quick')
 
UpdateProject(project = project$projectId, workerCount = maxWorkers, holdoutUnlocked = TRUE)

WaitForAutopilot(project = project)
 

