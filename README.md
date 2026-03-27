# 🌸 Iris ML Model - Production-Ready MLOps Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5.svg?logo=kubernetes&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-ECR%20%7C%20EKS-FF9900.svg?logo=amazon-aws&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**🚀 A complete, production-ready MLOps pipeline for Iris flower classification**

*From local development to cloud deployment - Everything you need for scalable ML inference*

[![Docker Image](https://img.shields.io/badge/Docker%20Hub-akatyayana%2Firis--ml--model-blue?logo=docker&style=for-the-badge)](https://hub.docker.com/r/akatyayana/iris-ml-model)

**[👉 Click here to use the Docker image directly on Docker Hub 👈](https://hub.docker.com/r/akatyayana/iris-ml-model)**

[Features](#-features) • [Quick Start](#-quick-start) • [Docker Hub](#-docker-hub) • [Kubernetes](#-kubernetes) • [AWS Deployment](#-aws-deployment)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Docker Hub](#-docker-hub)
- [Local Development](#-local-development)
- [Kubernetes with Minikube](#-kubernetes-with-minikube)
- [AWS Deployment](#-aws-deployment)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)

---

## 🎯 Overview

This is a **complete, enterprise-grade MLOps solution** for deploying machine learning models at scale. Built with modern best practices, this project demonstrates the full lifecycle of ML model deployment:

- ✅ **Model Training & Versioning** - Reproducible model training pipeline
- ✅ **Containerization** - Docker-based deployment
- ✅ **Local K8s Testing** - Minikube integration for local Kubernetes testing
- ✅ **Cloud Deployment** - AWS ECR + EKS production deployment
- ✅ **RESTful API** - FastAPI-based inference service
- ✅ **Production Ready** - Scalable, secure, and monitored

**Perfect for:** Data Scientists, ML Engineers, DevOps Engineers, and anyone looking to deploy ML models in production!

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 **ML Model** | Random Forest classifier with 96-100% accuracy |
| 🐳 **Dockerized** | Pre-built image available on Docker Hub |
| ☸️ **K8s Ready** | Tested with Minikube for local Kubernetes |
| ☁️ **Cloud Native** | AWS ECR/EKS deployment ready |
| 🚀 **FastAPI** | High-performance async API framework |
| 📊 **Production Grade** | Scalable, secure, and production-tested |
| 🔄 **CI/CD Ready** | Easy integration with GitHub Actions, GitLab CI, etc. |

---

## 🏗️ Architecture

```
┌─────────────────┐
│  Model Training │
│   (Local/Python) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Docker Build   │
│  & Push to Hub  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌─────────────────┐
│  Minikube Test  │ ───▶ │  AWS ECR Push   │
│  (Local K8s)    │      │  (Container Reg)│
└─────────────────┘      └────────┬────────┘
                                   │
                                   ▼
                            ┌─────────────────┐
                            │  AWS EKS Deploy │
                            │  (Production)   │
                            └─────────────────┘
```

---

## 🚀 Quick Start

### Use Pre-built Docker Image (Recommended)

**[👉 Get the Docker image from Docker Hub 👈](https://hub.docker.com/r/akatyayana/iris-ml-model)**

The Docker image is **ready to use** - just pull and run:

```bash
docker run -d -p 8000:8000 --name iris-ml-api akatyayana/iris-ml-model:latest
```

Test it: `curl http://localhost:8000/`

**That's it!** Your ML API is running. Visit `http://localhost:8000/docs` for interactive API documentation.

### Full stack (API + Streamlit UI) with Docker Compose

Run both the FastAPI model API and the Streamlit UI in one go (API image from Docker Hub, UI built from `streamlit-ui/`):

```bash
docker-compose up -d
```

- **API:** http://localhost:8000/ (use trailing slash for root)  
- **Streamlit UI:** http://localhost:8501  

The UI reads `IRIS_MODEL_ENDPOINTS` (JSON map of labels to API base URLs) or falls back to `IRIS_API_URL`. For **default + RF + SVC** backends together, use `docker-compose.variants.yml` and profile `variants` (see `streamlit-ui/README.md`).

**Docker runtime:** Works with Docker Desktop, [Colima](https://github.com/abiosoft/colima), or any Docker-compatible context. Use `docker-compose` (with hyphen) if `docker compose` is not available (e.g. Colima with Compose V1).  
**Colima / older Buildx:** If you see *"compose build requires buildx 0.17.0 or later"*, run with the legacy builder: `DOCKER_BUILDKIT=0 docker-compose up -d`

---

## 🐳 Docker Hub

### [👉 Click to View & Use Docker Image on Docker Hub 👈](https://hub.docker.com/r/akatyayana/iris-ml-model)

**Quick Overview:**
- **Image:** `akatyayana/iris-ml-model:latest`
- **Size:** ~2GB | **Base:** Python 3.11 | **Port:** 8000
- **Status:** ✅ Production-ready, tested, and verified

**Benefits:**
- ✅ Instant deployment - no build time required
- ✅ One-command setup: `docker run -d -p 8000:8000 akatyayana/iris-ml-model:latest`
- ✅ Ready for Kubernetes, AWS ECS, EKS, and more

---

## 💻 Local Development

### 1. Train the Model

```bash
# Install dependencies
pip install -r requirements.txt

# Train and save the model
python train_model.py
```

This creates `iris_model.joblib` with a trained Random Forest classifier.

### 2. Run API Locally

```bash
# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://localhost:8000/docs` for interactive API documentation!

### 3. Test the API

```bash
# Health check
curl http://localhost:8000/

# Make a prediction
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

**Expected Response:**
```json
{
  "prediction": "setosa"
}
```

---

## ☸️ Kubernetes with Minikube

### Why Minikube?

**Minikube** allows you to test Kubernetes deployments locally before pushing to production. It's the perfect way to validate your containerized ML model in a real K8s environment!

### Prerequisites

```bash
# Install Minikube (macOS)
brew install minikube

# Or download from: https://minikube.sigs.k8s.io/docs/start/
```

### Step 1: Start Minikube

```bash
# Start Minikube cluster
minikube start

# Verify cluster is running
kubectl get nodes
```

### Step 2: Load Docker Image into Minikube

```bash
# Option A: Use pre-built image from Docker Hub
minikube image pull akatyayana/iris-ml-model:latest

# Option B: Build image directly in Minikube
eval $(minikube docker-env)
docker build -t iris-ml-model:latest .
```

### Step 3: Create Kubernetes Deployment

Create `k8s-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iris-ml-api
spec:
  replicas: 2
  selector:
    matchLabels:
      app: iris-ml-api
  template:
    metadata:
      labels:
        app: iris-ml-api
    spec:
      containers:
      - name: iris-ml-api
        # If using Option A (Docker Hub): use akatyayana/iris-ml-model:latest
        # If using Option B (local build): use iris-ml-model:latest and set imagePullPolicy: Never
        image: akatyayana/iris-ml-model:latest
        imagePullPolicy: IfNotPresent  # Use IfNotPresent for Docker Hub, or Never for local builds
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: iris-ml-service
spec:
  type: NodePort
  selector:
    app: iris-ml-api
  ports:
    - protocol: TCP
      port: 8000
      targetPort: 8000
      nodePort: 30080
```

### Step 4: Deploy to Minikube

```bash
# Apply the deployment
kubectl apply -f k8s-deployment.yaml

# Check deployment status
kubectl get deployments
kubectl get pods
kubectl get services

# Get service URL
minikube service iris-ml-service --url
```

### Step 5: Test the Deployment

```bash
# Get the service URL
SERVICE_URL=$(minikube service iris-ml-service --url)

# Test the API
curl $SERVICE_URL/

# Make a prediction
curl -X POST "$SERVICE_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

### Step 6: Monitor and Debug

```bash
# View logs
kubectl logs -f deployment/iris-ml-api

# Scale the deployment
kubectl scale deployment iris-ml-api --replicas=3

# View pod details
kubectl describe pod <pod-name>
```

### Cleanup

```bash
# Delete deployment
kubectl delete -f k8s-deployment.yaml

# Stop Minikube
minikube stop
```

---

## ☁️ AWS Deployment

### Complete MLOps Workflow: Local → AWS Production

This section covers the **complete production deployment** workflow from Docker Hub to AWS ECR and EKS.

### Prerequisites

- AWS CLI configured (`aws configure`)
- Docker (or Colima / other Docker-compatible runtime) installed
- kubectl installed
- AWS account with ECR and EKS access

### Step 1: Push Image to AWS ECR

**ECR (Elastic Container Registry)** is AWS's managed Docker registry service.

```bash
# 1. Create ECR repository
aws ecr create-repository \
  --repository-name iris-ml-model \
  --region us-east-1

# 2. Get login token
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# 3. Tag the image
docker tag iris-ml-model:latest \
  <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/iris-ml-model:latest

# 4. Push to ECR
docker push \
  <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/iris-ml-model:latest
```

**Or use the pre-built Docker Hub image:**

```bash
# Pull from Docker Hub
docker pull akatyayana/iris-ml-model:latest

# Tag for ECR
docker tag akatyayana/iris-ml-model:latest \
  <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/iris-ml-model:latest

# Push to ECR
docker push \
  <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/iris-ml-model:latest
```

### Step 2: Create EKS Cluster

**EKS (Elastic Kubernetes Service)** is AWS's managed Kubernetes service.

```bash
# 1. Create EKS cluster (this takes 10-15 minutes)
aws eks create-cluster \
  --name iris-ml-cluster \
  --version 1.28 \
  --role-arn arn:aws:iam::<ACCOUNT_ID>:role/EKSServiceRole \
  --resources-vpc-config \
    subnetIds=subnet-xxx,subnet-yyy \
    securityGroupIds=sg-xxx \
  --region us-east-1

# 2. Wait for cluster to be active
aws eks wait cluster-active --name iris-ml-cluster --region us-east-1

# 3. Configure kubectl
aws eks update-kubeconfig --name iris-ml-cluster --region us-east-1

# 4. Verify connection
kubectl get nodes
```

### Step 3: Deploy to EKS

Create `eks-deployment.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iris-ml-api
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: iris-ml-api
  template:
    metadata:
      labels:
        app: iris-ml-api
    spec:
      containers:
      - name: iris-ml-api
        image: <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/iris-ml-model:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: iris-ml-service
  annotations:
    service.beta.kubernetes.io/aws-load-balancer-type: "nlb"
spec:
  type: LoadBalancer
  selector:
    app: iris-ml-api
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
```

Deploy:

```bash
# Apply deployment
kubectl apply -f eks-deployment.yaml

# Check status
kubectl get deployments
kubectl get pods
kubectl get services

# Get LoadBalancer URL
kubectl get service iris-ml-service -o wide
```

### Step 4: Test Production Deployment

```bash
# Get the LoadBalancer URL from kubectl output
LB_URL=$(kubectl get service iris-ml-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

# Test the API
curl http://$LB_URL/

# Make predictions
curl -X POST "http://$LB_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

### Step 5: Monitor and Scale

```bash
# View logs
kubectl logs -f deployment/iris-ml-api

# Scale horizontally
kubectl scale deployment iris-ml-api --replicas=5

# View metrics (if metrics-server is installed)
kubectl top pods
```

---

## 📚 API Documentation

### Interactive API Docs

Once the service is running, visit:
- **Swagger UI:** `http://<host>:8000/docs`
- **ReDoc:** `http://<host>:8000/redoc`

### Endpoints

#### `GET /`
Health check endpoint.

**Response:**
```json
{
  "message": "Welcome to the Iris Classifier API"
}
```

#### `POST /predict`
Make predictions on Iris flower features.

**Request Body:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response:**
```json
{
  "prediction": "setosa"
}
```

**Possible predictions:** `setosa`, `versicolor`, `virginica`

---

## 📁 Project Structure

```
mlops-iris-ml/
├── main.py                 # FastAPI application (model API)
├── train_model.py          # Model training script
├── create_model.py         # Minimal model creation
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker image for FastAPI (pushed to Hub)
├── docker-compose.yml      # Full stack: default API + Streamlit UI
├── docker-compose.variants.yml  # Optional: RF + SVC API services + multi-backend UI
├── iris_model.joblib       # Trained model (generated)
├── k8s-deployment.yaml     # Kubernetes deployment (Minikube)
├── eks-deployment.yaml     # EKS deployment
├── streamlit-ui/           # Streamlit UI (calls FastAPI)
│   ├── app.py              # Streamlit app (IRIS_MODEL_ENDPOINTS / IRIS_API_URL)
│   ├── Dockerfile          # Streamlit image
│   └── requirements.txt
├── .github/workflows/      # CI: test first; then conditional image push (mlops.yml)
│   └── mlops.yml             # Tests + path-based Docker Hub publish after success
├── README.md               # This file
└── README.txt              # Docker commands reference
```

---

## 🔄 CI: Test Then Publish Images

Single workflow **MLOps Pipeline** (`.github/workflows/mlops.yml`):

1. **Always runs:** Docker Compose smoke test (API + Streamlit) on every **push** and **pull request** to `main` / `master`.
2. **After tests pass** (push only): optional publish jobs run from **changed paths** and **committed model files**:
   - **Default API** → `iris-ml-model:latest` (needs `iris_model.joblib` in repo).
   - **RF variant** → `iris-api:rf`, `iris-api:rf-latest` (needs `iris_model_rf.joblib`; train with `python train_model.py --model all` or `rf`).
   - **SVC variant** → `iris-api:svc` (needs `iris_model_svc.joblib`).
   - **Streamlit** → `iris-streamlit-ui:latest` when `streamlit-ui/app.py`, `Dockerfile`, or `requirements.txt` change (not `streamlit-ui/README.md` alone).

K8s, observability, `data/raw/**`, README-only changes, etc. do **not** trigger API/Streamlit builds.

**Required repo secrets:** `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` (Settings → Secrets and variables → Actions).

---

## 🧪 Model Details

- **Algorithm:** Random Forest Classifier
- **Dataset:** Iris (150 samples, 4 features, 3 classes)
- **Accuracy:** 96-100% on test set
- **Features:** Sepal length, Sepal width, Petal length, Petal width
- **Classes:** Setosa, Versicolor, Virginica

---

## 🛠️ Technology Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0+-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-326CE5?logo=kubernetes&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-ECR%20%7C%20EKS-FF9900?logo=amazon-aws&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?logo=scikit-learn&logoColor=white)

</div>

---

## 🚀 Deployment Options Summary

| Environment | Command | Use Case |
|------------|---------|----------|
| **Local Docker** | `docker run -p 8000:8000 akatyayana/iris-ml-model:latest` | Quick testing |
| **Minikube** | `kubectl apply -f k8s-deployment.yaml` | Local K8s testing |
| **AWS ECR + EKS** | Push to ECR → Deploy to EKS | Production deployment |

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**Amit Choubey**
- GitHub: [@amit-choubey](https://github.com/amit-chaubey)
- Project: [MLOps Docker K8s FastAPI](https://github.com/amit-chaubey/mlops-docker-k8s-fastapi)

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Containerized with [Docker](https://www.docker.com/)
- Orchestrated with [Kubernetes](https://kubernetes.io/)
- Deployed on [AWS](https://aws.amazon.com/)

---

<div align="center">

**⭐ Star this repo if you find it helpful! ⭐**

Made with ❤️ for the MLOps community

</div>
