import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import serial
import time
import warnings

warnings.filterwarnings("ignore")

ser = serial.Serial('COM24', baudrate=9600)  # Adjust COM port and baudrate as needed
print("Serial connection opened successfully!")

# Load data from an Excel sheet and split into features and labels
data = pd.read_excel("dataset.xlsx", engine="openpyxl")

feature_1 = data['distence_val']
feature_2 = data['temp_val']
feature_3 = data['rain_Val']
feature_4 = data['flow_Val']

label_1 = data['label_distence']
label_2 = data['label_temp']
label_3 = data['label_rain']
label_4 = data['label_flow']

# Split the data
X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(feature_1, label_1, test_size=0.2, random_state=42)
X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(feature_2, label_2, test_size=0.2, random_state=42)
X_train_3, X_test_3, y_train_3, y_test_3 = train_test_split(feature_3, label_3, test_size=0.2, random_state=42)
X_train_4, X_test_4, y_train_4, y_test_4 = train_test_split(feature_4, label_4, test_size=0.2, random_state=42)

# Build Random Forest models
model_1 = RandomForestClassifier(random_state=42).fit(X_train_1.values.reshape(-1, 1), y_train_1)
model_2 = RandomForestClassifier(random_state=42).fit(X_train_2.values.reshape(-1, 1), y_train_2)
model_3 = RandomForestClassifier(random_state=42).fit(X_train_3.values.reshape(-1, 1), y_train_3)
model_4 = RandomForestClassifier(random_state=42).fit(X_train_4.values.reshape(-1, 1), y_train_4)

def readData():
    serial_data = ser.readline().decode().strip()

    print("\n----------------------------")
    print("     -= Data Received =- ")
    print("----------------------------\n")
    print("Data:", serial_data, "\n")

    distence_val = float(serial_data[serial_data.find("a")+1 : serial_data.find("b")])
    temp_val   = float(serial_data[serial_data.find("b")+1 : serial_data.find("c")])
    rain_Val = int(serial_data[serial_data.find("c")+1 : serial_data.find("d")])
    flow_Val  = int(serial_data[serial_data.find("d")+1 : serial_data.find("e")])
    humidity  = float(serial_data[serial_data.find("e")+1 : serial_data.find("f")])
    pressure  = float(serial_data[serial_data.find("f")+1 : serial_data.find("g")])                
    print("distence_val:", distence_val)
    print("temp_val:", temp_val)
    print("rain_Val:", rain_Val)
    print("flow_Val:", flow_Val)

    return distence_val, temp_val, rain_Val, flow_Val

while True:
    distence_val, temp_val, rain_Val, flow_Val = readData()

    u_prediction = model_1.predict([[distence_val]])[0]
    v_prediction = model_2.predict([[temp_val]])[0]
    w_prediction = model_3.predict([[rain_Val]])[0]
    x_prediction = model_4.predict([[flow_Val]])[0]

    print("\nPredictions:")
    print(f'U Prediction: {u_prediction}')
    print(f'V Prediction: {v_prediction}')
    print(f'W Prediction: {w_prediction}')
    print(f'X Prediction: {x_prediction}')

    if u_prediction == 1:
        print("Feature 1 is normal")
    else:
        print("Abnormal Feature 1 detected")

    if v_prediction == 1:
        print("Feature 2 is normal")
    else:
        print("Abnormal Feature 2 detected")

    if w_prediction == 1:
        print("Feature 3 is normal")
    else:
        print("Abnormal Feature 3 detected")

    if x_prediction == 1:
        print("Feature 4 is normal")
    else:
        print("Abnormal Feature 4 detected")

    values_string = f"t{u_prediction}u{v_prediction}v{w_prediction}w{x_prediction}x"
    ser.write(values_string.encode())
    print(values_string)
    print("completed")

    time.sleep(0.05)  # small delay for stable serial communication
