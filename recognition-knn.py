import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import joblib

# Define the base path for the image data
base_path = "images/"

# Initialize lists to store feature vectors (X) and labels (y)
X = []
y = []

# Process training and validation data
for dataset_type in ["train", "validation"]:
    dataset_path = os.path.join(base_path, dataset_type)
    for expression in os.listdir(dataset_path):
        expression_path = os.path.join(dataset_path, expression)
        label = expression  # Label is based on the subdirectory name
        for image_file in os.listdir(expression_path):
            image_path = os.path.join(expression_path, image_file)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Load the image in grayscale
            # Preprocess the image as needed (resize, normalize, etc.)
            # Flatten the image and append it to X
            X.append(image.flatten())
            y.append(label)

# Convert the lists to NumPy arrays for further processing
X = np.array(X)
y = np.array(y)

# Encode the labels into numerical values
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize (normalize) the features for k-NN
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create a k-NN classifier with the desired number of neighbors
knn_classifier = KNeighborsClassifier(n_neighbors=5)  # You can adjust 'n_neighbors' as needed

# Train the k-NN classifier
knn_classifier.fit(X_train, y_train)

# Make predictions using the trained k-NN classifier
y_pred = knn_classifier.predict(X_test)

# Evaluate the k-NN classifier's performance
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:\n", report)

# Save the k-NN model, label encoder, and scaler to files
joblib.dump(knn_classifier, 'knn_model.pkl')
joblib.dump(label_encoder, 'label_encoder.pkl')
joblib.dump(scaler, 'scaler.pkl')
s