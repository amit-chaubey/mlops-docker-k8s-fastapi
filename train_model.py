"""
Train an Iris dataset classification model and save it as a joblib file.
"""

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
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


def train_model(X_train, y_train):
    """Train a Random Forest classifier on the training data."""
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        max_depth=5
    )
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


def save_model(model, filepath='iris_model.joblib'):
    """Save the trained model to a joblib file."""
    joblib.dump(model, filepath)
    print(f"\nModel saved to {filepath}")
    return filepath


def main():
    """Main function to orchestrate model training."""
    print("Loading Iris dataset...")
    X, y, feature_names, target_names = load_data()
    
    print(f"Dataset shape: {X.shape}")
    print(f"Features: {feature_names}")
    print(f"Classes: {target_names}\n")
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Test set size: {X_test.shape[0]}\n")
    
    # Train the model
    print("Training Random Forest classifier...")
    model = train_model(X_train, y_train)
    
    # Evaluate the model
    print("\nEvaluating model...")
    evaluate_model(model, X_test, y_test, target_names)
    
    # Save the model
    model_path = save_model(model)
    
    print(f"\nTraining complete! Model saved to {model_path}")


if __name__ == "__main__":
    main()
