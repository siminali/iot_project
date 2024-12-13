import pandas as pd
import serial
import time


data = pd.read_csv('cosmos_db_export.csv')

# Define thresholds
HIGH_TRAFFIC_THRESHOLD = 1000  # Example: congestion in seconds
HIGH_POLLUTION_THRESHOLD = 1  # Example: AQI level

# Initialize Serial Communication with Arduino
arduino = serial.Serial(port='/dev/cu.usbserial-0001', baudrate=9600, timeout=1)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Wait for Arduino to initialize

#  Process Data and Send Commands
for index, row in data.iterrows():
    traffic = row['traffic_data.duration_in_traffic']  # Replace with the actual column name
    pollution = row['air_quality_data.air_quality_index']  # Replace with the actual column name

    if traffic > HIGH_TRAFFIC_THRESHOLD and pollution > HIGH_POLLUTION_THRESHOLD:
        command = "HIGH"
    else:
        command = "LOW"

    arduino.write(command.encode())  
    time.sleep(1) 


arduino.close()
