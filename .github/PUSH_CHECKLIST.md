# Push checklist

## CI flow (`mlops.yml`)

1. **Test** — Docker Compose stack + API + Streamlit smoke checks (every **push** and **PR** to `main` / `master`).
2. **Path filter** — On **push** only (after tests): decides if API vs Streamlit paths changed.
3. **API artifacts** — On **push** when API paths changed: after checkout, records which `.joblib` files exist (job-level `hashFiles()` is not used—it would see an empty workspace).
4. **Publish** — Matching build/push jobs run only when paths + artifact checks say so.

## Path → what gets built

| Changed paths | Publish job (if file exists) |
|---------------|------------------------------|
| Root **API** files: `main.py`, `train_model.py`, `create_model.py`, root `requirements.txt`, root `Dockerfile`, `data/processed/**`, `data/cleaned/**`, `iris_model*.joblib` | **API** images (see below) |
| `streamlit-ui/app.py`, `streamlit-ui/Dockerfile`, `streamlit-ui/requirements.txt` | **Streamlit** `iris-streamlit-ui` **only** (API jobs stay skipped) |
| `streamlit-ui/README.md`, `docker-compose*.yml`, `.github/**`, k8s yaml, root README, etc. | **No image** publish |

Workflow note: the `api` filter includes `!streamlit-ui/**` so UI-only Dockerfile/requirements changes do **not** match the `api` group (bare `Dockerfile` / `requirements.txt` would otherwise match every folder).

## API images (after tests pass)

| File in repo | Docker Hub tags (examples) |
|--------------|----------------------------|
| `iris_model.joblib` | `USER/iris-ml-model:latest`, `USER/iris-ml-model:<sha>` |
| `iris_model_rf.joblib` | `USER/iris-api:rf`, `USER/iris-api:rf-latest`, `USER/iris-api:rf-<sha>` |
| `iris_model_svc.joblib` | `USER/iris-api:svc`, `USER/iris-api:svc-latest`, `USER/iris-api:svc-<sha>` |

Generate RF + SVC artifacts locally:

```bash
python train_model.py --model all
```

Commit the `.joblib` files you want CI to bake into images.

## Secrets

Repository **Settings → Secrets and variables → Actions**:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## Removed workflows (consolidated into `mlops.yml`)

- `build-push-api.yml`, `build-push-streamlit.yml`, `dual-image-api.yaml` — logic merged into `mlops.yml` so **publish never runs before tests pass**.
