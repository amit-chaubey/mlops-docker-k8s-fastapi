from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

# Load model
model = joblib.load("iris_model.joblib")

class_names = np.array(["setosa", "versicolor", "virginica"])

app = FastAPI(
    title="Iris Classifier",
    description="Classify iris flowers into three species"
)

# ✅ Request schema (THIS fixes your error)
class IrisRequest(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


@app.get("/")
def root():
    return {"message": "Welcome to the Iris Classifier API"}


@app.post("/predict")
def predict(data: IrisRequest):
    features = np.array(
        [[
            data.sepal_length,
            data.sepal_width,
            data.petal_length,
            data.petal_width
        ]],
        dtype=float
    )

    prediction = model.predict(features)[0]

    return {
        "prediction": class_names[int(prediction)]
    }
