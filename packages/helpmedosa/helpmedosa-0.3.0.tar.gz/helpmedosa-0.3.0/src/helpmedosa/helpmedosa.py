"""Main module."""






#simple neural network
import tensorflow as tf 
import numpy as np 
import matplotlib.pyplot as plt

# %%
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

# %%
from tensorflow.keras.utils import to_categorical

# %%
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

# %%
fig, axes = plt.subplots(2, 5, figsize=(10, 5))
axes = axes.ravel()
for i in range(10):
    axes[i].imshow(x_train[y_train[:, i].argmax()], cmap='gray')
    axes[i].set_title(f"Digit {i}")
    axes[i].axis('off')
plt.tight_layout()
plt.show()

# %%
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Flatten, Dense

# %%
model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(10, activation='softmax')
])

# %%
weights, biases = model.layers[1].get_weights()

fig, axes = plt.subplots(2, 5, figsize=(10, 5))
axes = axes.ravel()
for i in range(10):
    axes[i].imshow(weights[:, i].reshape(28, 28), cmap='viridis')
    axes[i].set_title(f"Weights Node {i}")
    axes[i].axis('off')
plt.tight_layout()
plt.show()

# %%
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, epochs=5, validation_data=(x_test, y_test))
weights, biases = model.layers[1].get_weights()

fig, axes = plt.subplots(2, 5, figsize=(10, 5))
axes = axes.ravel()
for i in range(10):
    axes[i].imshow(weights[:, i].reshape(28, 28), cmap='viridis')
    axes[i].set_title(f"Weights Node {i}")
    axes[i].axis('off')
plt.tight_layout()
plt.show()


# %%
from sklearn.metrics import classification_report, confusion_matrix

y_pred = model.predict(x_test)
y_pred_classes = np.argmax(y_pred, axis=1)
y_true = np.argmax(y_test, axis=1)


print(classification_report(y_true, y_pred_classes))


conf_matrix = confusion_matrix(y_true, y_pred_classes)
plt.figure(figsize=(10, 8))
plt.imshow(conf_matrix, cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.colorbar()
plt.show()





#Dnn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam, SGD, RMSprop


# %%
def build_and_train_model(X_train, y_train, X_test, y_test, layers, lr, optimizer_type):
    # Build model
    model = Sequential()
    for units in layers:
        model.add(Dense(units, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # Set optimizer
    if optimizer_type == 'adam':
        optimizer = Adam(learning_rate=lr)
    elif optimizer_type == 'sgd':
        optimizer = SGD(learning_rate=lr)
    elif optimizer_type == 'rmsprop':
        optimizer = RMSprop(learning_rate=lr)
    
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])
    
    # Train model
    history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test), verbose=0)
    
    # Evaluate model
    _, accuracy = model.evaluate(X_test, y_test, verbose=0)
    
    # Generate classification report
    y_pred = (model.predict(X_test) > 0.5).astype("int32")
    report = classification_report(y_test, y_pred, output_dict=True)
    return accuracy, report['accuracy']

# %%
data = load_breast_cancer()
X = data.data
y = data.target

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Preprocess the dataset
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# %%
hyperparams = [
    {'layers': [16, 8], 'lr': 0.001, 'optimizer': 'adam'},
    {'layers': [32, 16, 8], 'lr': 0.001, 'optimizer': 'adam'},
    {'layers': [16, 8], 'lr': 0.01, 'optimizer': 'sgd'},
    {'layers': [32, 16, 8], 'lr': 0.01, 'optimizer': 'sgd'},
    {'layers': [16, 8], 'lr': 0.001, 'optimizer': 'rmsprop'},
    {'layers': [32, 16, 8], 'lr': 0.001, 'optimizer': 'rmsprop'}
]

# %%
results = []

for params in hyperparams:
    accuracy, train_acc = build_and_train_model(X_train_scaled, y_train, X_test_scaled, y_test, 
                                                layers=params['layers'], 
                                                lr=params['lr'], 
                                                optimizer_type=params['optimizer'])
    results.append({
        'Layers': params['layers'],
        'Learning Rate': params['lr'],
        'Optimizer': params['optimizer'],
        'Test Accuracy': accuracy,
        'Train Accuracy': train_acc
    })


# %%
results_df = pd.DataFrame(results)


results_df['Accuracy Difference'] = results_df['Train Accuracy'] - results_df['Test Accuracy']

