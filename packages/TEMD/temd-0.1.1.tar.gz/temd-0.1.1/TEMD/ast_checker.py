#ast
import requests
import joblib
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os


def train_ast_error_model():
    print("Starting to train the AST error model...")

    # Fetch the AST error dataset
    dataset_url = "https://raw.githubusercontent.com/GC1221YT/error_syntax_indentation_dataset/main/syntax_indentation_dataset.json"
    response = requests.get(dataset_url)

    if response.status_code != 200:
        print(f"Failed to fetch the dataset. Status code: {response.status_code}")
        exit()

    # Attempt to clean the raw JSON response to handle invalid escape sequences
    raw_data = response.text

    # Fix common invalid escape sequences by using a regex pattern to handle them
    cleaned_data = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', raw_data)  # Escape single backslashes
    cleaned_data = re.sub(r'\\[ntr]', ' ', cleaned_data)  # Replace \n, \t, \r with spaces

    # Try to parse the cleaned data into JSON
    try:
        data = json.loads(cleaned_data)
    except ValueError as e:
        print(f"Error parsing cleaned JSON: {e}")
        exit()

    # Debug: print the type of data and inspect the first few items
    print(f"Data type: {type(data)}")
    print(f"Keys in data: {list(data.keys())}")  # Print out the top-level keys

    # Initialize lists to hold error messages and explanations
    error_messages = []
    explanations = []

    # Extract data from 'syntax_errors' and 'indentation_errors' lists
    for error_category in ['syntax_errors', 'indentation_errors']:
        if error_category in data:
            print(f"Processing {error_category}...")
            error_list = data[error_category]
            for item in error_list:
                # Add error message and explanation to the lists
                error_messages.append(item.get('error_message', ''))
                explanations.append(item.get('explanation', ''))

    # Ensure that both error_messages and explanations are not empty
    if not error_messages or not explanations:
        print("Error messages or explanations are missing in the dataset. Exiting.")
        exit()

    # Split the data into training and testing sets
    print("Splitting the data into training and testing sets...")
    X_train, X_test, y_train, y_test = train_test_split(error_messages, explanations, test_size=0.2, random_state=42)

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
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # Print detailed classification report
    print("Classification Report:")
    print(classification_report(y_test, y_pred))

    # Check if the model directory exists, create it if not
    model_dir = 'models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Save the trained model as 'ast_error_model.joblib'
    try:
        print("Saving the model...")
        model_filename = os.path.join(model_dir, 'ast_error_model.joblib')
        joblib.dump(model, model_filename)
        print(f"AST error model trained and saved as '{model_filename}'")
    except Exception as e:
        print(f"Error saving the model: {e}")
        exit()


if __name__ == "__main__":
    train_ast_error_model()
