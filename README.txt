================================================================================
DOCKER SETUP AND COMMANDS FOR IRIS ML MODEL
================================================================================

This file contains Docker-specific instructions and commands for building,
running, and managing the Iris ML model container.

================================================================================
PREREQUISITES
================================================================================

1. Docker installed and running on your system
2. Dockerfile present in the project root
3. Model file (iris_model.joblib) must exist before building
4. Project structure must have an 'app' directory with serve.py inside

================================================================================
PROJECT STRUCTURE FOR DOCKER
================================================================================

Before building the Docker image, ensure your project structure is:

mlops-iris-ml/
├── Dockerfile
├── requirements.txt
├── iris_model.joblib
└── app/
    └── serve.py

IMPORTANT: The serve.py file must be inside the app/ directory for Docker.

================================================================================
SETUP STEPS
================================================================================

Step 1: Create the app directory structure
------------------------------------------
mkdir -p app

Step 2: Move or copy serve.py to app directory
----------------------------------------------
cp serve.py app/serve.py
# OR if serve.py needs to be created, ensure it's in app/serve.py

Step 3: Ensure iris_model.joblib exists
----------------------------------------
python train_model.py
# This creates iris_model.joblib in the root directory

Step 4: Copy model file to app directory (if needed)
-----------------------------------------------------
cp iris_model.joblib app/iris_model.joblib
# OR update Dockerfile to copy from root

================================================================================
DOCKER COMMANDS
================================================================================

1. BUILD THE DOCKER IMAGE
--------------------------
docker build -t iris-ml-model:latest .

Description: Builds a Docker image named 'iris-ml-model' with tag 'latest'
             from the current directory (where Dockerfile is located)

Alternative tags:
docker build -t iris-ml-model:v1.0 .
docker build -t iris-ml-model:dev .


2. RUN THE DOCKER CONTAINER
----------------------------
docker run -d -p 8000:8000 --name iris-api iris-ml-model:latest

Description: 
  -d: Run in detached mode (background)
  -p 8000:8000: Map container port 8000 to host port 8000
  --name iris-api: Name the container 'iris-api'
  iris-ml-model:latest: Use the image we built

Run in foreground (see logs):
docker run -p 8000:8000 --name iris-api iris-ml-model:latest


3. CHECK CONTAINER STATUS
--------------------------
docker ps

Description: List all running containers

View all containers (including stopped):
docker ps -a


4. VIEW CONTAINER LOGS
----------------------
docker logs iris-api

Description: View logs from the container named 'iris-api'

Follow logs in real-time:
docker logs -f iris-api

View last N lines:
docker logs --tail 50 iris-api


5. STOP THE CONTAINER
----------------------
docker stop iris-api

Description: Gracefully stop the running container


6. START A STOPPED CONTAINER
-----------------------------
docker start iris-api

Description: Start a previously stopped container


7. RESTART THE CONTAINER
-------------------------
docker restart iris-api

Description: Restart the container (stop and start)


8. REMOVE THE CONTAINER
-----------------------
docker rm iris-api

Description: Remove a stopped container

Force remove (even if running):
docker rm -f iris-api


9. REMOVE THE IMAGE
-------------------
docker rmi iris-ml-model:latest

Description: Remove the Docker image

Force remove:
docker rmi -f iris-ml-model:latest


10. EXECUTE COMMANDS INSIDE CONTAINER
--------------------------------------
docker exec -it iris-api /bin/bash

Description: Open an interactive bash shell inside the running container

Execute a single command:
docker exec iris-api ls -la /code


11. INSPECT CONTAINER DETAILS
------------------------------
docker inspect iris-api

Description: Get detailed information about the container


12. VIEW CONTAINER RESOURCE USAGE
----------------------------------
docker stats iris-api

Description: Monitor CPU, memory, and network usage in real-time


================================================================================
TESTING THE API
================================================================================

Once the container is running, test the API endpoints:

1. Test root endpoint:
   curl http://localhost:8000/

2. Test prediction endpoint:
   curl -X POST "http://localhost:8000/predict" \
        -H "Content-Type: application/json" \
        -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'

3. Access API documentation:
   Open browser: http://localhost:8000/docs
   (FastAPI provides automatic interactive API documentation)


================================================================================
TROUBLESHOOTING
================================================================================

Problem: Container exits immediately
Solution: Check logs with 'docker logs iris-api'
         Common issues: Missing model file, import errors, port conflicts

Problem: Port 8000 already in use
Solution: Use a different port mapping:
         docker run -d -p 8001:8000 --name iris-api iris-ml-model:latest
         Then access at http://localhost:8001

Problem: Cannot find module 'app.serve'
Solution: Ensure serve.py is in app/ directory and Dockerfile copies it correctly

Problem: Model file not found
Solution: Ensure iris_model.joblib exists and is copied to the container
         Check Dockerfile COPY commands

Problem: Permission denied errors
Solution: Check file permissions and Dockerfile user settings


================================================================================
COMPLETE WORKFLOW EXAMPLE
================================================================================

# 1. Train the model
python train_model.py

# 2. Set up directory structure
mkdir -p app
cp serve.py app/serve.py
cp iris_model.joblib app/iris_model.joblib

# 3. Build Docker image
docker build -t iris-ml-model:latest .

# 4. Run container
docker run -d -p 8000:8000 --name iris-api iris-ml-model:latest

# 5. Check if running
docker ps

# 6. Test API
curl http://localhost:8000/

# 7. View logs
docker logs iris-api

# 8. Stop when done
docker stop iris-api

# 9. Clean up (optional)
docker rm iris-api
docker rmi iris-ml-model:latest


================================================================================
DOCKER COMPOSE (OPTIONAL)
================================================================================

If you prefer using docker-compose, create a docker-compose.yml file:

version: '3.8'
services:
  iris-api:
    build: .
    ports:
      - "8000:8000"
    container_name: iris-api
    restart: unless-stopped

Then use:
docker-compose up -d          # Start services
docker-compose down           # Stop and remove services
docker-compose logs -f        # View logs
docker-compose ps             # Check status


================================================================================
NOTES
================================================================================

- The Dockerfile uses Python 3.11 base image
- The container exposes port 8000
- The working directory inside container is /code
- Model file path in serve.py should match container structure
- For production, consider adding health checks and resource limits
- Use environment variables for configuration in production deployments

================================================================================
