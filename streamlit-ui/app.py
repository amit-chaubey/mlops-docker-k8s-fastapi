"""
Iris ML Model - Streamlit UI
Calls the Iris classifier FastAPI for predictions.
API URL from env: IRIS_API_URL (Docker: http://iris-api:8000, local: http://localhost:8000).
"""

import os
import streamlit as st
import requests

# Page config (must be first Streamlit command)
st.set_page_config(
    page_title="Iris Classifier",
    page_icon="🌸",
    layout="centered",
)

# API endpoint: from env (Docker image uses service name; local dev set IRIS_API_URL=http://localhost:8000)
api_endpoint = os.getenv("IRIS_API_URL", "http://iris-api:8000")
predict_url = f"{api_endpoint.rstrip('/')}/predict"

# Sidebar: show which API we're using
st.sidebar.header("Settings")
st.sidebar.caption(f"**API:** `{api_endpoint}`")
if not os.getenv("IRIS_API_URL"):
    st.sidebar.markdown("**Local dev:** API is not set, so app is trying `iris-api:8000` (Docker only).")
    st.sidebar.code("IRIS_API_URL=http://localhost:8004 streamlit run app.py", language="text")
    st.sidebar.caption("Use the same port as uvicorn (e.g. 8004). Restart Streamlit after setting.")

# Main title and description
st.title("🌸 Iris Flower Classifier")
st.markdown("Enter sepal and petal measurements to predict the iris species.")

# Input sliders (typical Iris ranges)
col1, col2 = st.columns(2)
with col1:
    sepal_length = st.slider("Sepal length (cm)", 4.0, 8.0, 5.8, 0.1)
    sepal_width = st.slider("Sepal width (cm)", 2.0, 4.5, 3.0, 0.1)
with col2:
    petal_length = st.slider("Petal length (cm)", 1.0, 7.0, 4.4, 0.1)
    petal_width = st.slider("Petal width (cm)", 0.1, 2.5, 1.3, 0.1)

# Predict button
if st.button("Predict", type="primary"):
    payload = {
        "sepal_length": sepal_length,
        "sepal_width": sepal_width,
        "petal_length": petal_length,
        "petal_width": petal_width,
    }
    try:
        response = requests.post(predict_url, json=payload, timeout=5)
        response.raise_for_status()
        result = response.json()
        prediction = result.get("prediction", "unknown")
        st.success(f"**Predicted species:** {prediction.capitalize()}")
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to API at **{api_endpoint}**. Check that the API is running.")
        st.caption(
            "**Docker:** ensure iris-api container is up. "
            "**Local:** run uvicorn (e.g. `uvicorn main:app --port 8004`) then start Streamlit with "
            "`IRIS_API_URL=http://localhost:8004 streamlit run app.py` (same port as uvicorn)."
        )
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {e}")

st.caption("Uses the Iris classifier API. Ensure the API is running at the URL shown in Settings.")

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