print(results_df)

# %%
fig, ax = plt.subplots(figsize=(10, 6))


x_labels = [f"{params['layers']}, LR={params['lr']}, Opt={params['optimizer']}" for params in hyperparams]


ax.plot(x_labels, results_df['Train Accuracy'], label='Train Accuracy', marker='o')


ax.plot(x_labels, results_df['Test Accuracy'], label='Test Accuracy', marker='o')


ax.plot(x_labels, results_df['Accuracy Difference'], label='Accuracy Difference', marker='o', linestyle='--')

ax.set_xlabel("Hyperparameter Combinations")
ax.set_ylabel("Accuracy")
ax.set_title("Train Accuracy, Test Accuracy, and Accuracy Difference")
ax.legend()

plt.xticks(rotation=45, ha='right')

plt.tight_layout()
plt.show()






#cnn
import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.optimizers import Adam, SGD
from sklearn.metrics import classification_report
import matplotlib.pyplot as plt
import numpy as np

# Load CIFAR-10 dataset
(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Normalize the data
x_train, x_test = x_train / 255.0, x_test / 255.0

# Convert class labels to one-hot encoded format
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)


# %%
def create_simple_cnn():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(10, activation='softmax')
    ])
    return model


# %%
def create_deep_cnn():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Dropout(0.25),
        Flatten(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        Dense(10, activation='softmax')
    ])
    return model


# %%
def create_complex_cnn():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(256, activation='relu'),
        Dense(10, activation='softmax')
    ])
    return model


# %%
def compile_and_train(model, optimizer, epochs=10, batch_size=64):
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(x_test, y_test), verbose=2)
    return history, model


# %%
history_simple_adam, trained_simple_adam = compile_and_train(create_simple_cnn(), Adam(learning_rate=0.001), epochs=10)
history_deep_sgd, trained_deep_sgd = compile_and_train(create_deep_cnn(), SGD(learning_rate=0.001), epochs=10)
history_complex_adam, trained_complex_adam = compile_and_train(create_complex_cnn(), Adam(learning_rate=0.0001), epochs=10)

# %%
results = {
    "Simple CNN with Adam": trained_simple_adam.evaluate(x_test, y_test, verbose=0),
    "Deep CNN with SGD": trained_deep_sgd.evaluate(x_test, y_test, verbose=0),
    "Complex CNN with Adam (0.0001 LR)": trained_complex_adam.evaluate(x_test, y_test, verbose=0)
}


# %%
for model_name, (test_loss, test_acc) in results.items():
    print(f"{model_name} - Test Loss: {test_loss:.4f}, Test Accuracy: {test_acc:.4f}")

# Step 8: Plot accuracy over epochs for each model
def plot_history(history, title="Model Accuracy"):
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title(title)
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.show()

# Plot results for each model
plot_history(history_simple_adam, title="Simple CNN Model Accuracy")
plot_history(history_deep_sgd, title="Deep CNN Model Accuracy")
plot_history(history_complex_adam, title="Complex CNN Model Accuracy")







#lstm

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'airline-passengers.csv'  # Update this with the path to your dataset
data = pd.read_csv(file_path)

# Preprocess the data
data['Month'] = pd.to_datetime(data['Month'])
data.set_index('Month', inplace=True)

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
data_scaled = scaler.fit_transform(data[['Passengers']])

# Function to create sequences
def create_sequences(data, sequence_length=12):
    x, y = [], []
    for i in range(len(data) - sequence_length):
        x.append(data[i:i+sequence_length, 0])
        y.append(data[i+sequence_length, 0])
    return np.array(x), np.array(y)

# Create sequences with a 12-month look-back period
sequence_length = 12
x, y = create_sequences(data_scaled, sequence_length=sequence_length)
x = np.reshape(x, (x.shape[0], x.shape[1], 1))

# Define the LSTM model
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=(sequence_length, 1)),
    LSTM(50),
    Dense(1)
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(x, y, epochs=100, batch_size=16, validation_split=0.2, verbose=1)

# Plot training & validation loss values
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Make predictions
predicted = model.predict(x)

# Inverse transform the predictions and actual values to original scale
predicted = scaler.inverse_transform(predicted)
actual = scaler.inverse_transform(data_scaled[sequence_length:])

