# k8s-controller-sqs-autoscaler
Kubernetes deployment autoscale controller based on AWS SQS queue size.  

## Features
- Auto scale-up, scale-down Kubernetes deployment's replicas count based on queue size  


# Technology stack
- Python 3.6+
- boto3 - for AWS integration


# Requirements and dependencies
## Application
Python libs requirements in requirements.txt

## External
Kubernetes instance


# Configuration
## Variables
| Name | Required | Values | Default | Description |
|:----------|:-------------|:------|:------|:------|
|AWS_REGION|True|||AWS region name|
|AWS_ID|True|||AWS account id|
|SQS_QUEUE|True|||AWS sqs name|
|KUBERNETES_DEPLOYMENT|True|||Kubernetes deployment name for scaling|
|KUBERNETES_NAMESPACE|True|||Kubernetes namespace|


# Usage
Apply a Kubernetes deployment configuration:
```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: controller-sqs-autoscaler
spec:
  revisionHistoryLimit: 1
  replicas: 1
  template:
    metadata:
      labels:
        app: controller-sqs-autoscaler
    spec:
      containers:
      - name: controller-sqs-autoscaler
        image: vfabi/k8s-controller-sqs-autoscaler
        command:
          - ./k8s-app
          - --sqs-queue-url=https://sqs.$(AWS_REGION).amazonaws.com/$(AWS_ID)/$(SQS_QUEUE)  # required
          - --kubernetes-deployment=$(KUBERNETES_DEPLOYMENT)  # required
          - --kubernetes-namespace=$(KUBERNETES_NAMESPACE)  # required
          - --aws-region=us-west-2  # required
          - --poll-period=10  # optional
          - --scale-down-cool-down=30  # optional
          - --scale-up-cool-down=10  # optional
          - --scale-up-messages=20  # optional
          - --scale-down-messages=10  # optional
          - --max-pods=30  # optional
          - --min-pods=1  # optional
        env:
          - name: K8S_NAMESPACE
            valueFrom:
              fieldRef:
                fieldPath: metadata.namespace
        resources:
          requests:
            memory: "64Mi"
            cpu: "250m"
          limits:
            memory: "1512Mi"
            cpu: "500m"
        ports:
        - containerPort: 80
```


# Docker
[![Generic badge](https://img.shields.io/badge/hub.docker.com-vfabi/k8s_controller_sqs_autoscaler-<>.svg)](https://hub.docker.com/repository/docker/vfabi/k8s-controller-sqs-autoscaler)  


# Contributing
Please refer to each project's style and contribution guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!


# License
Apache 2.0