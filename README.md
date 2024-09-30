# Arrhythmia Detect

**Arrhythmia Detect** is a personal project designed to monitor patients' ECG signals and detect arrhythmic conditions. If arrhythmia is detected, the system immediately alerts a caregiver and, if necessary, dispatches emergency medical services.

## Features
- **ECG Monitoring**: Continuously evaluates ECG signals using a machine learning model to identify arrhythmic events.
- **Caregiver Alerts**: Utilizes Twilio API to call caregivers when arrhythmia is detected. If the caregiver is unreachable, the system contacts emergency services.

## Implementation
**Hardware**:
- **Arduino Pro Mini** with FTDI basic breakout for microcontroller communication.
- **AD8232 ECG Sensor**: Captures single-lead ECG signals, transmitting them as analog data to a PC.

**Software**:
- **Machine Learning Model**: Developed a convolutional neural network using the VGG16 architecture to process 1-D ECG signals and detect arrhythmia. The model, trained on over 500,000 patient datasets, achieves an accuracy of 99.7%.
- **Twilio API Integration**: Automatically calls caregivers and relays critical patient data through a voice bot in case of emergency.

## Key Challenges
- Initial hardware setup required extensive troubleshooting.
- Security breach when Twilio credentials were accidentally exposed on GitHub.

## Lessons Learned
- Gained hands-on experience with machine learning, hardware integration, and efficient task management in a fast-paced environment.