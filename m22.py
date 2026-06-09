import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import serial
import time
import warnings

warnings.filterwarnings("ignore")

# ----------------------------
# Serial connection
# ----------------------------
ser = serial.Serial('COM3', baudrate=9600, timeout=1)
print("Serial connection opened successfully!")

# ----------------------------
# Load dataset
# ----------------------------
data = pd.read_excel("dataset.xlsx", engine="openpyxl")

# Extract features and labels
feature_1 = data['distence_val']
feature_2 = data['temp_val']
feature_3 = data['rain_Val']
feature_4 = data['flow_Val']

label_1 = data['label_distence']
label_2 = data['label_temp']
label_3 = data['label_rain']
label_4 = data['label_flow']

# ----------------------------
# Split data
# ----------------------------
X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(feature_1, label_1, test_size=0.2, random_state=42)
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(feature_2, label_2, test_size=0.2, random_state=42)
X_train_3, X_test_3, y_train_3, y_test_3 = train_test_split(feature_3, label_3, test_size=0.2, random_state=42)
X_train_4, X_test_4, y_train_4, y_test_4 = train_test_split(feature_4, label_4, test_size=0.2, random_state=42)

# ----------------------------
# Train models
# ----------------------------
model_1 = RandomForestClassifier(random_state=42).fit(X_train_1.values.reshape(-1, 1), y_train_1)
model_2 = RandomForestClassifier(random_state=42).fit(X_train_2.values.reshape(-1, 1), y_train_2)
model_3 = RandomForestClassifier(random_state=42).fit(X_train_3.values.reshape(-1, 1), y_train_3)
model_4 = RandomForestClassifier(random_state=42).fit(X_train_4.values.reshape(-1, 1), y_train_4)

# ----------------------------
# Function to read and parse serial data
# ----------------------------
def readData():
    """Read and safely parse serial data from Arduino."""
    serial_data = ser.readline().decode(errors='ignore').strip()
    if not serial_data:
        return None

    # Remove unwanted prefix
    if "Received:" in serial_data:
        serial_data = serial_data.split("Received:")[-1].strip()

    # Cut off anything after 'g'
    if "g" in serial_data:
        serial_data = serial_data[:serial_data.find("g") + 1]

    print("\n----------------------------")
    print("     -= Data Received =- ")
    print("----------------------------\n")
    print("Cleaned Data:", serial_data, "\n")

    # Expected markers in order
    markers = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    if not all(m in serial_data for m in markers):
        print("⚠️ Invalid or incomplete data received, skipping this line...")
        return None

    try:
        distence_val = float(serial_data[serial_data.find("a") + 1: serial_data.find("b")])
        temp_val = float(serial_data[serial_data.find("b") + 1: serial_data.find("c")])
        rain_Val = float(serial_data[serial_data.find("c") + 1: serial_data.find("d")])
        flow_Val = float(serial_data[serial_data.find("d") + 1: serial_data.find("e")])
        humidity = float(serial_data[serial_data.find("e") + 1: serial_data.find("f")])
        pressure = float(serial_data[serial_data.find("f") + 1: serial_data.find("g")])

        print(f"distence_val: {distence_val}")
        print(f"temp_val: {temp_val}")
        print(f"rain_Val: {rain_Val}")
        print(f"flow_Val: {flow_Val}")
        print(f"humidity: {humidity}")
        print(f"pressure: {pressure}")

        return distence_val, temp_val, rain_Val, flow_Val

    except ValueError as e:
        print(f"⚠️ Error parsing numeric values ({e}). Skipping line...")
        return None

# ----------------------------
# Main loop
# ----------------------------
while True:
    result = readData()
    if result is None:
        continue  # Skip if data is invalid

    distence_val, temp_val, rain_Val, flow_Val = result

    # ----------------------------
    # Predictions
    # ----------------------------
    u_prediction = model_1.predict([[distence_val]])[0]
    v_prediction = model_2.predict([[temp_val]])[0]
    w_prediction = model_3.predict([[rain_Val]])[0]
    x_prediction = model_4.predict([[flow_Val]])[0]

    print("\nPredictions:")
    print(f'U Prediction: {u_prediction}')
    print(f'V Prediction: {v_prediction}')
    print(f'W Prediction: {w_prediction}')
    print(f'X Prediction: {x_prediction}')
    print()

    # ----------------------------
    # Interpret results
    # ----------------------------
    print("Feature 1:", "Normal ✅" if u_prediction == 1 else "⚠️ Abnormal")
    print("Feature 2:", "Normal ✅" if v_prediction == 1 else "⚠️ Abnormal")
    print("Feature 3:", "Normal ✅" if w_prediction == 1 else "⚠️ Abnormal")
    print("Feature 4:", "Normal ✅" if x_prediction == 1 else "⚠️ Abnormal")

    # ----------------------------
    # Send results over serial
    # ----------------------------
    values_string = f"t{u_prediction}u{v_prediction}v{w_prediction}w{x_prediction}x"
    ser.write(values_string.encode())
    print(f"\nSent to serial: {values_string}")
    print("Cycle completed ✅\n")

    time.sleep(5)
