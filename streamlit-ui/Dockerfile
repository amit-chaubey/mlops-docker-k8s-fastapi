# Streamlit UI for Iris Classifier - calls FastAPI backend
# API URL at runtime: set IRIS_API_URL (e.g. http://iris-api:8000 in docker-compose)

FROM python:3.11-slim

WORKDIR /app

COPY . . 

RUN pip install --no-cache-dir -r requirements.txt


# Streamlit default port
EXPOSE 8501

# Allow override via env when running container
ENV IRIS_API_URL=http://localhost:8000

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
