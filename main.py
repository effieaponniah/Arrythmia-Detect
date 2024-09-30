import csv
import serial
import pandas as pd
import time
from tensorflow import keras
from twilio.rest import Client
from tkinter import *

def initialize_device_connection(port="COM8", baudrate=9600, timeout=1):
    """
    Establishes a serial connection to the specified device.

    Args:
        port (str): Serial port name (e.g., "COM8").
        baudrate (int): Communication speed in bits per second (default is 9600).
        timeout (int/float): Time to wait for data before giving up (default is 1 second).

    Returns:
        serial.Serial: A serial connection object if successful, otherwise None.
        
    Raises:
        serial.SerialException: If the port cannot be accessed.

    Note:
        Verify the port and baud rate for the specific hardware setup.
    """
    try:
        return serial.Serial(port, baudrate=baudrate, timeout=timeout)
    except serial.SerialException as e:
        print(f"Error initializing device connection: {e}")
        return None

def normalize_device_data(raw_data):
    """
    Cleans and normalizes the raw data received from the device.

    Args:
        raw_data (str): Raw data string read from the device.

    Returns:
        float: Normalized data value, or None if parsing fails.

    Note:
        Assumes data format like "\\bxxx\\", where 'xxx' is the numeric value to extract.
    """
    try:
        return int(raw_data.strip()[2:-1]) / 1024
    except (ValueError, IndexError) as e:
        print(f"Error cleaning data: {e}")
        return None

def log_data_to_csv(device_conn, output_file="device_data_log.csv", max_lines=188):
    """
    Logs data from the device to a CSV file.

    Args:
        device_conn (serial.Serial): Active serial connection object.
        output_file (str): Path to the CSV file for data logging (default is "device_data_log.csv").
        max_lines (int): Maximum number of data lines to record (default is 188).

    Returns:
        None
    
    Note:
        - Continuously reads data, processes it, and writes it to the specified CSV file.
        - Stops once the maximum number of lines is reached or if the connection is unavailable.
    """
    if device_conn is None:
        print("No active serial connection available.")
        return

    with open(output_file, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        line_count = 0

        while line_count < max_lines:
            raw_data = device_conn.readline().decode('utf-8').strip()
            processed_data = normalize_device_data(raw_data)
            
            if processed_data is not None:
                csv_writer.writerow([processed_data]) 
                line_count += 1

    print(f"Data logging complete. Saved to {output_file}")

def load_prediction_model(model_path):
    """
    Loads a pre-trained neural network model from the specified path.

    Args:
        model_path (str): Path to the .h5 model file.

    Returns:
        keras.Model: Loaded Keras model object, or None if loading fails.

    Note:
        Ensure the model path is correct and the file is accessible.
    """
    try:
        return keras.models.load_model(model_path)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def launch_gui():
    """
    Launches a basic GUI to display ECG monitoring status.
    """
    root = Tk()
    root.title("ECG Monitoring Dashboard")
    label = Label(root, text="Recording and Analyzing ECG Data in Real-Time...")
    label.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    arduino_device = initialize_device_connection()
    log_data_to_csv(arduino_device)
    ecg_model = load_prediction_model("ecg_prediction_model.h5")    
    launch_gui()
