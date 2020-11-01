# Build
## Prerequisites
* pyenv
* docker
* awscli
## Build commands
```
pyenv virtualenv 3.7.5 cloudwatch-pod-alerts-operator
pyenv activate cloudwatch-pod-alerts-operator
pip -r requirements.txt
make
```
This will create a docker image with the application in it and upload it to ECR.
Push the image into your repository of choice.

# Install the CRD 
The current CRD supports kubernetes <= 1.15. 
```
kubectl apply -f crd-v1beta1.yaml
```

# Setup RBAC
Setup roles and service account with needed permissions for the operator
```
kubectl apply -f rbac.yaml
```

# Deploy the operator
Edit the deployment yaml and change the repository where the image is located
```
kubectl apply -f deployment.yaml
```

# Test
## Local testing
You can test the operator without craeting a container and deploying it in kubernetes.
In order for this to work you need to uncommend lines 13-15 from src/handler.py
Make sure you export AWS_PROFILE, AWS_DEFAULT_REGION and choose your kubernetes context before that.
```
kopf run src/handler.py
```

## Create example alarm
Edit the example and replace the topics, namespace and cluster name

```
kubectl apply -f alarm.yaml

```
For your examples to work, the container needs to have IAM policy that allows it to access
cloudwatchlogs assigned ot it

# TODO
* Introduce parameters for cluster and region (currently region is hardcoded to us-west-2 for the creation of the cloudwatch alerts)
* Introduce a better kubernetes login mechanism to remove the need to uncomment the client authentication for local testing
