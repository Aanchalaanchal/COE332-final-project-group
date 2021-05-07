# Deployment

Deploying the app to a kubernetes cluster involves several different deployment files. YAML files are provided in the /kubernetes/test directory for the flask API, flask service, redis database, redis service, redis persistent volume mount, 2 workers, and debug deployment. Using this app requires execing into the debug pod to interact with the api. 

## Installation
First, clone the project and access it. 
```bash
git clone https://github.com/SierraOG/coe332-final-project
cd coe332-final-project
```
The source files have already been containerized, although the Dockerfile is provided in /docker for future desired builds. 

## Deploy
There are six different deployments in the kubernetes/test directory. Since managing all of them can be cumbersome, a Makefile is provided to perform operations on them. To deploy to the kubernetes cluster, begin by verifying that your cluster doesn't contain any existing deployments from this app using 
```
make kube-get_all
```
This will get all pods, deployments, services, and pvc's. If there is no existing deployment of this project, initialize it by running 
```
make kube-init
```
After all containers and services are running, check the IP addresses of final-api-service-test and final-db-service-test using
``` 
make kube-get_all
```
The IP addresses of the services will likely be different from the ones listed in the environment variables of the deployment files. Go to /kubernetes/test/api-deployment and find the flask_IP and redis_IP values. Replace them if they are different than your current IP addresses.

Once the IP addresses are fixed, we can restart in the deployments using
```
make kube-restart_deployments
```
which will delete all deployments and restart them. Once restarted, the fixes will be applied and the app should be fully functional and ready to be used.