# Plot the results
plt.figure(figsize=(10,6))
plt.plot(actual, label='Actual Passengers')
plt.plot(predicted, label='Predicted Passengers')
plt.title('Passenger Prediction')
plt.xlabel('Time')
plt.ylabel('Passengers')
plt.legend()
plt.show()






#autopca

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.metrics import mean_squared_error
from tensorflow.keras.datasets import mnist
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

# Load the MNIST dataset
(x_train, _), (x_test, _) = mnist.load_data()

# Normalize the images
x_train = x_train.astype('float32') / 255.
x_test = x_test.astype('float32') / 255.

# Add noise to the images
noise_factor = 0.5
x_train_noisy = x_train + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_train.shape)
x_test_noisy = x_test + noise_factor * np.random.normal(loc=0.0, scale=1.0, size=x_test.shape)

# Clip the images to be between 0 and 1
x_train_noisy = np.clip(x_train_noisy, 0., 1.)
x_test_noisy = np.clip(x_test_noisy, 0., 1.)

# Reshape the test images for PCA
x_test_noisy_flat_pca = x_test_noisy.reshape(len(x_test_noisy), -1)  # Shape: (num_samples, 784)
x_test_flat = x_test.reshape(len(x_test), -1)  # Shape: (num_samples, 784)

# Apply PCA
pca = PCA(n_components=32)
x_test_noisy_pca = pca.fit_transform(x_test_noisy_flat_pca)
x_test_denoised_pca = pca.inverse_transform(x_test_noisy_pca)  # Shape: (num_samples, 784)
x_test_denoised_pca = x_test_denoised_pca.reshape(len(x_test_noisy), 28, 28)  # Reshape back to (num_samples, 28, 28)

# Flatten the images for the Autoencoder
x_train_noisy_flat = x_train_noisy.reshape(len(x_train_noisy), -1)  # Shape: (num_samples, 784)
x_test_noisy_flat = x_test_noisy.reshape(len(x_test_noisy), -1)  # Shape: (num_samples, 784)
x_train_flat = x_train.reshape(len(x_train), -1)  # Shape: (num_samples, 784)

# Build the Autoencoder model
input_img = Input(shape=(784,))
encoded = Dense(128, activation='relu')(input_img)
encoded = Dense(64, activation='relu')(encoded)
encoded = Dense(32, activation='relu')(encoded)

decoded = Dense(64, activation='relu')(encoded)
decoded = Dense(128, activation='relu')(decoded)
decoded = Dense(784, activation='sigmoid')(decoded)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

# Train the Autoencoder
autoencoder.fit(x_train_noisy_flat, x_train_flat, epochs=10, batch_size=256, shuffle=True, validation_data=(x_test_noisy_flat, x_test_flat))

# Predict the denoised images using the Autoencoder
denoised_images = autoencoder.predict(x_test_noisy_flat).reshape(len(x_test), 28, 28)  # Shape: (num_samples, 28, 28)

# Calculate the Mean Squared Error (MSE) for PCA and Autoencoder
mse_pca = mean_squared_error(x_test.flatten(), x_test_denoised_pca.flatten())  # Flatten to calculate MSE
mse_autoencoder = mean_squared_error(x_test.flatten(), denoised_images.flatten())  # Flatten to calculate MSE

# Function to plot results
def plot_pca_vs_autoencoder(noisy_images, pca_images, autoencoder_images, original_images, n=10):
    plt.figure(figsize=(20, 8))
    for i in range(n):
        ax = plt.subplot(4, n, i + 1)
        plt.imshow(noisy_images[i], cmap='gray')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ax = plt.subplot(4, n, i + 1 + n)
        plt.imshow(pca_images[i], cmap='gray')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ax = plt.subplot(4, n, i + 1 + 2 * n)
        plt.imshow(autoencoder_images[i], cmap='gray')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ax = plt.subplot(4, n, i + 1 + 3 * n)
        plt.imshow(original_images[i], cmap='gray')
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.show()

# Plot the results
plot_pca_vs_autoencoder(x_test_noisy, x_test_denoised_pca, denoised_images, x_test)
 
# Print the MSE results
print(f"MSE for PCA Denoising: {mse_pca}")
print(f"MSE for Autoencoder Denoising: {mse_autoencoder}")






#linear regression

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


# %%
data = pd.read_csv('detaset.csv')

