import os
import json
import time
import serial
import boto3
from time import sleep
from dotenv import load_dotenv
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Load environment variables
load_dotenv("configuration.env")
print("🧪 DYNAMODB_TABLE =", os.getenv("DYNAMODB_TABLE"))

class ParkingSystem:
    def __init__(self):
        print("🔧 Initializing Parking System...")

        # Load config values
        self.serial_port = os.getenv("SERIAL_PORT")
        self.topic = os.getenv("TOPIC")
        self.table_name = os.getenv("DYNAMODB_TABLE")
        self.region = os.getenv("AWS_REGION")

        # Serial connection to Arduino
        self.serial = serial.Serial(self.serial_port, 9600, timeout=1)
        print(f"✅ Serial port {self.serial_port} opened.")

        # AWS IoT MQTT client
        self.iot_client = AWSIoTMQTTClient("parking-system-client")
        self.iot_client.configureEndpoint(os.getenv("AWS_IOT_ENDPOINT"), int(os.getenv("AWS_IOT_PORT")))
        self.iot_client.configureCredentials(
            os.getenv("ROOT_CA_PATH"),
            os.getenv("PRIVATE_KEY_PATH"),
            os.getenv("CERTIFICATE_PATH")
        )
        self.iot_client.configureOfflinePublishQueueing(-1)
        self.iot_client.configureDrainingFrequency(2)
        self.iot_client.configureConnectDisconnectTimeout(10)
        self.iot_client.configureMQTTOperationTimeout(5)

        # DynamoDB setup
        self.dynamodb = boto3.resource('dynamodb', region_name=self.region)
        self.table = self.dynamodb.Table(self.table_name)

    def connect(self):
        self.iot_client.connect()
        print("✅ Connected to AWS IoT Core")

    def run(self):
        print("🚗 Listening for sensor data...\n")
        while True:
            try:
                if self.serial.in_waiting > 0:
                    raw = self.serial.readline().decode("utf-8", errors="ignore").strip()
                    print(f"📥 Raw input: '{raw}'")

                    parts = raw.split(",")
                    if len(parts) == 2:
                        # ✅ Convert spot ID to clean numeric string
                        spot_id = str(int(parts[0]))
                        state = parts[1]

                        # ✅ "X" = taken, "O" = available
                        display_state = "X" if state == "1" else "O"

                        payload = {
                            "spot_id": spot_id,
                            "status": display_state,
                            "timestamp": int(time.time())
                        }

                        # Publish to AWS IoT
                        self.iot_client.publish(self.topic, json.dumps(payload), 1)
                        print(f"📤 MQTT Published: {payload}")

                        # Save to DynamoDB
                        self.table.put_item(Item=payload)
                        print(f"📦 DynamoDB Updated for spot {spot_id}: {payload}\n")
                    else:
                        print("⚠️ Invalid input format.")
                sleep(0.2)
            except Exception as e:
                print("❌ Error:", e)
                sleep(1)

if __name__ == "__main__":
    system = ParkingSystem()
    system.connect()

    # Test connection
    test_message = {
        "status": "Parking system online"
    }
    system.iot_client.publish(os.getenv("TOPIC"), json.dumps(test_message), 1)
    print("🟡 Test message published to AWS IoT Core\n")

    # Start the main loop
    system.run()
