# AI-Driven LoRaWAN Flood Prediction System

Real-time environmental monitoring system that ingests data from 5 sensor
types and triggers sub-2-minute flood alerts using a trained ML model.

## Tech Stack
Python · Arduino · LoRaWAN · NodeMCU · GSM · GPS · scikit-learn · Pandas · NumPy

## How It Works
1. Arduino UNO collects data from rain, ultrasonic, BMP180, DHT11, and flow sensors
2. NodeMCU transmits sensor data to the system via serial communication
3. Python reads live sensor data, runs a Random Forest classifier per sensor channel
4. If any channel predicts abnormal reading, a location-tagged alert is dispatched via GSM + GPS

## ML Model
- Algorithm: Random Forest Classifier (scikit-learn)
- 4 separate models trained per sensor type: distance, temperature, rain, flow
- Trained on labelled sensor dataset (`dataset.xlsx`)
- Live predictions loop every 5 seconds via serial port

## Results
- Sub-2-minute warning lead time in lab tests
- 60% reduction in emergency response initiation time

## Files
- `modified.py` — main ML prediction and serial communication script
- `m22.py` — alternate version of the prediction pipeline
- `dataset.xlsx` — labelled sensor readings used for model training
- `source_code.docx` — full documented source code
- `ppt_batch6.pptx` — project presentation
- `project-report.pdf` — detailed project report

## Setup
1. Connect Arduino UNO via USB (COM3 by default — update port in script if needed)
2. Install dependencies: `pip install pandas numpy scikit-learn openpyxl pyserial`
3. Run `python modified.py`
4. Live sensor readings and flood predictions will display in the terminal
