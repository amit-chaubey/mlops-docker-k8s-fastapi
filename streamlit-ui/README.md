# Iris Classifier - Streamlit UI

Simple UI for the Iris ML model. It calls the **FastAPI** Iris classifier API for predictions. Works locally and in Docker (API URL set via `IRIS_API_URL`).

## Option 1: Full stack with Docker Compose (recommended)

From the **project root** (not this folder):

```bash
docker-compose up -d
```

- **API:** http://localhost:8000 (image: `akatyayana/iris-ml-model:latest`)
- **UI:** http://localhost:8501 (Streamlit; uses `IRIS_API_URL=http://iris-api:8000` inside Docker)

## Option 2: Run UI only (API already running)

Ensure the Iris API is running (e.g. `uvicorn main:app --port 8000` or Docker on port 8000). Then from **this folder**:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501. Default API URL is `http://localhost:8000` (overridable in the sidebar).

## Option 3: Run Streamlit in Docker, API elsewhere

Build and run the UI container; point it at the API with `IRIS_API_URL`:

```bash
docker build -t iris-streamlit-ui .
docker run -p 8501:8501 -e IRIS_API_URL=http://host.docker.internal:8000 iris-streamlit-ui
```

Use `http://host.docker.internal:8000` if the API runs on the host; use `http://iris-api:8000` if running with docker-compose.

## Settings

- **API Base URL**: In the sidebar you can override the URL. In Docker Compose it is set by `IRIS_API_URL` so the UI talks to the `iris-api` service by name.
