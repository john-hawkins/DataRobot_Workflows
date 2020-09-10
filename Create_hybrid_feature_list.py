# #####################################################################
# CREATE A NEW FEATURE LIST BY TAKING:
# - THE TOP N FEATURES USED 
# - OF THE TOP Z MODELS ON THE LEADERBOARD
# - AND THE SELECTING ONLY THOSE FEATURES ON ALL LISTS
# ###########################################################################
library(datarobot)

# SET THE VARIABLES
# We need the identifiers for the existing project
project_id    		<- '5b19f64fdb03716d1a23be8b'

FeaturesPerModel 	<- 10
ModelsToUse		<-3

# GET THE DATAROBOT OBJECTS
project         	<- GetProject(project_id)
models          	<- ListModels(project)

compositeList 		<- c()
for (i in 1:ModelsToUse) {
    compositeList[[i]] 	<-  models[[i]].ListModelFeatures() 


result = tryCatch({
    expr
}, warning = function(w) {
    warning-handler-code
}, error = function(e) {
    error-handler-code
}, finally = {
    cleanup-code
}

}
 
featureImpactJobId <- RequestFeatureImpact(models[[i]])
featureImpact <- GetFeatureImpactForJobId(project, featureImpactJobId)

