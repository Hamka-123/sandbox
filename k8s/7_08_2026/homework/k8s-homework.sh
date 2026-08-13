#!/bin/bash

# Exit immediately if any command fails
set -e

echo "=== 0. Checking Minikube status ==="
minikube status || minikube start


echo -e "\n=== 1. Creating Pod, Dry-Run and YAML Manifests ==="

echo "A) Running imperative pod via 'kubectl run' (nginx)..."
kubectl run nginx-temp --image=nginx:alpine --dry-run=client -o yaml > pod.yaml
echo "Manifest successfully generated and saved to pod.yaml"

echo "B) Displaying the contents of pod.yaml:"
cat pod.yaml

echo "C) Creating the Pod from the saved YAML file..."
kubectl apply -f pod.yaml

echo "Checking the status of the created pod:"
kubectl get pod nginx-temp


echo -e "\n=== 2. Creating ReplicaSet and Testing Self-Healing ==="

# Creating a temporary manifest for the ReplicaSet
cat <<EOF > rs.yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: test-replicaset
spec:
  replicas: 2
  selector:
    matchLabels:
      app: homework-app
  template:
    metadata:
      labels:
        app: homework-app
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
EOF

echo "Applying the ReplicaSet manifest..."
kubectl apply -f rs.yaml

echo "Waiting 3 seconds for the pods to start..."
sleep 3

echo "Viewing current ReplicaSet pods:"
kubectl get pods -l app=homework-app

echo -e "\n--- Deleting one pod to test ReplicaSet Self-Healing ---"
POD_TO_KILL=$(kubectl get pods -l app=homework-app -o jsonpath='{.items[0].metadata.name}')
echo "Deleting pod: $POD_TO_KILL"
kubectl delete pod "$POD_TO_KILL"

echo "Viewing pods immediately after deletion (controller should spin up a new one):"
sleep 2
kubectl get pods -l app=homework-app 

echo -e "\n--- Trying to manually add an 'extra' pod with the same labels ---"
kubectl run extra-pod --image=nginx:alpine --labels="app=homework-app" --restart=Never
sleep 2
echo "Checking controller reaction (extra pod should be terminated, count should return to 2):"
kubectl get pods -l app=homework-app


echo -e "\n=== 3. JSONPath Practice ==="
echo "Extracting only pod names via jsonpath:"
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}'

echo -e "\nExtracting pairs [Pod Name -> Container Image]:"
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name} --> {.spec.containers[*].image}{"\n"}{end}'


echo -e "\n=== 4. Bonus Task: Deploying Go Application from GHCR ==="
GO_IMAGE="ghcr.io/hamka-123/go-web-app:latest"

echo "Running Go application from image: $GO_IMAGE"
kubectl delete pod go-app --ignore-not-found=true
kubectl run go-app --image="$GO_IMAGE" --port=8080

echo "Waiting for pod to start (up to 15 seconds)..."
kubectl wait --for=condition=Ready pod/go-app --timeout=15s || echo "Pod is still starting up..."


echo -e "\n=== Done! Instructions for manual verification ==="
echo "1. Describe pod and replicaset:"
echo "   kubectl describe pod nginx-temp"
echo "   kubectl describe rs test-replicaset"
echo "2. View pod logs:"
echo "   kubectl logs go-app"
echo "3. Port forwarding (run in a separate terminal):"
echo "   kubectl port-forward pod/go-app 8080:8080"
echo "4. Accessing inside the Go application container:"
echo "   kubectl exec -it go-app -- /bin/sh or kubectl exec -it go-app -- /bin/bash if available in the image"
echo "   kubectl debug -it go-app --image=busybox:latest --target=go-app if the image is minimal and secure"
echo "5. Clean up resources:"
echo "   kubectl delete -f pod.yaml -f rs.yaml"
echo "   kubectl delete pod nginx-temp go-app extra-pod"
echo "   rm -f pod.yaml rs.yaml"