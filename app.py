import pandas as pd
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical
import matplotlib.pyplot as plt
from cn.protect import Protect
from cn.protect.privacy import KAnonymity
from cn.protect.quality import Loss

def load_and_merge_data(train_path, test_path):
    """
    Loads and merges training and testing data from specified CSV files.

    Args:
        train_path (str): Path to the training dataset CSV file.
        test_path (str): Path to the testing dataset CSV file.

    Returns:
        pd.DataFrame: Merged dataset with missing values dropped.

    Note:
        - Ensure that the datasets are preprocessed to avoid unnecessary missing values.
    """
    train_df = pd.read_csv(train_path, header=None)
    test_df = pd.read_csv(test_path, header=None)
    merged_data = pd.concat([train_df, test_df], axis=0).dropna()
    return merged_data

def apply_privacy_protection(data, k_value=5, suppression_rate=0.1):
    """
    Applies K-Anonymity to protect the dataset.

    Args:
        data (pd.DataFrame): Input dataset to be anonymized.
        k_value (int): Minimum number of records to ensure anonymity (default is 5).
        suppression_rate (float): Maximum proportion of records to suppress (default is 0.1).

    Returns:
        Protect: An object with the privacy model applied.

    Note:
        - Ensures data privacy and utility balance by limiting the suppression rate.
    """
    privacy_model = Protect(data, KAnonymity(k_value))
    privacy_model.quality_model = Loss()
    privacy_model.suppression = suppression_rate
    privacy_model.create_hierarchies()
    return privacy_model

def build_and_train_nn_model(data, target_column_index, test_ratio=0.2, random_seed=42):
    """
    Constructs and trains a neural network for multi-class classification.

    Args:
        data (pd.DataFrame): Dataset including features and target labels.
        target_column_index (int): Index of the target label column.
        test_ratio (float): Ratio of the test set (default is 0.2).
        random_seed (int): Random seed for reproducibility (default is 42).

    Returns:
        float: Accuracy of the model on the test set.

    Note:
        - A simple feedforward neural network with two hidden layers is used.
        - 'adam' optimizer and 'categorical_crossentropy' loss function for multi-class classification.
    """
    # Split features (X) and target (y)
    features = data.drop(columns=[target_column_index])
    target = to_categorical(data[target_column_index])
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=test_ratio, random_state=random_seed)
    
    # Define the neural network architecture
    nn_model = Sequential([
        Dense(64, input_dim=features.shape[1], activation='relu'),
        Dense(32, activation='relu'),
        Dense(target.shape[1], activation='softmax')
    ])
    
    # Compile the model
    nn_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Train the model
    nn_model.fit(X_train, y_train, epochs=10, batch_size=32, verbose=1)
    
    _, accuracy = nn_model.evaluate(X_test, y_test, verbose=0)
    return accuracy

if __name__ == "__main__":
    train_file = "custom_train_dataset.csv"
    test_file = "custom_test_dataset.csv"
    dataset = load_and_merge_data(train_file, test_file)
    protected_data = apply_privacy_protection(dataset)
    accuracy = build_and_train_nn_model(protected_data.data, target_column_index=-1)
    print(f"Neural Network Model Accuracy: {accuracy:.2f}")
