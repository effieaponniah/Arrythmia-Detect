import csv
import serial
from tensorflow import keras
import time
from twilio.rest import Client
import pandas as pd
from tkinter import *

# Attempt to connect to Arduino device at specified port and baud rate
try:
    arduino = serial.Serial("COM8", timeout=1, baudrate=9600) 
except serial.SerialException as e:
    print(f'Error: {e}. Please check the port connection.')

# Open a new CSV file to record the sensor data
with open("effiea_sensor_data.csv", "w") as new_file:
    csv_writer = csv.writer(new_file, lineterminator=',')
    line_count = 0

    # Read data continuously from the Arduino
    while True:
        rawdata = str(arduino.readline().strip())  # Read and clean the raw data from the serial port
        line_count += 1
        if line_count > 2:  # Skip the first two lines as they may contain noise
            def clean(data_str):
                """
                Clean the raw data string by removing unnecessary characters
                and converting it to a normalized float value.
                """
                data_str = data_str[2:]  # Remove leading '\\b'
                data_str = data_str[:-1]  # Remove trailing '\\'
                return int(data_str) / 1024  # Normalize the data

            cleaned_data = clean(rawdata)
            csv_writer.writerow([cleaned_data]) 

        # Stop recording after 188 lines of data
        if line_count > 188:
            break

print("Data Recording Complete.")

# Load the pre-recorded data for prediction
myFile = pd.read_csv("bradyarrythmia.csv", header=None)

# Load the pre-trained Keras model for arrhythmia detection
try:
    model = keras.models.load_model("arrhythmia_model.h5")
except IOError as e:
    print(f"Error loading model: {e}. Make sure 'arrhythmia_model.h5' is available.")

# Perform predictions using the model on the loaded data
predictions = model.predict(myFile)

classificationFull = [
    "Normal",
    "Premature atrial contraction",
    "Premature ventricular contraction or Ventricular escape",
    "Ventricular fibrillation",
    "Bradyarrhythmias",
]

indexValue = 0
mostLikely = max(predictions[0])
for i in range(len(predictions[0])):
    if mostLikely == predictions[0][i]:
        indexValue = i

percentage = mostLikely * 100
print(f"Prediction Probability: {percentage:.2f}%")
print(f"Predicted Class Index: {indexValue}")

print(f"\nThe patient is likely to have a {percentage:.6f}% chance of {classificationFull[indexValue]}.\n")

# If normal readings, provide reassurance. Otherwise, trigger an alert.
if indexValue == 0:
    print("Patient seems to have normal readings.")
else:
    account_sid = "YOUR_ACCOUNT_SID"
    auth_token = "YOUR_AUTH_TOKEN"
    caregiver_number = "CAREGIVER_PHONE_NUMBER"
    twilio_number = "TWILIO_PHONE_NUMBER"

    # Establish Twilio client connection
    client = Client(account_sid, auth_token)

    # Make a call to the caregiver
    try:
        call = client.calls.create(
            to=caregiver_number,
            from_=twilio_number,
            url='http://demo.twilio.com/docs/voice.xml'
        )
        print(f"Call initiated: {call.sid}")
    except Exception as e:
        print(f"Error initiating call: {e}")

    # Send an SMS alert to the caregiver
    try:
        message = client.messages.create(
            body='Alert: Patient Effiea Ponniah is experiencing abnormal heart activity. Immediate attention required.',
            from_=twilio_number,
            to=caregiver_number
        )
        print(f"Message sent: {message.sid}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Display the diagnosis result
root = Tk()
root.title("Arrhythmia Diagnosis Result")

# Display patient name and diagnosis on the GUI
label_00 = Label(root, text="Effiea Ponniah", bg="green", fg="black", font='Helvetica 24 bold')
label_01 = Label(root, text="Diagnosis:", font='Helvetica 18 bold')
label_01_value = Label(root, text=classificationFull[indexValue], font='Helvetica 20 bold')

# Arrange the labels on the GUI window using grid layout
label_00.grid(row=0)
label_01.grid(row=1)
label_01_value.grid(row=1, column=1)

# Display probability percentages for all classifications
for i in range(len(predictions[0])):
    percent = f"{predictions[0][i] * 100:.2f}%"
    label_i = Label(root, text=classificationFull[i], font='Helvetica 18')
    label_i_value = Label(root, text=percent, font='Helvetica 18')
    label_i.grid(row=i + 2)
    label_i_value.grid(row=i + 2, column=1)

root.mainloop()
