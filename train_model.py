"""
Train an Iris dataset classification model and save it as a joblib file.
"""

import argparse
import os
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import joblib


def load_data():
    """Load the Iris dataset."""
    iris = load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names
    target_names = iris.target_names

    return X, y, feature_names, target_names


MODEL_CONFIG = {
    "rf": {
        "name": "Random Forest",
        "model": RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            max_depth=5,
        ),
    },
    "svc": {
        "name": "Support Vector Classifier",
        "model": SVC(kernel="linear", C=1.0, probability=True, random_state=42),
    },
}


def train_model(model_name, X_train, y_train):
    """Train the selected classifier on the training data."""
    config = MODEL_CONFIG[model_name]
    model = config["model"]
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test, target_names):
    """Evaluate the model and print performance metrics."""
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print(f"Model Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=target_names))

    return accuracy


def save_model(model, model_name, output_dir="."):
    """Save the trained model to a joblib file."""
    os.makedirs(output_dir, exist_ok=True)
    filename = f"iris_model_{model_name}.joblib"
    filepath = os.path.join(output_dir, filename)
    joblib.dump(model, filepath)
    print(f"\nModel saved to {filepath}")
    return filepath


def parse_args():
    parser = argparse.ArgumentParser(description="Train an Iris classification model.")
    parser.add_argument(
        "--model",
        choices=["rf", "svc", "all"],
        default="rf",
        help="Which model to train: rf, svc, or all.",
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.2,
        help="Test set fraction.",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory to save trained joblib model files.",
    )
    return parser.parse_args()


def train_and_save(model_name, X_train, y_train, X_test, y_test, target_names, output_dir):
    config = MODEL_CONFIG[model_name]
    print(f"Training {config['name']} classifier...")
    model = train_model(model_name, X_train, y_train)
    print("\nEvaluating model...")
    evaluate_model(model, X_test, y_test, target_names)
    return save_model(model, model_name, output_dir)


def main():
    args = parse_args()

    print("Loading Iris dataset...")
    X, y, feature_names, target_names = load_data()

    print(f"Dataset shape: {X.shape}")
    print(f"Features: {feature_names}")
    print(f"Classes: {target_names}\n")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=args.test_size,
        random_state=42,
        stratify=y,
    )

    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}\n")

    saved_paths = []
    if args.model == "all":
        for model_name in ["rf", "svc"]:
            saved_paths.append(
                train_and_save(
                    model_name,
                    X_train,
                    y_train,
                    X_test,
                    y_test,
                    target_names,
                    args.output_dir,
                )
            )
    else:
        saved_paths.append(
            train_and_save(
                args.model,
                X_train,
                y_train,
                X_test,
                y_test,
                target_names,
                args.output_dir,
            )
        )

    print("\nTraining complete!")
    print("Saved models:")
    for path in saved_paths:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
