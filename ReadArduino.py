import csv
import serial
import datetime

def connect_device(port="COM8", baudrate=9600, timeout=1):
    """
    Establishes a serial connection to the device.

    Args:
        port (str): Serial port name (e.g., "COM8").
        baudrate (int): Communication speed (default is 9600).
        timeout (int/float): Time in seconds before timeout (default is 1).

    Returns:
        serial.Serial: Serial connection object if successful, otherwise None.

    Note:
        - Verify that the port and baud rate match the device's settings.
    """
    try:
        return serial.Serial(port, baudrate=baudrate, timeout=timeout)
    except serial.SerialException as e:
        print(f"Error connecting to device: {e}")
        return None

def parse_device_data(raw_data):
    """
    Parses and normalizes the raw data from the device.

    Args:
        raw_data (str): Raw string data from the serial device.

    Returns:
        float: Normalized data value, or None if parsing fails.

    Note:
        Assumes format like "\\bxxx\\", where 'xxx' is the numeric value.
    """
    try:
        return int(raw_data.strip()[2:-1]) / 1024
    except (ValueError, IndexError) as e:
        print(f"Error parsing data: {e}")
        return None

def log_data(serial_conn, file_name=None, max_entries=188):
    """
    Logs data from the device to a CSV file.

    Args:
        serial_conn (serial.Serial): Active serial connection.
        file_name (str): CSV file name for logging (default is a timestamped name).
        max_entries (int): Max number of data entries to record (default is 188).

    Returns:
        None
    
    Note:
        - If no file name is provided, a timestamped name is generated.
        - Useful for logging real-time sensor data for further analysis.
    """
    if serial_conn is None:
        print("No serial connection available.")
        return

    if file_name is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"device_log_{timestamp}.csv"

    with open(file_name, "w", newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        entry_count = 0

        while entry_count < max_entries:
            raw_data = serial_conn.readline().decode('utf-8').strip()
            parsed_data = parse_device_data(raw_data)
            
            if parsed_data is not None:
                csv_writer.writerow([parsed_data])
                entry_count += 1

    print(f"Data logging complete. File saved as: {file_name}")

if __name__ == "__main__":
    device_conn = connect_device()
    log_data(device_conn, max_entries=250)