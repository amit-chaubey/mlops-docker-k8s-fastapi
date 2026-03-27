"""
Iris ML Model - Streamlit UI
Calls one or more Iris classifier FastAPI backends.

Configuration (pick one):
  - IRIS_MODEL_ENDPOINTS: JSON object mapping display label -> API base URL, e.g.
    {"Default":"http://iris-api:8000","Random Forest":"http://iris-api-rf:8000"}
  - Else IRIS_API_URL: single API base URL (legacy; one implicit "Default" backend).
"""

from __future__ import annotations

import json
import os
from typing import Any

import requests
import streamlit as st

# Page config (must be first Streamlit command)
st.set_page_config(
    page_title="Iris Classifier",
    page_icon="🌸",
    layout="centered",
)


def load_model_endpoints() -> dict[str, str]:
    """Single source for backend map: labels -> base URLs (no trailing slash)."""
    raw = os.getenv("IRIS_MODEL_ENDPOINTS", "").strip()
    if raw:
        try:
            data: Any = json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"IRIS_MODEL_ENDPOINTS must be valid JSON: {e}") from e
        if not isinstance(data, dict) or not data:
            raise ValueError("IRIS_MODEL_ENDPOINTS must be a non-empty JSON object")
        out: dict[str, str] = {}
        for k, v in data.items():
            if not isinstance(k, str) or not isinstance(v, str):
                raise ValueError("IRIS_MODEL_ENDPOINTS keys and values must be strings")
            out[k] = v.rstrip("/")
        return out
    single = os.getenv("IRIS_API_URL", "http://localhost:8000").rstrip("/")
    return {"Default": single}


def post_predict(base_url: str, payload: dict[str, float], timeout: float = 5.0) -> str:
    """POST /predict; returns prediction string or raises requests exception."""
    url = f"{base_url}/predict"
    r = requests.post(url, json=payload, timeout=timeout)
    r.raise_for_status()
    body = r.json()
    pred = body.get("prediction", "unknown")
    return str(pred)


# --- Bootstrap config once per session ---
try:
    _ENDPOINTS = load_model_endpoints()
except ValueError as e:
    st.error(str(e))
    st.stop()

_LABELS = list(_ENDPOINTS.keys())


# Main title and description
st.title("🌸 Iris Flower Classifier")
st.markdown("Enter sepal and petal measurements to predict the iris species.")

if len(_LABELS) > 1:
    choice = st.selectbox("Model backend", options=_LABELS, key="iris_model_backend")
else:
    choice = _LABELS[0]

base_url = _ENDPOINTS[choice]

# Input sliders (typical Iris ranges)
col1, col2 = st.columns(2)
with col1:
    sepal_length = st.slider("Sepal length (cm)", 4.0, 8.0, 5.8, 0.1)
    sepal_width = st.slider("Sepal width (cm)", 2.0, 4.5, 3.0, 0.1)
with col2:
    petal_length = st.slider("Petal length (cm)", 1.0, 7.0, 4.4, 0.1)
    petal_width = st.slider("Petal width (cm)", 0.1, 2.5, 1.3, 0.1)

if st.button("Predict", type="primary"):
    payload = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }
    try:
        prediction = post_predict(base_url, payload)
        st.success(f"**Predicted species:** {prediction.capitalize()}")
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to the **{choice}** backend. Is that API running and reachable from this app?")
        st.caption(
            "Docker: check the service is up on the same network. "
            "Local dev: run uvicorn and set IRIS_MODEL_ENDPOINTS or IRIS_API_URL so the URL matches."
        )
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")

hint = (
    "Backends are configured with IRIS_MODEL_ENDPOINTS (JSON) or a single IRIS_API_URL."
    if len(_LABELS) == 1
    else "Each backend is a separate deployment; URLs come from IRIS_MODEL_ENDPOINTS."
)
st.caption(hint)

# Footer
version = os.getenv("APP_VERSION", "1.0.0")
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    f"""
    <div style="text-align: center; color: #6b7280; margin-top: 20px; font-size: 14px;">
        <p><strong>HectorLabs</strong> · Built by <a href="https://www.amitchoubey.dev/" target="_blank" style="color: #6b7280;"><strong>Amit Choubey</strong></a></p>
        <p><a href="https://www.hectorlabs.co.uk" target="_blank" style="color: #6b7280;">hectorlabs.co.uk</a></p>
        <p style="margin-top: 12px;"><strong>Version:</strong> {version}</p>
    </div>
    """,
    unsafe_allow_html=True,
)
