# Kubernetes-



apiVersion: eksctl.io/v1alpha5
kind: ClusterConfig

metadata:
  name: basic-cluster-t3
  region: us-east-2

nodeGroups:
  - name: ng-2
    instanceType: t3.small
    desiredCapacity: 2
___
cd  Reloader
kubectl apply -f https://raw.githubusercontent.com/stakater/Reloader/master/deployments/kubernetes/reloader.yaml
