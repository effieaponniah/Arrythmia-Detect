from tensorflow import keras
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Activation
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tkinter import *
import os

# Load the ECG data from the CSV file
# The data is expected to be a preprocessed dataset for model prediction
myFile = pd.read_csv("datafile.csv", header=None)

# Load the pre-trained deep learning model for arrhythmia classification
# The model has been trained on a dataset of ECG signals to detect different types of arrhythmias
model = keras.models.load_model("arrhythmia_model.h5")

# Predict the arrhythmia type based on the input data
# The model outputs a probability distribution over the possible classifications
predict = model.predict(myFile)

# List of possible arrhythmia classifications corresponding to the model's output
classificationFull = [
    "Normal",
    "Premature atrial contraction",
    "Premature ventricular contraction or Ventricular escape",
    "Ventricular fibrillation",
    "Bradyarrhythmias",
]

# Find the most likely classification from the model's predictions
mostLikely = max(predict[0])
for i in range(len(predict[0])):
    if mostLikely == predict[0][i]:
        indexValue = i

# Calculate the probability percentage for the most likely classification
percentage = mostLikely * 100
print(percentage)
print(indexValue)

# Print a formatted message indicating the classification result
print("\nThe Patient is likely to have {:8.6f}% chance of {}.\n".format(percentage, classificationFull[indexValue]))

# Create a Tkinter GUI window to display the classification result
root = Tk()
root.title("Arrhythmia Classification Result")

# Display patient's name and the diagnosis on the GUI
label_00 = Label(root, text="Luke Edward", bg="green", fg="black", font='Helvetica 24 bold')
label_01 = Label(root, text="Diagnosis:", font='Helvetica 18 bold')
label_01_value = Label(root, text=classificationFull[indexValue], font='Helvetica 20 bold')

# Organize the labels using grid layout
label_00.grid(row=0)
label_01.grid(row=1)
label_01_value.grid(row=1, column=1)

# Display the probability percentages for all classifications
for i in range(len(predict[0])):
    percent = str(predict[0][i] * 100)
    label_i = Label(root, text=classificationFull[i], font='Helvetica 18')
    label_i_value = Label(root, text=percent[:6] + "%", font='Helvetica 18')
    label_i.grid(row=i + 2)
    label_i_value.grid(row=i + 2, column=1)

# Start the Tkinter GUI main loop
root.mainloop()
