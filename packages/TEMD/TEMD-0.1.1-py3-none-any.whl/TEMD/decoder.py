#decoder.py
import requests

import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def train_runtime_error_model():
    print("Starting to train the runtime error model...")

    # Fetch the runtime error dataset
    dataset_url = "https://raw.githubusercontent.com/Sujaykharat/python-error-dataset/main/errors_dataset.json"
    response = requests.get(dataset_url)

    if response.status_code != 200:
        print(f"Failed to fetch the dataset. Status code: {response.status_code}")
        exit()

    try:
        # Try to parse the JSON response
        data = response.json()
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        exit()

    # Debug: print the type of data and the first few items to inspect
    print(f"Data type: {type(data)}")
    if isinstance(data, dict):
        print(f"First key in data: {list(data.keys())[0]}")
    else:
        print(f"Data content: {data}")

    # Ensure data is a dictionary (not a list)
    if not isinstance(data, dict):
        print("Expected data to be a dictionary of errors, but it's not. Exiting.")
        exit()

    # Prepare the data
    error_messages = []
    explanations = []

    # Iterate over the error types and extract the messages and explanations
    for error_type, details in data.items():
        if isinstance(details, dict):
            error_message = details.get('trigger_function', '')
            explanation = details.get('explanation', '')
            if error_message and explanation:
                error_messages.append(error_message)
                explanations.append(explanation)

    # Ensure that both error_messages and explanations are not empty
    if not error_messages or not explanations:
        print("Error messages or explanations are missing in the dataset. Exiting.")
        exit()

    # Split the data into training and testing sets
    print("Splitting the data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(error_messages, explanations, test_size=0.5, random_state=42)

    # Build a Random Forest model pipeline
    model = make_pipeline(TfidfVectorizer(), RandomForestClassifier())

    # Train the model
    print("Training the model...")
    try:
        model.fit(X_train, y_train)
        print("Model training completed.")
    except Exception as e:
        print(f"Error during model training: {e}")
        exit()

    # Evaluate the model
    print("Evaluating the model...")
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # Print detailed classification report
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Check if the model directory exists, create it if not
    model_dir = 'models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Save the trained model as 'runtime_error_model.joblib'
    try:
        print("Saving the model...")
        model_filename = os.path.join(model_dir, 'runtime_error_model.joblib')
        joblib.dump(model, model_filename)
        print(f"Runtime error model trained and saved as '{model_filename}'")
    except Exception as e:
        print(f"Error saving the model: {e}")
        exit()


if __name__ == "__main__":
    train_runtime_error_model()
