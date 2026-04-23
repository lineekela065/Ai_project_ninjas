

import sys
import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# image size we resize everything to (30x30 pixels as required)
IMG_SIZE = 30

# number of traffic sign categories in GTSRB dataset
NUM_CATEGORIES = 43

# how many times to train over the data
EPOCHS = 10

# 80% training, 20% testing split
TEST_SPLIT = 0.2


def main():
    # check command line arguments
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python3 traffic.py <data_folder> [model_filename]")
        sys.exit(1)

    data_folder = sys.argv[1]
    model_save_file = sys.argv[2] if len(sys.argv) == 3 else None

    # load all the images and labels from the dataset
    print("Loading data...")
    images, labels = load_data(data_folder)
    print("Data loaded.")

    # split into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(
        images, labels, test_size=TEST_SPLIT, random_state=42
    )

    # convert labels to one-hot encoding for the neural network
    y_train = keras.utils.to_categorical(y_train, NUM_CATEGORIES)
    y_test_categorical = keras.utils.to_categorical(y_test, NUM_CATEGORIES)

    # build the CNN model
    print("Training model...")
    model = build_model()

    # train the model
    model.fit(
        x_train, y_train,
        epochs=EPOCHS,
        validation_split=0.1,
        verbose=1
    )

    # evaluate on the test set
    print("Evaluating model")
    loss, accuracy = model.evaluate(x_test, y_test_categorical, verbose=0)
    print(f"Model accuracy: {accuracy:.4f}")

    # save the model if a filename was given
    if model_save_file:
        model.save(model_save_file)
        print(f"Model saved to {model_save_file}")


def load_data(data_folder):
    """
    Loads all images and labels from the GTSRB dataset folder.

    The folder should have 43 subfolders named 0 to 42.
    Each subfolder contains images of that traffic sign category.

    Returns:
        images - numpy array of shape (N, 30, 30, 3)
        labels - list of integer labels (0 to 42)
    """
    images = []
    labels = []

    # loop through each category folder (0 to 42)
    for category in range(NUM_CATEGORIES):
        category_folder = os.path.join(data_folder, str(category))

        # skip if the folder doesnt exist
        if not os.path.isdir(category_folder):
            print(f"Warning: folder {category_folder} not found, skipping")
            continue

        # load every image in this category folder
        for filename in os.listdir(category_folder):
            # only load image files
            if not filename.lower().endswith((".jpg", ".jpeg", ".png", ".ppm")):
                continue

            filepath = os.path.join(category_folder, filename)

            # read image with opencv
            img = cv2.imread(filepath)

            if img is None:
                continue

            # resize to 30x30 pixels
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

            images.append(img)
            labels.append(category)

    # convert to numpy arrays and normalize pixel values to 0-1
    images = np.array(images, dtype="float32") / 255.0
    labels = np.array(labels)

    return images, labels


def build_model():
    """
    Builds and compiles the CNN model.

    Architecture:
    - Two convolutional layers to extract features from the images
    - Max pooling layers to reduce size
    - Dropout to prevent overfitting
    - Dense layers for classification
    - Output layer with 43 nodes (one per traffic sign category)
    """

    model = keras.Sequential([
        # first convolutional block
        layers.Conv2D(32, (3, 3), activation="relu", input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.MaxPooling2D(pool_size=(2, 2)),

        # second convolutional block - more filters to learn complex patterns
        layers.Conv2D(64, (3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),

        # third convolutional block for even more detail
        layers.Conv2D(128, (3, 3), activation="relu"),

        # flatten to feed into dense layers
        layers.Flatten(),

        # fully connected layer
        layers.Dense(256, activation="relu"),

        # dropout to reduce overfitting (randomly turn off 50% of neurons)
        layers.Dropout(0.5),

        # output layer - 43 nodes for 43 sign categories, softmax gives probabilities
        layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])


    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.summary()

    return model


if __name__ == "__main__":
    main()
