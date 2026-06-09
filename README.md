# flood-prediction-lorawan
Real-time flood prediction system using LoRaWAN, multi-sensor pipeline, and threshold-based alerting.
# AI-Driven LoRaWAN Flood Prediction System

Real-time environmental monitoring system that ingests data from 5 sensor 
types and triggers sub-2-minute flood alerts using threshold-based logic.

## Tech Stack
Python · Arduino · LoRaWAN · NodeMCU · GSM · GPS

## How It Works
1. Arduino UNO collects data from rain, ultrasonic, BMP180, DHT11, and flow sensors
2. NodeMCU transmits data to cloud via LoRaWAN
3. Python alerting logic detects abnormal water-level events
4. GSM + GPS module dispatches location-tagged alerts to authorities

## Results
- Sub-2-minute warning lead time in lab tests
- 60% reduction in emergency response initiation time

## Setup
first upload programme into python environment and then give all connections using usb cables to your system one is system managable usb that will handle bby us and another one is to manage environment changes where we need to measure changes and then execute the code the output should show on our system using sensors as abnormal in  system display it is showing longitude latitude values.
