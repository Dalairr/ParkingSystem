# Smart Parking System – Capstone Project
Dalair Franzen | CLDE2291-01 | Spring 2025

## Project Elevator Pitch
This project is a smart parking system that uses a Raspberry Pi and Arduino to detect vehicle presence in real time. It sends sensor data to AWS IoT Core, stores it in DynamoDB, and displays the parking layout through a live web interface.

## Quick Start – Build & Run
These steps assume you're running the Raspberry Pi with Python 3 and dependencies installed.

### Raspberry Pi Setup
```bash
# Clone the project
git clone https://github.com/Dalairr/ParkingSystem.git
cd RaspberryPiParkingSystem

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the parking system
python3 parking_system.py

# Find host name
5. Find host name `hostname -I`
# Web Interface Thru (Static Hosting)
6. Place the index.html file in /var/www/html/ and open http://<raspberrypi-local-ip>/ in a browser.

parking_system.py - Main Python script reading sensor data and updating AWS
configuration.env - Environment variables (AWS endpoint, certs, serial port)
requirements.txt - Python dependencies
index.html - Frontend visual of the parking layout
/Presentation_Materials/ - PDF of slide deck and demo reference
/Design_Documentation/ - System diagram, flowchart, and rationale
/Testing_Validation/ - Final report and test logs
/Deployment_Guide/ - Step-by-step AWS + device deployment instructions
/User_Guide/ - Overview of how to use the system, screenshots included
/Reflection/ - Personal growth, lessons learned, and recommendations
/Physical_Aid_Images/ - Pictures of the Raspberry Pi + Arduino hardware (optional)