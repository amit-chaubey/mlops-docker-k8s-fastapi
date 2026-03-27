# Iris Classifier - Streamlit UI

Calls one or more **FastAPI** Iris classifier backends. URLs are set at deploy time (not hard-coded in the app).

## Configuration

| Variable | Purpose |
|----------|---------|
| `IRIS_MODEL_ENDPOINTS` | JSON object: `{ "Label": "http://host:port", ... }`. Multiple entries → **Model backend** dropdown. |
| `IRIS_API_URL` | Used only if `IRIS_MODEL_ENDPOINTS` is unset; single backend named `Default`. |

Example (Docker internal DNS):

```text
IRIS_MODEL_ENDPOINTS={"Default":"http://iris-api:8000","Random Forest":"http://iris-api-rf:8000","SVC":"http://iris-api-svc:8000"}
```

## Option 1: Full stack with Docker Compose (recommended)

From the **project root**:

```bash
docker compose up -d
```

- **API:** http://localhost:8000 (`akatyayana/iris-ml-model:latest`)
- **UI:** http://localhost:8501 (`IRIS_MODEL_ENDPOINTS` with one `Default` backend)

### Multiple models (RF + SVC images on Hub)

```bash
docker compose -f docker-compose.yml -f docker-compose.variants.yml --profile variants up -d
```

Override images if needed: `IRIS_RF_IMAGE`, `IRIS_SVC_IMAGE`.

If you see **container name already in use**, an old container is still on the host. Remove it, then bring the stack up again:

```bash
docker rm -f iris-api-rf iris-api-svc 2>/dev/null; docker compose -f docker-compose.yml -f docker-compose.variants.yml --profile variants up -d
```

## Option 2: Run UI only (API already running)

From **this folder**:

```bash
pip install -r requirements.txt
export IRIS_API_URL=http://localhost:8000
streamlit run app.py
```

## Option 3: UI container, API on host

```bash
docker build -t iris-streamlit-ui .
docker run -p 8501:8501 -e IRIS_API_URL=http://host.docker.internal:8000 iris-streamlit-ui
```

Use `IRIS_MODEL_ENDPOINTS` when pointing at several deployments.