# %%
plt.scatter(data['x'], data['y'])
plt.xlabel('x')
plt.ylabel('y')
plt.show()

# %%
x = data['x'].values.reshape(-1, 1)
y = data['y'].values

# %%
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# %%
X_train = np.ravel(X_train)
X_test = np.ravel(X_test)

# %%
w = np.random.randn()
b = np.random.randn()
n = len(X_train)
learning_rate=0.01


# %%
for epoch in range(1000):
        y_pred = w * X_train + b
        loss = (1/n) * np.sum((y_pred - y_train) ** 2)
        dw = np.dot((2/n),np.sum(np.dot((y_pred - y_train) , X_train)))
        db = np.dot((2/n), np.sum(y_pred - y_train))
        w -= learning_rate * dw
        b -= learning_rate * db
        print(f'Epoch {epoch}: Loss = {loss}')

# %%
    print(f'Final values - w: {w}, b: {b}')
    y_pred_test = w * X_test + b
    mse = np.mean((y_pred_test - y_test) ** 2)
    r2 = r2_score(y_test, y_pred_test)*100
    print(f'R-squared Score on Test Data: {r2}')
    print(f'Mean Squared Error on Test Data: {mse}')
    plt.scatter(X_train, y_train, color='blue', label='Training Data')
    plt.scatter(X_test, y_test, color='red', label='Testing Data')
    plt.plot(X_test, y_pred_test, color='green', label='Model Prediction')
    plt.title('Training and Testing Data with Model Prediction')
    plt.xlabel('Independent Variable')
    plt.ylabel('Dependent Variable')
    plt.legend()
    plt.show()






#logistic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %%
##import dataset
data=pd.read_csv(r"C:\Users\RIG\Downloads\suv_data.csv")
data

# %%


# %%
##make training and testing datasets
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test=train_test_split(x,y,test_size=0.20,random_state=0)
print(x_train)
print(x_test)
print(y_train)
print(y_test)

# %%

# Sigmoid function to map values to probabilities
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# Training function for logistic regression
def train_logistic_regression(x_train, y_train, learning_rate=0.01, epochs=100):
    # Initialize parameters
    w = 0.0  # Initial weight
    b = 0.0  # Initial bias
    n = len(x_train)  # Number of data points

    # Training loop
    for epoch in range(epochs):
        # Step 2: Predict probabilities using the current w and b
        z = w * x_train + b
        y_pred = sigmoid(z)
        
        # Step 3: Compute Binary Cross-Entropy Loss
        loss = -np.mean(y_train * np.log(y_pred) + (1 - y_train) * np.log(1 - y_pred))
        
        # Step 4: Compute gradients with respect to w and b
        dw = (1/n) * np.dot(x_train, (y_pred - y_train))
        db = (1/n) * np.sum(y_pred - y_train)
        
        # Step 5: Update w and b using gradient descent
        w -= learning_rate * dw
        b -= learning_rate * db
        
        # Observe loss for each epoch
        print(f"Epoch {epoch+1}/{epochs}, Loss: {loss:.4f}, w: {w:.4f}, b: {b:.4f}")

    # Print final values of w and b
    print(f"\nFinal values: w = {w:.4f}, b = {b:.4f}")
    return w, b

# Prediction function using logistic regression
def predict(x, w, b):
    z = w * x + b
    return sigmoid(z)


# %%
##use final w and b to predict the y values for the test set
##plot line on training and testing dataset
w, b = train_logistic_regression(x_train, y_train, learning_rate=0.1, epochs=200)

# Predict values for the training and testing datasets
y_train_pred = predict(x_train, w, b)
y_test_pred = predict(x_test, w, b)

# Thresholding predictions to classify as 0 or 1
y_train_class = (y_train_pred >= 0.5).astype(int)
y_test_class = (y_test_pred >= 0.5).astype(int)

# Plotting the results
plt.figure(figsize=(10, 6))

# Plot training data points
plt.scatter(x_train, y_train, color='blue', label='Training Data')
# Plot test data points
plt.scatter(x_test, y_test, color='red', label='Test Data')

# Decision boundary: plot the probability curve
x_boundary = np.linspace(min(x_train) - 1, max(x_test) + 1, 100)
y_boundary = sigmoid(w * x_boundary + b)
plt.plot(x_boundary, y_boundary, color='green', linestyle='--', label='Decision Boundary')

