# k8s-autoscaler-sqs
K8S deployment autoscaler based on AWS SQS queue size  

## Status
Beta  

## Usage
Create a Kubernetes deployment yaml like this:
```
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: kub-sqs-autoscaler
spec:
  revisionHistoryLimit: 1
  replicas: 1
  template:
    metadata:
      labels:
        app: kub-sqs-autoscaler
    spec:
      containers:
      - name: kub-sqs-autoscaler
        image: $(DOCKER_IMAGE_REPOSITORY)  # required
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
