#!/bin/sh
set -e

docker build --build-arg MODEL_FILE=iris_model_rf.joblib -t iris-api:rf .
docker build --build-arg MODEL_FILE=iris_model_svc.joblib -t iris-api:svc .
