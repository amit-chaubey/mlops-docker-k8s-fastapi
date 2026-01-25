# Iris Dataset ML Model

A complete MLOps project for training, saving, and serving an Iris flower classification model using scikit-learn, FastAPI, and Docker.

## Project Overview

This project implements a machine learning pipeline for classifying Iris flowers into three species (Setosa, Versicolor, Virginica) based on four features: sepal length, sepal width, petal length, and petal width.

## Features

- **Model Training**: Train a Random Forest classifier on the Iris dataset
- **Model Persistence**: Save trained models using joblib
- **API Service**: FastAPI-based REST API for model predictions
- **Docker Support**: Containerized deployment with Docker
- **Evaluation Metrics**: Comprehensive model performance evaluation

## Project Structure

```
mlops-iris-ml/
├── train_model.py          # Model training script
├── create_model.py         # Minimal model creation script
├── serve.py                # FastAPI application (move to app/serve.py for Docker)
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker container configuration
├── iris_model.joblib      # Trained model file (generated)
├── README.md              # This file - GitHub documentation
└── README.txt             # Docker-specific instructions
```

## Prerequisites

- Python 3.11 or higher
- pip package manager
- Docker (optional, for containerized deployment)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mlops-iris-ml
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Training the Model

Train the model and save it as a joblib file:

```bash
python train_model.py
```

This script will:
1. Load the Iris dataset
2. Split data into training (80%) and test (20%) sets
3. Train a Random Forest classifier with 100 estimators
4. Evaluate model performance with accuracy and classification report
5. Save the trained model as `iris_model.joblib`

### Using the Model Directly

Load and use the saved model in Python:

```python
import joblib
import numpy as np

# Load the model
model = joblib.load('iris_model.joblib')

# Make predictions
# Features: [sepal length, sepal width, petal length, petal width]
sample = np.array([[5.1, 3.5, 1.4, 0.2]])
prediction = model.predict(sample)
print(f"Predicted class: {prediction[0]}")
```

### Running the API Server

For local development, ensure `serve.py` is in the root directory:

```bash
uvicorn serve:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

**API Endpoints:**

- `GET /` - Welcome message
- `POST /predict` - Make predictions

**Example prediction request:**

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

**Response:**
```json
{
  "prediction": "setosa"
}
```

### Docker Deployment

See `README.txt` for detailed Docker commands and setup instructions.

## Dataset Information

The Iris dataset contains:
- **150 samples** with 4 features each
- **Features**: Sepal length, Sepal width, Petal length, Petal width
- **Classes**: Setosa, Versicolor, Virginica (50 samples each)

## Model Details

- **Algorithm**: Random Forest Classifier
- **Parameters**:
  - `n_estimators`: 100
  - `max_depth`: 5
  - `random_state`: 42
- **Expected Accuracy**: ~96-100% on test set

## Dependencies

- `scikit-learn>=1.3.0` - Machine learning library
- `joblib>=1.3.0` - Model serialization
- `fastapi>=0.115.6` - Web framework for API
- `numpy>=1.26.0` - Numerical computing
- `uvicorn>=0.34.0` - ASGI server

## Development

### Project Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Testing

Test the model training:
```bash
python train_model.py
```

Test the API locally:
```bash
python -m uvicorn serve:app --reload
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Author

Created as part of an MLOps project for Iris flower classification.