# Plot settings
plt.title('Logistic Regression on Training and Test Data')
plt.xlabel('x-axis')
plt.ylabel('Probability (y)')
plt.grid(True)
plt.legend()
plt.show()





#svm
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

# %%
data = datasets.load_iris()
X=data.data;
y=data.target;

# %%
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# %%

svc = SVC(kernel='poly') #rbf and linear and poly
svc.fit(X_train, y_train)


# %%
y_pred = svc.predict(X_test)

# %%
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy * 100:.2f}%")


precision = precision_score(y_test, y_pred, average='weighted')
print(f"Precision: {precision * 100:.2f}%")

recall = recall_score(y_test, y_pred, average='weighted')
print(f"Recall: {recall * 100:.2f}%")


f1 = f1_score(y_test, y_pred, average='weighted')
print(f"F1 Score: {f1 * 100:.2f}%")
print("Classification Report:\n", classification_report(y_test, y_pred))


from sklearn import datasets

# %%
data = datasets.load_iris()

# %%
data.data_train, data.data_test, data.target_train, data.target_test = train_test_split(data.data, data.target, test_size=0.3, random_state=42)


# %%
print("Training set shape:", data.data_train.shape)
print("Testing set shape:", data.data_test.shape)


# %%





#naive bayes
from sklearn import datasets

# %%
data = datasets.load_iris()

# %%
data.data_train, data.data_test, data.target_train, data.target_test = train_test_split(data.data, data.target, test_size=0.3, random_state=42)


# %%
print("Training set shape:", data.data_train.shape)
print("Testing set shape:", data.data_test.shape)
import numpy as np

# %%

class_0 = data.data_train[data.target_train == 0]
class_1 = data.data_train[data.target_train == 1]
class_2 = data.data_train[data.target_train == 2]


# %%

print("Class 0 shape:", class_0.shape)
print("Class 1 shape:", class_1.shape)
print("Class 2 shape:", class_2.shape)

print("Class 0 samples:\n", class_0[:5])
print("Class 1 samples:\n", class_1[:5])
print("Class 2 samples:\n", class_2[:5])


# %%

mean_class_0 = np.mean(class_0, axis=0)
std_class_0 = np.std(class_0, axis=0)

mean_class_1 = np.mean(class_1, axis=0)
std_class_1 = np.std(class_1, axis=0)


mean_class_2 = np.mean(class_2, axis=0)
std_class_2 = np.std(class_2, axis=0)


# %%

print("Class 0 Mean:\n", mean_class_0)
print("Class 0 Std Dev:\n", std_class_0)

print("Class 1 Mean:\n", mean_class_1)
print("Class 1 Std Dev:\n", std_class_1)

print("Class 2 Mean:\n", mean_class_2)
print("Class 2 Std Dev:\n", std_class_2)


# %%
def gaussian_pdf(x, mean, std):
    coefficient = 1 / (std * np.sqrt(2 * np.pi))
    exponent = np.exp(-0.5 * ((x - mean) / std) ** 2)
    return coefficient * exponent

# %%
def predict_naive_bayes(X, priors, means, stds):
    n_classes = len(priors)
    n_samples = X.shape[0]
    posteriors = np.zeros((n_samples, n_classes))
    
    for i in range(n_classes):
        likelihood = np.prod(gaussian_pdf(X, means[i], stds[i]), axis=1)
        posteriors[:, i] = priors[i] * likelihood
    
    return np.argmax(posteriors, axis=1)

# %%

n_samples, n_features = data.data_train.shape
n_classes = len(np.unique(data.target_train))


priors = np.array([np.sum(data.target_train == i) / n_samples for i in range(n_classes)])

means = np.array([data.data_train[data.target_train == i].mean(axis=0) for i in range(n_classes)])
stds = np.array([data.data_train[data.target_train == i].std(axis=0) for i in range(n_classes)])


# %%

data.target_pred = predict_naive_bayes(data.data_test, priors, means, stds)


# %%
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

accuracy = accuracy_score(data.target_test, data.target_pred)
print(f"Accuracy: {accuracy:.2f}")

conf_matrix = confusion_matrix(data.target_test, data.target_pred)
print("Confusion Matrix:")
print(conf_matrix)

class_report = classification_report(data.target_test, data.target_pred, target_names=data.target_names)
print("Classification Report:")
print(class_report)