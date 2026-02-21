# Push checklist: what to commit and which workflows run

## Quick reference: path → workflow

- **API image** builds when: `main.py`, `train_model.py`, `create_model.py`, `requirements.txt`, `Dockerfile`, `data/processed/**`, `data/cleaned/**`, `iris_model.joblib`
- **Streamlit image** builds when: `streamlit-ui/app.py`, `streamlit-ui/Dockerfile`, `streamlit-ui/requirements.txt`
- **No image** build: README, .github/*, docker-compose, k8s, monitoring, data/raw, etc.
